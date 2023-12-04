"""Views to run the personalized canvas email action."""
import datetime
import json
from typing import Dict, Optional, Tuple
from zoneinfo import ZoneInfo

import requests
from celery.utils.log import get_task_logger
from django import http
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from rest_framework import status

from ontask import models
from ontask.action.evaluate import evaluate_action
from ontask.action.services.edit_factory import ActionOutEditProducerBase
from ontask.action.services.run_factory import ActionRunProducerBase
from ontask.core import canvas_do_burst_pause, canvas_get_or_set_oauth_token
from ontask.oauth import services

LOGGER = get_task_logger('celery_execution')


def _refresh_and_retry_send(
    oauth_info,
    conversation_url: str,
    canvas_email_payload: Dict,
    user_token: models.OAuthUserToken
):
    """Refresh OAuth token and retry send.

    :param oauth_info: Object with the oauth information
    :param conversation_url: URL to send the conversation
    :param canvas_email_payload: Dictionary with additional information
    :return:
    """
    # Request rejected due to token expiration. Refresh the token
    result_msg = gettext('OAuth token refreshed')
    response_status = None
    try:
        if user_token := services.refresh_token(user_token, oauth_info):
            # Update the header with the new token
            headers = {
                'content-type':
                    'application/x-www-form-urlencoded; charset=UTF-8',
                'Authorization': 'Bearer {0}'.format(
                    user_token.access_token,
                ),
            }

            # Second attempt at executing the API call
            response = requests.post(
                url=conversation_url,
                data=canvas_email_payload,
                headers=headers)
            response_status = response.status_code
    except Exception as exc:
        result_msg = str(exc)

    return result_msg, response_status


def _send_single_canvas_message(
    conversation_url: str,
    canvas_email_payload,
    headers: Dict,
    oauth_info,
    user_token
) -> Tuple[str, int]:
    """Send a single email to Canvas using the API.

    :param conversation_url: URL pointing to the conversation object
    :param canvas_email_payload: Email message
    :param headers: HTTP headers for the request
    :param oauth_info: Authentication info
    :return: response message, response status
    """
    result_msg = gettext('Message successfully sent')

    # Send the email through the API call
    # First attempt
    response = requests.post(
        url=conversation_url,
        data=canvas_email_payload,
        headers=headers,
        verify=True)

    response_status = response.status_code
    if (
        response.status_code == status.HTTP_401_UNAUTHORIZED
        and response.headers.get('WWW-Authenticate')
    ):
        result_msg, response_status = _refresh_and_retry_send(
            oauth_info,
            conversation_url,
            canvas_email_payload,
            user_token
        )
    elif response_status != status.HTTP_201_CREATED:
        result_msg = gettext(
            'Unable to deliver message (code {0})').format(
            response_status)

    return result_msg, response_status


class ActionEditProducerCanvasEmail(ActionOutEditProducerBase):
    """Class to serve running an email action."""

    def get_context_data(self, **kwargs) -> Dict:
        """Add conditions, conditions to clone and columns to show stats."""
        context = super().get_context_data(**kwargs)
        self.add_conditions(context)
        self.add_conditions_to_clone(context)
        self.add_columns_show_stats(context)
        return context


class ActionRunProducerCanvasEmail(ActionRunProducerBase):
    """Class to Run Canvas Email Actions."""

    # Type of event to log when running the action
    log_event = models.Log.ACTION_RUN_PERSONALIZED_CANVAS_EMAIL

    def form_valid(self, form) -> http.HttpResponse:
        """Process the VALID POST request."""
        if self.payload.get('confirm_items'):
            # Create a dictionary in the session to carry over all the
            # information to execute the next pages
            self.payload['button_label'] = gettext('Send')
            self.payload['value_range'] = 2
            self.payload['step'] = 2
            continue_url = 'action:item_filter'
        else:
            continue_url = 'action:run_done'

        self.payload.store_in_session(self.request.session)

        # Check for the CANVAS token and proceed to the continue_url
        return canvas_get_or_set_oauth_token(
            self.request,
            self.payload['target_url'],
            continue_url,
            'action:index')

    def execute_operation(
        self,
        user,
        workflow: Optional[models.Workflow] = None,
        action: Optional[models.Action] = None,
        payload: Optional[Dict] = None,
        log_item: Optional[models.Log] = None,
    ):
        """Send CANVAS emails with the action content evaluated for each row.

        Performs the submission of the emails for the given action and with the
        given subject. The subject will be evaluated also with respect to the
        rows, attributes, and conditions.
        :param user: User object that executed the action
        :param workflow: Workflow being processed
        :param action: Action from where to take the messages
        :param log_item: Log object to store results
        :param payload: Dictionary with all the parameters
        :return: Nothing
        """
        # Evaluate the action string, evaluate the subject, and get the value
        # of the email column.
        if log_item is None:
            log_item = action.log(user, self.log_event, **payload)

        item_column = action.workflow.columns.get(pk=payload['item_column'])
        action_evals = evaluate_action(
            action,
            extra_string=payload['subject'],
            column_name=item_column.name,
            exclude_values=payload.get('exclude_values', []))

        # Get the oauth info
        target_url = payload['target_url']
        if not (oauth_info := settings.CANVAS_INFO_DICT.get(target_url)):
            raise Exception(_('Unable to find OAuth Information Record'))

        # Get the token
        if not (user_token := models.OAuthUserToken.objects.filter(
            user=user,
            instance_name=target_url,
        ).first()):
            # There is no token, execution cannot proceed
            raise Exception(_('Incorrect execution due to absence of token'))

        # Create the headers to use for all requests
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(user_token.access_token),
        }

        # Create the context for the log events
        context = {'action': action.id}

        # Send the objects to the given URL
        idx = 1
        burst = oauth_info['aux_params'].get('burst')
        burst_pause = oauth_info['aux_params'].get('pause', 0)
        domain = oauth_info['domain_port']
        conversation_url = oauth_info['conversation_url'].format(domain)
        to_emails = []
        for msg_body, msg_subject, msg_to in action_evals:
            # JSON object to send. Taken from method.conversations.create in
            # https://canvas.instructure.com/doc/api/conversations.html
            canvas_email_payload = {
                'recipients[]': int(msg_to),
                'subject': msg_subject,
                'body': msg_body,
                'force_new': True}

            # Manage the bursts
            canvas_do_burst_pause(burst, burst_pause, idx)
            # Index to detect bursts
            idx += 1

            # Send the email
            result_msg, response_status = _send_single_canvas_message(
                conversation_url,
                canvas_email_payload,
                headers,
                oauth_info,
                user_token
            )
            if settings.ONTASK_TESTING:
                # Print the JSON object sent to the server
                LOGGER.info(
                    'SEND JSON(%s): %s',
                    target_url,
                    json.dumps(canvas_email_payload))
                result_msg = 'SENT TO LOGGER'
                response_status = 200

            # Log message sent
            context['subject'] = canvas_email_payload['subject']
            context['body'] = canvas_email_payload['body']
            context['from_email'] = user.email
            context['to_email'] = canvas_email_payload['recipients[]']
            context['email_sent_datetime'] = str(
                datetime.datetime.now(ZoneInfo(settings.TIME_ZONE)))
            context['response_status'] = response_status
            context['result_msg'] = result_msg
            action.log(
                user,
                models.Log.ACTION_CANVAS_EMAIL_SENT,
                **context)
            to_emails.append(msg_to)

        action.last_executed_log = log_item
        action.save(update_fields=['last_executed_log'])

        # Update excluded items in payload
        self._update_excluded_items(payload, to_emails)
