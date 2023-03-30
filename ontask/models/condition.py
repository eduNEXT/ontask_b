# -*- coding: utf-8 -*-

"""Condition Model."""
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ontask.dataops import formula as dataops_formula, sql
from ontask.models.column import Column
from ontask.models.workflow import Workflow
from ontask.models.common import (
    CHAR_FIELD_LONG_SIZE, CHAR_FIELD_MID_SIZE, CreateModifyFields,
    NameAndDescription,
)
from ontask.models.logs import Log


class ConditionBase(CreateModifyFields):
    """Object to storing a formula.

    The object also encodes:
    - list of columns in the support of the formula
    - number of rows for which the formula is true

    @DynamicAttrs
    """

    formula = JSONField(
        default=dict,
        blank=True,
        null=True,
        verbose_name=_('formula'))

    formula_text = models.CharField(
        max_length=CHAR_FIELD_LONG_SIZE,
        default='',
        blank=True,
        null=True,
        verbose_name=_('formula text'))

    # Number or rows selected by the expression
    n_rows_selected = models.IntegerField(
        verbose_name=_('Number of rows selected'),
        default=-1,
        name='n_rows_selected',
        blank=False,
        null=False)

    def update_n_rows_selected(self, column=None, filter_formula=None):
        """Calculate the number of rows for which condition is true.

        Given a condition update the number of rows
        for which this condition will have true result.

        :param column: Column that has changed value (None when unknown)
        :param filter_formula: Formula provided by another filter condition
        and to take the conjunction with the condition formula.
        :return: Boolean. True if number has changed
        """
        if column and column not in self.columns.all():
            # The column is not part of this condition. Nothing to do
            return

        formula = self.formula
        if filter_formula:
            # There is a formula to add to the condition, create a conjunction
            formula = {
                'condition': 'AND',
                'not': False,
                'rules': [filter_formula, self.formula],
                'valid': True,
            }

        old_count = self.n_rows_selected
        self.n_rows_selected = sql.get_num_rows(
            self.action.workflow.get_data_frame_table_name(),
            formula,
        )
        self.save(update_fields=['n_rows_selected'])

        return old_count != self.n_rows_selected

    def get_formula_text(self):
        """Translate the formula to plain text.

        Return the content of the formula in a string that is human readable
        :return: String
        """
        if not self.formula_text:
            self.formula_text = dataops_formula.evaluate(
                self.formula,
                dataops_formula.EVAL_TXT)
            self.save(update_fields=['formula_text'])
        return self.formula_text

    class Meta:
        """Make the class abstract."""

        abstract = True


class Condition(NameAndDescription, ConditionBase):
    """Object to storing a Condition that is used in an action.

    @DynamicAttrs
    """

    workflow = models.ForeignKey(
        Workflow,
        db_index=True,
        null=False,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
        related_name='conditions')

    action = models.ForeignKey(
        'Action',
        db_index=True,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='conditions')

    # Set of columns that appear in this condition
    columns = models.ManyToManyField(
        Column,
        verbose_name=_('Columns present in this condition'),
        related_name='conditions')

    @property
    def is_filter(self) -> bool:
        """Identify as filter"""
        return False

    def __str__(self) -> str:
        """Render string."""
        return self.name

    def log(self, user, operation_type: str, **kwargs):
        """Log the operation with the object."""
        payload = {
            'id': self.id,
            'name': self.name,
            'action': self.action.name,
            'formula': self.get_formula_text(),
            'n_rows_selected': self.n_rows_selected,
            'workflow_id': self.action.workflow.id}

        payload.update(kwargs)
        return Log.objects.register(
            user,
            operation_type,
            self.action.workflow,
            payload)

    class Meta:
        """Define unique criteria and ordering.

        The unique criteria here is within the action and the name.
        """

        unique_together = ('action', 'name')
        ordering = ['name']


class Filter(ConditionBase):
    """Object to storing a Filter that is used in an action or a view.

    @DynamicAttrs
    """

    workflow = models.ForeignKey(
        Workflow,
        db_index=True,
        null=False,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
        related_name='filters')

    description_text = models.CharField(
        max_length=CHAR_FIELD_LONG_SIZE,
        default='',
        blank=True,
        verbose_name=_('description'),
    )

    # Set of columns that appear in this condition
    columns = models.ManyToManyField(
        Column,
        verbose_name=_('Columns present in this filter'),
        related_name='filters')

    @property
    def is_filter(self) -> bool:
        """Identify as filter"""
        return True

    class Meta:
        """No definitions required here (so far)"""

        pass
