import sys
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json, datetime, random, secrets
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

customers_file_name= './datasets/Customers_1.csv'
deposit_file_name= './datasets/Deposit_1.csv'
loan_file_name= './datasets/LoanData_1.csv'
savings_file_name= './datasets/Savingdata_1.csv'

class Data:

    global customers_file_name
    global deposit_file_name
    global loan_file_name
    global savings_file_name

    customers_file = pd.read_csv(customers_file_name)
    deposit_file = pd.read_csv(deposit_file_name)
    loan_file = pd.read_csv(loan_file_name)
    savings_file = pd.read_csv(savings_file_name)


    def gender_per_branch(self):

        cust_per_branch = self.customers_file.groupby("Branch").count().to_dict()["Gender"]
        cust_per_branch

        gender_per_branch = pd.pivot_table(self.customers_file, values='Nationality', index=['Gender'], columns=['Branch'], aggfunc=np.count_nonzero)
        
        return gender_per_branch.to_dict()


    def grouped_customers_by_month(self):

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

        loans_per_segment_count = self.loan_file.groupby("Segment").count().reset_index()[["Segment","Clined ID"]]
        
        return loans_per_segment_count.to_dict("list")

    def loans_amount_per_segment(self):

        loans_per_segment_sum = self.loan_file.groupby("Segment").sum().reset_index()[["Segment","Disbursement", "outstanding"]]
        
        return loans_per_segment_sum.to_dict("list")

    def general_perfomance_of_loans(self):
        
        loans_per_segment_sum = self.loan_file.sum(numeric_only=True).reset_index()

        return loans_per_segment_sum.to_dict("records")

    def loan_performance_over_time(self):

        loan_file_copy = self.loan_file[:]


        loan_file_copy["Approval_date"] = pd.to_datetime(self.loan_file["Approval.Date"])
        loan_file_copy = loan_file_copy.sort_values(by=['Approval_date'])


        loan_file_copy["month"] = loan_file_copy["Approval_date"].dt.month_name().astype("str").str.slice(stop = 3) + "/" + loan_file_copy["Approval_date"].dt.year.astype("str")
        loan_file_copy = loan_file_copy.sort_values("Approval_date")

        loan_peformance_per_time = loan_file_copy.groupby(loan_file_copy.month, sort = False).sum()[["Approved.Amount", "Disbursement", "Balance", "paid_principal", "unpaid_principal", "outstanding"]]
        return loan_peformance_per_time.to_dict("index")

    def deposits_vs_saves(self):

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


        grouped_saves_deps = full_deps_saves.groupby(full_deps_saves["date_str"], sort = False).sum()

        return grouped_saves_deps.to_dict("index")




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

            token_exists = True
            self.token = self.generate_token()
        
        super(Token, self).save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    def add_token(self, request = False):
        if request:
            current_tokens = self.user.token_set.all()

            self.device_name = request.META.get("COMPUTERNAME", "")
            self.user_agent = request.META.get("HTTP_USER_AGENT", "")
        self.is_active = True
        self.save(is_new = True)
    
    @staticmethod
    def verify_token(request):

        user_id  = request.META.get("HTTP_PHONE")

        try:
            user = User.objects.get(username = user_id)
        except:
            return False

        token = request.META.get("HTTP_AUTHORIZATION")
        
        token_exists = user.token_set.filter(token = token).exists()

        if token_exists:
            return {"authenticated": True, "user": user}
        else:
            return False

    @staticmethod
    def authenticate(username, password, request):

        user = authenticate(username = username , password = password)
        # print(user, username, username.lower())

        if user and (user.username == username): #allows user to login using username
                # No backend authenticated the credentials

                if True:

                    user = User.objects.get(id=user.id)
                    login(request, user)
                    Token(user = user).add_token(request)

                    return {"success" : True, "message":"Not yet Verified"}

                else:
                    return {"success" : False, "message":"Not yet Verified"}

        else: return {"success" : False, "message":"Incorrect details"}

    @staticmethod
    def authenticate_from_verify(user, request):

        if user.is_verified:

            user = User.objects.get(id=user.id)
            login(request, user)
            Token(user = user).add_token(request)

            return True

        else: return False