"""finances_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login, logout
from views import (
    home,
    view_dashboard,
    view_preferences,
    search_default_bill,
    search_default_budget,
    add_category,
    remove_default_category
)

urlpatterns = [
    url(r'^$', home),
    url(r'(?P<period_id>\d+)/$', view_dashboard),
    url(r'^preferences/$', view_preferences),
    url(r'^api/v1/search_default_bill/$', search_default_bill),
    url(r'^api/v1/search_default_budget/$', search_default_budget),
    url(r'^api/v1/add_category/$', add_category),
    url(r'^api/v1/remove_default_category/$', remove_default_category),
]
