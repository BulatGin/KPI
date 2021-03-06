# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KPITest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='taskcontext',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
