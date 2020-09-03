from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from dashboard.models import *
import json

from django.contrib.auth import authenticate, login, logout

@csrf_exempt
def login_view(request):

    if request.is_ajax:

        token = Token().authenticate(request)

        return CORS(HttpResponse(json.dumps({"response":"True", "status": token }))).allow_all()
        # Redirect to a success page.

    else:
        # Return an 'invalid login' error message.
    
        return CORS(HttpResponse(json.dumps({"response":"False"}))).allow_all()

@csrf_exempt
def logout_view(request):

    logout(request)

    return CORS(HttpResponse(json.dumps({"response":"True"}))).allow_all()

@csrf_exempt
def get_gender_per_branch(request, branch):
    
    token = Token().authorize(request)

    if token.get("authenticated"):
        
        data = Data(request, branch).gender_per_branch()
        
        return CORS(HttpResponse(json.dumps({"response":data, "status": True}))).allow_all()

    return CORS(HttpResponse(json.dumps({"response":[], "status": False, "content":token}))).allow_all()

@csrf_exempt
def get_grouped_customers_by_month(request, branch):
    
    token = Token().authorize(request)

    if token.get("authenticated"):

        data = Data(request, branch).grouped_customers_by_month()
        
        return CORS(HttpResponse(json.dumps({"response":data, "status": True}))).allow_all()

    return CORS(HttpResponse(json.dumps({"response":[], "status": False, "content":token}))).allow_all()

@csrf_exempt
def get_number_of_loans_per_segment(request, branch):
    
    token = Token().authorize(request)

    if token.get("authenticated"):

        data = Data(request, branch).number_of_loans_per_segment()
        grouped = Data(request, branch).loans_amount_per_segment()
        
        return CORS(HttpResponse(json.dumps({"response":{"summarized":data, "grouped":grouped}, "status": True}))).allow_all()

    return CORS(HttpResponse(json.dumps({"response":[], "status": False, "content":token}))).allow_all()

@csrf_exempt
def get_loan_performance_over_time(request, branch):

    token = Token().authorize(request)

    if token.get("authenticated"):

        data = Data(request, branch).loan_performance_over_time()
        
        return CORS(HttpResponse(json.dumps({"response":data, "status": True}))).allow_all()

    return CORS(HttpResponse(json.dumps({"response":[], "status": False, "content":token}))).allow_all()

@csrf_exempt
def get_deposits_vs_saves(request, branch):

    token = Token().authorize(request)

    if token.get("authenticated"):
        
        data = Data(request, branch).deposits_vs_saves()
        
        return CORS(HttpResponse(json.dumps({"response":data, "status": True}))).allow_all()

    return CORS(HttpResponse(json.dumps({"response":[], "status": False, "content":token}))).allow_all()

@csrf_exempt
def get_loans_summary(request, branch):

    token = Token().authorize(request)

    if token.get("authenticated"):
        
        data = Data(request, branch).general_perfomance_of_loans()
        
        return CORS(HttpResponse(json.dumps({"response":data, "status": True}))).allow_all()

    return CORS(HttpResponse(json.dumps({"response":[], "status": False, "content":token}))).allow_all()

@csrf_exempt
def post_units(request, device, units, voltage, current):

    device = Device.objects.filter(device_id = device)


    if device.exists():        

        device = device[0]
        device.total_kwh = device.total_kwh + (device.last_kwh - units)
        device.save()

        Reading.objects.create(device = device, voltage = voltage, current = current, total_kwh = device.total_kwh, time = datetime.datetime.now())

        return CORS(HttpResponse(1)).allow_all()


    return CORS(HttpResponse(0)).allow_all()

@csrf_exempt
def check_units(request, device):

    device = Device.objects.filter(device_id = device)
    print(device[0])
    new_kwh = 2

    if device.exists():        

        new_kwh = device[0].new_kwh
        device[0].new_kwh = 0
        device[0].save()

        return CORS(HttpResponse(new_kwh)).allow_all()


    return CORS(HttpResponse(new_kwh)).allow_all()

@csrf_exempt
def relay_status(request, device):
    
    device = Device.objects.filter(device_id = device)
    relay_status = 2

    if device.exists():
        relay_status = int(device[0].relay_status)

    return CORS(HttpResponse(relay_status)).allow_all()


@csrf_exempt
class CORS(HttpResponse):
    def allow_all(self, auth = "", status_code = 200):

        self["Access-Control-Allow-Origin"] = "*"
        self["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        self["Access-Control-Max-Age"] = "1000"
        self["Access-Control-Allow-Headers"] = "*"
        self["Authorization"] = "Token-" + str(auth)
        self["Content-Type"] = "application/json"

        self.status_code = status_code

        return self