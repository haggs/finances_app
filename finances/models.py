from __future__ import unicode_literals
from authentication.models import Account
from django.db import models
from datetime import datetime
from workdays import networkdays
from django.db.models.signals import post_save
from django.dispatch import receiver


class Period(models.Model):
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __unicode__(self):
        return self.name()

    def name(self):
        return self.month + " " + self.year

    def get_num_hours(self):
        return networkdays(self.start_date, self.end_date)


class IncomeType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    is_default = models.BooleanField(False)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    account = models.OneToOneField(Account)
    income_type = models.ForeignKey(IncomeType)
    hourly_income = models.FloatField(default=0.0)
    monthly_income = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.account.get_full_name()

    def get_default_categories(self):
        return self.objects.filter(is_default=True, profile=self)

    def save(self, *args, **kwargs):
        if not self.id:
            self.income_type = IncomeType.objects.get(is_default=True)
            cats = [
                Category(name="Rent", is_bill=True, is_default=True),
                Category(name="Car Loan", is_bill=True, is_default=True),
                Category(name="Car Insurance", is_bill=True, is_default=True),
                Category(name="Electric Bill", is_bill=True, is_default=True),

                Category(name="Restaurants & Bars", is_bill=False, is_default=True),
                Category(name="Shopping", is_bill=False, is_default=True),
                Category(name="Rent", is_bill=False, is_default=True),
                Category(name="Misc.", is_default_new_expense=True, is_bill=False, is_default=True)
            ]
            for cat in cats:
                cat.save()

            retval = super(UserProfile, self).save(*args, **kwargs)

            for cat in cats:
                cat.profile = self
                cat.save()

            return retval
        return super(UserProfile, self).save(*args, **kwargs)


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    is_bill = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    is_default_new_expense = models.BooleanField(default=False)
    profile = models.ForeignKey(UserProfile, null=True)

    def __unicode__(self):
        return self.name


class Dashboard(models.Model):
    profile = models.ForeignKey(UserProfile, null=True)
    period = models.ForeignKey(Period)
    net_income = models.FloatField(null=True)
    net_hourly_pay = models.FloatField(default=0.0)
    hours_worked = models.FloatField(default=0.0)
    expected_cash_saved = models.FloatField(default=0.0, null=True)
    interpolated_cash_saved = models.FloatField(default=0.0, null=True)
    actual_cash_saved = models.FloatField(default=0.0, null=True)
    avg_cash_spent_per_day = models.FloatField(default=0.0, null=True)

    def __unicode__(self):
        return self.period.name() + " " + elf.account.get_full_name()

    def save(self, *args, **kwargs):
        if not self.id:
            retval = super(Dashboard, self).save(*args, **kwargs)
            profile = self.profile
            for category in Category.objects.filter(is_bill=True, profile=profile, is_default=True):
                Expense.objects.create(dashboard=self, category=category)

            for category in Category.objects.filter(is_bill=False, profile=profile, is_default=True):
                Budget.objects.create(dashboard=self, category=category)

            if profile.income_type.name == "Hourly":
                self.hours_worked = self.period.get_num_hours()
                self.net_hourly_pay = profile.hourly_income
                self.net_income = self.net_hourly_pay * self.hours_worked
            else:
                self.net_income = profile.monthly_income
            self.save()
            return retval
        return super(Dashboard, self).save(*args, **kwargs)


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

    def __unicode__(self):
        return self.category.name + " " + self.dashboard.__unicode__()


@receiver(post_save, sender=Account)
def create_userprofile_on_account_create(**kwargs):
    created = kwargs.get('created')
    if created:
        account = kwargs.get('instance')
        profile = UserProfile(account=account, income_type=IncomeType.objects.get(is_default=True))
        profile.save()


