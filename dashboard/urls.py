"""rwanda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'),
    path('login_view', views.login_view, name='login_view'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('get_gender_per_branch/<str:branch>', views.get_gender_per_branch, name='get_gender_per_branch'),
    path('get_deposits_vs_saves/<str:branch>', views.get_deposits_vs_saves, name='get_deposits_vs_saves'),
    path('get_loans_summary/<str:branch>', views.get_loans_summary, name='get_loans_summary'),
    path('get_loan_performance_over_time/<str:branch>', views.get_loan_performance_over_time, name='get_loan_performance_over_time'),
    path('get_number_of_loans_per_segment/<str:branch>', views.get_number_of_loans_per_segment, name='get_number_of_loans_per_segment'),
    path('get_grouped_customers_by_month/<str:branch>', views.get_grouped_customers_by_month, name='get_grouped_customers_by_month'),
    path('post_units/<str:device>/<str:units>/<str:voltage>/<str:current>', views.post_units, name='post_units'),
    path('check_new_units/<str:device>', views.check_new_units, name='check_new_units'),
    path('relay_status/<str:device>/', views.relay_status, name='relay_status'),
    path('get_device_details/<str:device>/', views.get_device_details, name='get_device_details')

]