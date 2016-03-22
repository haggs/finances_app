# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 06:12
from __future__ import unicode_literals

from django.db import migrations
from ..models import Period
from datetime import datetime
from ..helpers import get_period


def create_12_periods(apps, schema_editor):
    now = datetime.now()

    month = now.month
    year = now.year
    for i in range(24):
        get_period(datetime(month=month, year=year, day=1))
        month = month - 1
        if month < 1:
            month = 12
            year = year - 1


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0002_auto_20160320_2054'),
    ]

    operations = [
        migrations.RunPython(create_12_periods)
    ]
