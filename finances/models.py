from __future__ import unicode_literals
from authentication.models import Account
from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_bill = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

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


class IncomeType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __unicode__(self):
        return self.name


def get_default_income_type():
    return IncomeType.objects.get(name="salary")


def get_default_categories():
    return Category.objects.filter(is_default=True)


class UserProfile(models.Model):
    account = models.OneToOneField(Account)
    default_categories = models.ManyToManyField(Category)
    income_type = models.ForeignKey(IncomeType, default=get_default_income_type)
    hourly_income = models.FloatField(default=0.0)
    monthly_income = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.account.get_full_name()


class Dashboard(models.Model):
    profile = models.ForeignKey(UserProfile)
    period = models.ForeignKey(Period)
    net_income = models.FloatField(null=True)
    net_hourly_pay = models.FloatField(default=0.0)
    hours_worked = models.FloatField(default=0.0)
    expected_cash_saved = models.FloatField(default=0.0, null=True)
    interpolated_cash_saved = models.FloatField(default=0.0, null=True)
    actual_cash_saved = models.FloatField(default=0.0, null=True)
    avg_cash_spent_per_day = models.FloatField(default=0.0, null=True)

    def __unicode__(self):
        return self.account.get_full_name() + ": " + self.period.name()


class Expense(models.Model):
    dashboard = models.ForeignKey(Dashboard)
    category = models.ForeignKey(Category)
    description = models.CharField(max_length=512)
    amount = models.FloatField(default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.dashboard.account.get_full_name() + " " \
               + str(self.amount) + " " + self.category.name + " " + self.date


class Budget(models.Model):
    dashboard = models.ForeignKey(Dashboard)
    category = models.ForeignKey(Category)
    amount = models.FloatField(default=0.0)
    expenses = models.ManyToManyField(Expense)


def get_num_hours_this_month(period=None):
    return 12


@receiver(post_save, sender=Dashboard)
def add_default_bills_and_budgets_to_dashboard(**kwargs):
    dashboard = kwargs.get('instance')
    profile = dashboard.profile
    created = kwargs.get('created')
    if created:
        # create bills (as expenses) for this dashboard
        for category in profile.default_categories.filter(is_bill=True):
            Expense.objects.create(dashboard=dashboard, category=category)

        for category in profile.default_categories.filter(is_bill=False):
            Budget.objects.create(dashboard=dashboard, category=category)

        if profile.income_type.name == "hourly":
            dashboard.hours_worked = get_num_hours_this_month(dashboard.period)
            dashboard.net_hourly_pay = profile.hourly_income
            dashboard.net_income = dashboard.net_hourly_pay * dashboard.hours_worked
            dashboard.save()
        else:
            dashboard.net_income = profile.monthly_income
            dashboard.save()


        # if profile.income_type.name == "hourly":
        #     dashboard.


@receiver(post_save, sender=Account)
def create_userprofile_on_account_create(**kwargs):
    created = kwargs.get('created')
    if created:
        account = kwargs.get('instance')
        profile = UserProfile(account=account)
        profile.save()

@receiver(post_save, sender=UserProfile)
def add_default_categories_to_user_profile(**kwargs):
    created = kwargs.get('created')
    profile = kwargs.get('instance')
    if created:
        cats = Category.objects.filter(is_default=True)
        for cat in cats:
            profile.default_categories.add(cat.id)


