# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 04:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import finances.models
from ..models import UserProfile, Category
from authentication.models import Account


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0005_auto_20160323_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_categories',
            field=models.ManyToManyField(default=finances.models.get_default_categories, to='finances.Category'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='income_type',
            field=models.ForeignKey(default=finances.models.get_default_income_type, on_delete=django.db.models.deletion.CASCADE, to='finances.IncomeType'),
        )
    ]
