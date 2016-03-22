# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='actual_cash_saved',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='avg_cash_spent_per_day',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='expected_cash_saved',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='interpolated_cash_saved',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='net_income',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]