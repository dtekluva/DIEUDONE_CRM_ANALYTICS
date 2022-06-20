import imp
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import *
import json
from dashboard.predict import test_model
from dashboard.sendemail import Mail


@csrf_exempt
def test(request):

    data = request.GET.get("text", "Happy")
    print(data)
    response = test_model(input_data=data)

    return CORS(HttpResponse(json.dumps({"response":"True", "data":response}))).allow_all()


@csrf_exempt
def send_mail(request):

    email = request.GET.get("email", "")
    lga = request.GET.get("lga", "")
    
    Mail().send([email], lga)

    return CORS(HttpResponse(json.dumps({"response":"True", "data":"mail sent"}))).allow_all()



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