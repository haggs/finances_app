from __future__ import unicode_literals
from authentication.models import Account
from django.db import models
from datetime import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_bill = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Period(models.Model):
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def name(self):
        return self.month + " " + self.year

    def __unicode__(self):
        return self.name()


class Dashboard(models.Model):
    account = models.ForeignKey(Account)
    period = models.ForeignKey(Period)
    net_income = models.FloatField(null=True)
    expected_cash_saved = models.FloatField(null=True)
    interpolated_cash_saved = models.FloatField(null=True)
    actual_cash_saved = models.FloatField(null=True)
    avg_cash_spent_per_day = models.FloatField(null=True)

    def __unicode__(self):
        return self.account.get_full_name() + ": " + self.period.name()


class Expense(models.Model):
    dashboard = models.ForeignKey(Dashboard)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length=512)
    amount = models.FloatField(default=0.00)
    date = models.DateTimeField(auto_now_add=True)


