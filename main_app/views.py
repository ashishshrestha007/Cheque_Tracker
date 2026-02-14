from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("staffId")
        password = request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            messages.error(request,"Invalid username or password")
            return redirect("login")


    return render(request,"login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("fullName")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirmPassword")
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user=User.objects.create_user(
            username=username,
            email=email,
            password=password,
            
        )
        messages.success(request, "Account created successfully")
        return redirect('login')
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
