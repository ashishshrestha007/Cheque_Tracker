from django.shortcuts import render


def login(request):
    
    return render(request,"login.html")

def register(request):
    return render(request,"register.html")


def dashboard_home(request):
    return render(request,"dashboard.html")

def cheque_home(request):
    return render(request,"cheque.html")

def deposit_home(request):
    return render(request,"Deposit.html")

def report_home(request):
    return render(request,"report.html")

def setting_home(request):
    return render(request,"setting.html")

def help_home(request): 
    return render(request,"help.html")



# Create your views here.
