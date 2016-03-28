from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import Expense, Period, UserProfile, Category, Budget, IncomeType
from .helpers import get_period, get_dashboard
from json import dumps


@login_required
def home(request):
    now = datetime.now()
    period = get_period(now)
    return HttpResponseRedirect('/' + str(period.id) + '/')


@login_required
def view_dashboard(request, period_id=None):
    profile = UserProfile.objects.get(account=request.user)
    dashboard = get_dashboard(period_id=period_id, profile_id=profile.id)
    expenses = Expense.objects.filter(dashboard=dashboard)
    periods = Period.objects.order_by('-start_date')

    this_month = get_period(datetime.now())

    sidebar_elements = []

    current_year = this_month.start_date.year

    # Get periods used by sidebar
    for period in periods:
        if period == this_month:
            continue
        if period.start_date.year != current_year:
            sidebar_elements.append({'type': 'year', 'label': period.start_date.year})
            current_year = period.start_date.year
        sidebar_elements.append({'type': 'month', 'label': period.month, 'id': period.id})

    bills = expenses.filter(category__is_bill=True)
    budgets = Budget.objects.filter(dashboard=dashboard)

    expense_table = {}
    current_date = this_month.start_date
    while current_date <= this_month.end_date:
        expense_table[current_date] = {'name': current_date.strftime("%-m/%-d")}
        current_date += timedelta(days=1)

    data = {'dashboard': dashboard,
            'expenses': expenses,
            'bills': bills,
            'budgets': budgets,
            'periods': periods,
            'this_month': this_month,
            'sidebar_elements': sidebar_elements,
            'total_bills': bills.aggregate(Sum('amount')).get('amount__sum'),
            'total_budgets': budgets.aggregate(Sum('amount')).get('amount_sum'),
            'expense_table': expense_table
           }

    return render(request, 'finances/dashboard.html', data)


@login_required
@ensure_csrf_cookie
def view_preferences(request):
    profile = UserProfile.objects.get(account=request.user)

    if request.method == 'POST':
        if 'action' not in request.POST:
            return JsonResponse({'success': True})
        if request.POST['action'] == 'apply_changes':
            income_type = IncomeType.objects.get(id=request.POST['income_type_id'])
            profile.income_type = income_type
            if income_type.name == "Hourly":
                profile.hourly_income = float(request.POST['hourly_income'])
            else:
                profile.monthly_income = float(request.POST['monthly_income'])
            profile.save()
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
        'bills': Category.objects.filter(profile=profile, is_default=True, is_bill=True).order_by('name'),
        'budgets': Category.objects.filter(profile=profile, is_default=True, is_bill=False).order_by('name'),
        'income_types': IncomeType.objects.all(),
        'periods': Period.objects.order_by('-start_date'),
    }

    return render(request, 'finances/preferences.html', data)


@login_required
def add_expense(request):
    return HttpResponseRedirect('/')


@login_required
def search_default_bill(request):
    profile = UserProfile.objects.get(account=request.user)
    bills = Category.objects.filter(profile=profile,
                                    is_bill=True,
                                    is_default=False,
                                    name__contains=request.GET['term']
                                   )

    values = []
    for bill in bills:
        values.append({
            'id': bill.id,
            'label': bill.name,
            'name': bill.name
        })

    test_name = Category.objects.filter(name=request.GET['term'])

    if request.GET['term'].replace(" ", "") != "" and not test_name.exists():
        values.append({
            'id': 0,
            'label': "Create new bill:  " + request.GET['term'],
            'name': "Create new bill:  " + request.GET['term'],
        })

    return HttpResponse(dumps(values), 'application/json')


@login_required
def add_category(request):
    cat_id = int(request.POST.get('id', 0))
    is_bill = int(request.POST.get('is_bill', 0))
    is_default = int(request.POST.get('is_default', 0))
    name = request.POST.get('name', 'New category')

    profile = UserProfile.objects.get(account=request.user)

    cat = Category.objects.filter(Q(profile=profile) & (Q(id=cat_id) | Q(name=name)))

    if cat.exists():
        cat = cat.get()
        if cat.is_default == is_default and cat.is_bill == is_bill:
            return JsonResponse({'success': 0})
    else:
        cat = Category(profile=profile, name=name)

    cat.is_bill = is_bill
    cat.is_default = is_default
    cat.save()
    return JsonResponse({'success': 1, 'id': cat.id, 'name': cat.name})


@login_required
def remove_default_bill(request):
    profile = UserProfile.objects.get(account=request.user)
    bill = Category.objects.get(profile=profile, id=request.POST['id'])
    bill.is_default = False
    bill.save()
    return JsonResponse({'success': 1})
