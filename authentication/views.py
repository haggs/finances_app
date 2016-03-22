from django.shortcuts import render
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate as django_authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import Account,  SignupKey
from django.core import validators
from django import forms
from .forms import RegistrationForm, LoginForm


def register(request):
    if request.method == "POST":
        errors = []
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            new_account = form.save()
            new_account = django_authenticate(email=request.POST['email'], password=request.POST['password'])
            django_login(request, new_account)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'authentication/register.html', {'form': form})
    form = RegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        errors = []
        form = LoginForm(data=request.POST)
        if form.is_valid():
            account = django_authenticate(email=request.POST['email'], password=request.POST['password'])
            if account and account.is_active:
                django_login(request, account)
                return HttpResponseRedirect('/')
            else:
                errors.append("Login failed")
                return render(request, 'authentication/login.html', {'form': form, 'errors': errors})
        else:
            errors.append("Form invalid")
            return render(request, 'authentication/login.html', {'form': form, 'errors': errors})
    else:
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')