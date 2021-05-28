import sys
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json, datetime, random, secrets
from rwanda import settings
from django.db.models import Count
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

customers_file_name= './datasets/Customers_1.csv'
deposit_file_name= './datasets/Deposit_1.csv'
loan_file_name= './datasets/LoanData_1.csv'
savings_file_name= './datasets/Savingdata_1.csv'


def from_sql(table):
    import pymysql
    # global username, password, db

    connection =pymysql.connect(host=settings.HOST,
                                user=settings.USERNAME,
                                password=settings.PASSWORD,
                                db= settings.DB,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:

        with connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM {table}"
            
            cursor.execute(sql)
            result = cursor.fetchall()

            return pd.DataFrame(result)

    finally:
        connection.close()

class Data:

    global customers_file_name
    global deposit_file_name
    global loan_file_name
    global savings_file_name

    # if settings.DATA_FROM_DB:

    def __init__(self, request, branch):
        print(json.loads(request.body))
        self.period = json.loads(request.body).get("period", "0/0").split("/")
        self.start = self.period[0]
        self.end = self.period[1]
        self.branch = branch

        if self.branch == "OVERVIEW":
            self.customers_file = from_sql("Customers_1")
            self.deposit_file = from_sql("Deposit_1")
            self.loan_file = from_sql("LoanData_1")
            self.savings_file = from_sql("Savingdata_1")
        
        elif self.branch != "OVERVIEW":
            customers_file = from_sql("Customers_1")
            self.customers_file = customers_file[customers_file.Branch.str.contains(self.branch)]
            self.deposit_file = from_sql("Deposit_1")[from_sql("Deposit_1").Branch.str.contains(self.branch)]
            self.loan_file = from_sql("LoanData_1")[from_sql("LoanData_1").Branch.str.contains(self.branch)]
            self.savings_file = from_sql("Savingdata_1")[from_sql("Savingdata_1").Branch.str.contains(self.branch)]

    # else:

    #     customers_file = pd.read_csv(customers_file_name)
    #     deposit_file = pd.read_csv(deposit_file_name)
    #     loan_file = pd.read_csv(loan_file_name)
    #     savings_file = pd.read_csv(savings_file_name)


    def gender_per_branch(self):

        if self.start != '0':

            self.customers_file["JoinDate"] = pd.to_datetime(self.customers_file["JoinDate"])
            self.customers_file["JoinDate"] = self.customers_file[(self.customers_file['JoinDate'] > self.start) & (self.customers_file['JoinDate'] <= self.end)]

        cust_per_branch = self.customers_file.groupby("Branch").count().to_dict()["Gender"]

        gender_per_branch = pd.pivot_table(self.customers_file, values='Nationality', index=['Gender'], columns=['Branch'], aggfunc=np.count_nonzero)
        
        return gender_per_branch.to_dict()


    def grouped_customers_by_month(self):

        if self.start != '0':

            self.customers_file["JoinDate"] = pd.to_datetime(self.customers_file["JoinDate"])
            self.customers_file = self.customers_file[(self.customers_file['JoinDate'] > self.start) & (self.customers_file['JoinDate'] <= self.end)]
        
        self.customers_file["JoinDate"] = pd.to_datetime(self.customers_file["JoinDate"])
        self.customers_file["JoinMonth"] = self.customers_file.JoinDate.dt.month_name().str.slice(stop = 3) + "-" + self.customers_file.JoinDate.dt.year.astype("str")
        customers_file_sorted = self.customers_file.sort_values(by=['JoinDate'])
        grouped_customers_by_month = customers_file_sorted.groupby("JoinMonth")

        data = {}

        for key, group in grouped_customers_by_month:
            
            group_data = group.groupby("Gender").count()["Branch"].to_dict()
            if "C" not in group_data:
                group_data["C"] = 0
            elif "M" not in group_data:
                group_data["M"] = 0
            elif "F" not in group_data:
                group_data["F"] = 0
                
            data[key] = group_data

        return data


    # ## LOANS SECTION
    def number_of_loans_per_segment(self):

        if self.start != '0':

            self.loan_file["Approval.Date"] = pd.to_datetime(self.loan_file["Approval.Date"])
            self.loan_file = self.loan_file[(self.loan_file['Approval.Date'] > self.start) & (self.loan_file['Approval.Date'] <= self.end)]

        loans_per_segment_count = self.loan_file.groupby("Segment").count().reset_index()[["Segment","Clined ID"]]
        loans_per_segment_count.columns = ["Segment","NumberOfLoans"]
        
        return loans_per_segment_count.to_dict("list")

    def loans_amount_per_segment(self):

        if self.start != '0':

            self.loan_file["Approval.Date"] = pd.to_datetime(self.loan_file["Approval.Date"])
            self.loan_file = self.loan_file[(self.loan_file['Approval.Date'] > self.start) & (self.loan_file['Approval.Date'] <= self.end)]

        self.loan_file[["Approved.Amount", "outstanding","Disbursement", "paid_principal"]] = self.loan_file[["Approved.Amount", "outstanding","Disbursement", "paid_principal"]].astype("int")
        loans_per_segment_sum = self.loan_file.groupby("Segment").sum().reset_index()[["Segment","Disbursement", "outstanding"]]
        
        return loans_per_segment_sum.to_dict("list")

    def general_perfomance_of_loans(self):
        
        if self.start != '0':

            self.loan_file["Approval.Date"] = pd.to_datetime(self.loan_file["Approval.Date"])
            self.loan_file = self.loan_file[(self.loan_file['Approval.Date'] > self.start) & (self.loan_file['Approval.Date'] <= self.end)]
        
        self.loan_file[["Approved.Amount", "outstanding","Disbursement", "paid_principal"]] = self.loan_file[["Approved.Amount", "outstanding","Disbursement", "paid_principal"]].astype("int")

        loans_per_segment_sum = self.loan_file[["Approved.Amount", "outstanding","Disbursement", "paid_principal"]].sum(numeric_only=True).reset_index()

        return loans_per_segment_sum.to_dict("records")

    def loan_performance_over_time(self):

        if self.start != '0':

            self.loan_file["Approval.Date"] = pd.to_datetime(self.loan_file["Approval.Date"])
            self.loan_file = self.loan_file[(self.loan_file['Approval.Date'] > self.start) & (self.loan_file['Approval.Date'] <= self.end)]

        loan_file_copy = self.loan_file[:]

        loan_file_copy["Approval_date"] = pd.to_datetime(self.loan_file["Approval.Date"])
        loan_file_copy[["Approved.Amount", "Disbursement", "Balance", "paid_principal", "unpaid_principal", "outstanding"]] = loan_file_copy[["Approved.Amount", "Disbursement", "Balance", "paid_principal", "unpaid_principal", "outstanding"]].astype(int)
        loan_file_copy = loan_file_copy.sort_values(by=['Approval_date'])


        loan_file_copy["month"] = loan_file_copy["Approval_date"].dt.month_name().astype("str").str.slice(stop = 3) + "/" + loan_file_copy["Approval_date"].dt.year.astype("str")
        loan_file_copy = loan_file_copy.sort_values("Approval_date")

        loan_peformance_per_time = loan_file_copy.groupby(loan_file_copy.month, sort = False).sum()[["Approved.Amount", "Disbursement", "Balance", "paid_principal", "unpaid_principal", "outstanding"]]
        return loan_peformance_per_time.to_dict("index")

    def deposits_vs_saves(self):

        if self.start != '0':

            self.deposit_file["dateofdeposit"] = pd.to_datetime(self.deposit_file["dateofdeposit"])
            self.deposit_file = self.deposit_file[(self.deposit_file['dateofdeposit'] > self.start) & (self.deposit_file['dateofdeposit'] <= self.end)]
            
            self.savings_file["savingDate"] = pd.to_datetime(self.savings_file["savingDate"])
            self.savings_file = self.savings_file[(self.savings_file['savingDate'] > self.start) & (self.savings_file['savingDate'] <= self.end)]

        self.deposit_file["deposit_date"] = pd.to_datetime(self.deposit_file["dateofdeposit"])
        deposit_file_copy = self.deposit_file[:]
        deposit_file_copy = self.deposit_file.sort_values(by=['deposit_date'])


        self.savings_file["saving_date"] = pd.to_datetime(self.savings_file["savingDate"])
        savings_file_copy = self.savings_file.sort_values(by=['savingDate'])

        trimmed_saves = savings_file_copy[["Segment", "savingDate", "Branch", "SavingAmount"]].rename(columns = {"savingDate":"trans_date"})
        trimmed_deps = deposit_file_copy[["Segment", "dateofdeposit", "Branch", "depositamount"]].rename(columns = {"dateofdeposit":"trans_date"})

        full_deps_saves = pd.concat([trimmed_saves, trimmed_deps])


        full_deps_saves = full_deps_saves.fillna(0)


        full_deps_saves["trans_date"] = pd.to_datetime(full_deps_saves["trans_date"])

        full_deps_saves = full_deps_saves.sort_values(by = "trans_date")



        full_deps_saves["date_str"] = full_deps_saves.trans_date.dt.month_name().str.slice(stop = 3) + "-" + full_deps_saves.trans_date.dt.year.astype("str") 

        full_deps_saves["depositamount"] = full_deps_saves["depositamount"].astype("int")
        grouped_saves_deps = full_deps_saves.groupby(full_deps_saves["date_str"], sort = False).sum()

        return grouped_saves_deps.to_dict("index")


class Attempt(models.Model):

    name = models.CharField(max_length=200, null=True, blank = True) #mac address preferably
    value  = models.CharField(max_length=200, null=True, blank = True)
    time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def new_attempt(name, value):

        status = False
        print(value, "282021", value == "282021")

        if value == "282021":
            status = True

        attempt = Attempt(name = name, value = value, status = status)

        attempt.save()


    def display_all_attempts():

        attempts = set(list(map(lambda attempt: attempt.name, Attempt.objects.all())))
        
        all_attempts = []

        for name in attempts:
            attempt = list(Attempt.objects.filter(name = name))[-1]

            all_attempts.append({
                "time": attempt.time.strftime("%m/%d/%Y, %H:%M:%S"),
                "name": attempt.name,
                "value": attempt.value,
                "status": attempt.status,
                "correct": Attempt.objects.filter(status = True)[0].time.strftime("%m/%d/%Y, %H:%M:%S") if Attempt.objects.filter(status = True, name = name).exists() else 0,
                "attempts": Attempt.objects.filter(name = attempt.name).count()
            })

        return all_attempts




class Token(models.Model):

    device_id = models.CharField(max_length=200, null=True, blank = True) #mac address preferably
    username  = models.CharField(max_length=200, null=True, blank = True)
    device_name = models.CharField(max_length=200, null=True, blank = True)
    user_agent  = models.CharField(max_length=200, null=True, blank = True)
    token     = models.CharField(max_length=200, null=True, blank = True)
    user      = models.ForeignKey(User, on_delete= models.CASCADE)
    is_active = models.BooleanField(default = False)

    def generate_token(self):
        return secrets.token_urlsafe(40)

    def save(self, *args, **kwargs):

        if kwargs.get("is_new"):

            self.token = self.generate_token()
        
        super(Token, self).save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    def add_token(self):

        self.user.token_set.all().delete()
        self.is_active = True
        self.save(is_new = True)


        return self.token
    
    @staticmethod
    def authorize(request):
        
        data = json.loads(request.body)

        token  = data["auth"]
        username  = data["username"]

        try:
            user = User.objects.get(username = username)
        except:
            return {"authenticated": False, "user": "username does not exist"}

        
        token_exists = user.token_set.filter(token = token).exists()

        if token_exists:
            return {"authenticated": True, "user": user}
        else:
            return {"authenticated": False, "user": "bad token"}

    @staticmethod
    def authenticate(request):

        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(username = username , password = password)

        if user and (user.username == username): #allows user to login using username
                # No backend authenticated the credentials

                if True:

                    user = User.objects.get(id=user.id)
                    login(request, user)
                    token = Token(user = user).add_token()

                    return {"success" : True, "token": token, "message":"Not yet Verified"}

                else:
                    return {"success" : False, "message":"Not yet Verified"}

        else: return {"success" : False, "message":"Incorrect details"}


class Device(models.Model):

    user      = models.ForeignKey(User, on_delete= models.CASCADE, default = 1)
    device_id = models.CharField(max_length=200, null=True, blank = True) #mac address preferably
    ownername  = models.CharField(max_length=200, null=True, blank = True)
    device_name = models.CharField(max_length=200, null=True, blank = True)
    total_kwh = models.FloatField(max_length=200, null=True, blank = True)
    last_kwh = models.FloatField(max_length=200, null=True, blank = True)
    new_kwh = models.FloatField(max_length=200, null=True, blank = True)
    relay_status = models.BooleanField(default = False)

    def __str__(self):
        return self.ownername

class Reading(models.Model):

    device   = models.ForeignKey(Device, on_delete= models.CASCADE)
    voltage  = models.FloatField(max_length=200, null=True, blank = True)
    current  = models.FloatField(max_length=200, null=True, blank = True)
    total_kwh= models.FloatField(max_length=200, null=True, blank = True)
    kwh_used = models.FloatField(max_length=200, null=True, blank = True)
    time     = models.DateTimeField(max_length=200, null=True, blank = True)
    relay_status = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)

    def __str__(self):
        return self.device.device_id