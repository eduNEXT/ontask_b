# Generated by Django 2.2.6 on 2019-10-23 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0052_auto_20191024_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view',
            name='description_text',
            field=models.CharField(blank=True, default='', max_length=2048, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='view',
            name='name',
            field=models.CharField(max_length=512, verbose_name='name'),
        ),
    ]
