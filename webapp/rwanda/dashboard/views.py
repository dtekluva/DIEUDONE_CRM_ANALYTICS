from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from dashboard.models import *
from dashboard.models import *
import json

from django.contrib.auth import authenticate, login, logout

@csrf_exempt
def login_view(request):

    username = "admin" # request.POST['username']
    password = "19sedimat54" #request.POST['password']
    user = authenticate(request, username=username, password=password)
    

    if user is not None:
        login(request, user)
        return HttpResponse(json.dumps({"response":"True"}))
        # Redirect to a success page.

    else:
        # Return an 'invalid login' error message.
    
        return HttpResponse(json.dumps({"response":"False"}))


def logout_view(request):

    logout(request)

    return HttpResponse(json.dumps({"response":"True"}))


def get_gender_per_branch(request):

    if request.user.is_authenticated:
        
        data = Data().gender_per_branch()
        
        return HttpResponse(json.dumps({"response":data, "status": True}))

    return HttpResponse(json.dumps({"response":[], "status": False}))


def get_grouped_customers_by_month(request):

    if request.user.is_authenticated:

        data = Data().grouped_customers_by_month()
        
        return HttpResponse(json.dumps({"response":data, "status": True}))

    return HttpResponse(json.dumps({"response":[], "status": False}))


def get_number_of_loans_per_segment(request):

    if request.user.is_authenticated():

        data = Data().number_of_loans_per_segment()
        
        return HttpResponse(json.dumps({"response":data, "status": True}))

    return HttpResponse(json.dumps({"response":[], "status": False}))


def get_loan_performance_over_time(request):

    if request.user.is_authenticated():

        data = Data().loan_performance_over_time()
        
        return HttpResponse(json.dumps({"response":data, "status": True}))

    return HttpResponse(json.dumps({"response":[], "status": False}))


def get_deposits_vs_saves(request):

    if request.user.is_authenticated():
        
        data = Data().deposits_vs_saves()
        
        return HttpResponse(json.dumps({"response":data, "status": True}))

    return HttpResponse(json.dumps({"response":[], "status": False}))