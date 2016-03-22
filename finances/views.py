from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Expense, Period
from .helpers import get_period, get_dashboard


@login_required
def home(request):
    now = datetime.now()
    period = get_period(now)
    return HttpResponseRedirect('/' + str(period.id) + '/')

@login_required
def view_dashboard(request, period_id=None):

    dashboard = get_dashboard(period_id=period_id, account_id=request.user.id)
    expenses = Expense.objects.filter(dashboard=dashboard)
    periods = Period.objects.order_by('-start_date')

    this_month = get_period(datetime.now())

    sidebar_elements = []

    current_year = this_month.start_date.year

    for period in periods:
        if period == this_month:
            continue
        if period.start_date.year != current_year:
            sidebar_elements.append({'type': 'year', 'label': period.start_date.year})
            current_year = period.start_date.year
        sidebar_elements.append({'type': 'month', 'label': period.month, 'id': period.id})

    data = {'dashboard': dashboard,
            'expenses': expenses,
            'periods': periods,
            'this_month': this_month,
            'sidebar_elements': sidebar_elements
           }

    return render(request, 'finances/dashboard.html', data)

@login_required
def add_expense(request):
    return HttpResponseRedirect('/')


