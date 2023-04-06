# Generated by Django 2.2.13 on 2020-08-16 03:24

import copy

from django.db import migrations
from ontask.models import Filter


def set_condition_workflow(apps, schema_editor):
    """Separate conditions and filters into two tables."""

    Condition = apps.get_model('ontask', 'Condition')
    for citem in Condition.objects.all():
        citem.workflow = citem.action.workflow
        citem.save()


def separate_conditions_and_filters(apps, schema_editor):
    """Separate conditions and filters into two tables."""

    Condition = apps.get_model('ontask', 'Condition')
    Filter = apps.get_model('ontask', 'Filter')
    for citem in Condition.objects.filter(is_filter=True):
        new_item = Filter.objects.create(
            formula=copy.deepcopy(citem.formula),
            formula_text=citem.formula_text,
            n_rows_selected=citem.n_rows_selected,
            workflow=citem.action.workflow,
            action_ref=citem.action,
            description_text=citem.description_text)
        new_item.columns.set(citem.columns.all())
        new_item.save()

    Condition.objects.filter(is_filter=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0036_auto_20230330_1140'),
    ]

    operations = [
        migrations.RunPython(code=set_condition_workflow),
        migrations.RunPython(code=separate_conditions_and_filters)]
