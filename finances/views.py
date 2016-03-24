from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime
from .models import Expense, Period, UserProfile, Category
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
@ensure_csrf_cookie
def view_preferences(request):
    profile = UserProfile.objects.get(account=request.user)

    if request.method == 'POST':
        if 'action' not in request.POST:
            return JsonResponse({'success': True})
        if request.POST['action'] == 'delete_default_bill':
            bill = Category.objects.get(id=request.POST['id'])
            profile.default_categories.remove(bill)
            return JsonResponse({'success': True})
        if request.POST['action'] == 'add_default_bill':
            bill = Category.objects.get(id=request.POST['id'])
            profile.default_categories.add(bill)
            return JsonResponse({'success': True})

    data = {
        'profile': profile,
        'bills': Category.objects.filter(is_bill=True).order_by('id'),
    }

    return render(request, 'finances/preferences.html', data)


@login_required
def add_expense(request):
    return HttpResponseRedirect('/')


