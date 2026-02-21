from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import cheque_details,cheque_deposit
from django.db.models import Sum, Count, Q
from datetime import date
from django.contrib.auth.decorators import login_required






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

@login_required
def dashboard_home(request):

    return render(request,"dashboard.html")


@login_required
def cheque_home(request):
    if request.method == "POST":
        cheque_number = request.POST.get("cheque_no")
        cheque_date = request.POST.get("cheque_date")
        cheque_bank = request.POST.get("cheque_bank")
        account_name = request.POST.get("account_name")
        payee_name = request.POST.get("payee_name")
        cheque_amount = request.POST.get("cheque_amount")
        remarks = request.POST.get("remarks")
        
        cheque_entry = cheque_details(
            cheque_number=cheque_number,
            cheque_date=cheque_date,
            cheque_bank=cheque_bank,
            account_name=account_name,
            payee_name=payee_name,
            cheque_amount=cheque_amount,
            remarks=remarks
        )
        cheque_entry.save()
        messages.success(request, f'Cheque #{cheque_number} submitted successfully!')
        
        return redirect("cheque")
    
    # Get all cheques
    cheques = cheque_details.objects.all().order_by('-id')
    
    # Calculate stats
    today = date.today()
    today_count = cheque_details.objects.filter(cheque_date=today).count()
    cleared_count = 0
    pending_count = cheques.count()
    total_amount = cheque_details.objects.aggregate(total=Sum('cheque_amount'))['total'] or 0
    
    context = {
        'cheques': cheques,
        'today_count': today_count,
        'cleared_count': cleared_count,
        'pending_count': pending_count,
        'total_amount': total_amount,
    }
    
    return render(request, "cheque.html", context)

@login_required
def cheque_edit(request, id):
    cheque = get_object_or_404(cheque_details, id=id)
    
    if request.method == "POST":
        cheque.cheque_number = request.POST.get("cheque_no")
        cheque.cheque_date = request.POST.get("cheque_date")
        cheque.cheque_bank = request.POST.get("cheque_bank")
        cheque.account_name = request.POST.get("account_name")
        cheque.payee_name = request.POST.get("payee_name")
        cheque.cheque_amount = request.POST.get("cheque_amount")
        cheque.remarks = request.POST.get("remarks")
        cheque.save()
        
        messages.success(request, f'Cheque #{cheque.cheque_number} updated successfully!')
        return redirect("cheque")
    
    # Get all cheques for table display
    cheques = cheque_details.objects.all().order_by('-id')
    
    # Calculate stats
    today = date.today()
    today_count = cheque_details.objects.filter(cheque_date=today).count()
    cleared_count = 0
    pending_count = cheques.count()
    total_amount = cheque_details.objects.aggregate(total=Sum('cheque_amount'))['total'] or 0
    
    context = {
        'cheques': cheques,
        'today_count': today_count,
        'cleared_count': cleared_count,
        'pending_count': pending_count,
        'total_amount': total_amount,
        'edit_cheque': cheque,  # Pass the cheque being edited
        'edit_mode': True,
    }
    
    return render(request, "cheque.html", context)


def cheque_delete(request, id):
    if request.method == "POST":
        cheque = get_object_or_404(cheque_details, id=id)
    
        cheque_number = cheque.cheque_number
        cheque.delete()
        messages.success(request, f'Cheque #{cheque_number} deleted successfully!')
    return redirect("cheque")
@login_required
def deposit_home(request):
    available_cheque=cheque_details.objects.all()
    cheque_deposits=cheque_deposit.objects.all()
     
    
    return render(request,"Deposit.html",{"available_cheque":available_cheque,"cheque_deposits":cheque_deposits})


@login_required
def deposit_form(request):
    if request.method == "POST":
        cheque_number   = request.POST.get("cheque_number")
        account_name    = request.POST.get("account_name")
        cheque_bank     = request.POST.get("cheque_bank")
        cheque_amount   = request.POST.get("cheque_amount")
        deposit_bank    = request.POST.get("deposit_bank")
        branch_name     = request.POST.get("branch_name")
        deposit_date    = request.POST.get("deposit_date")
        deposit_slip_no = request.POST.get("deposit_slip_no")
        remarks         = request.POST.get("remarks")

        # Get selected cheque IDs from hidden input
        selected_ids_raw = request.POST.get("selected_cheque_ids", "")
        selected_ids = [i.strip() for i in selected_ids_raw.split(",") if i.strip()]

        # Save deposit record
        new_deposit = cheque_deposit(
            cheque_number   = cheque_number,
            account_name    = account_name,
            cheque_bank     = cheque_bank,
            cheque_amount   = cheque_amount,
            deposit_bank    = deposit_bank,
            branch_name     = branch_name,
            deposit_date    = deposit_date,
            deposit_slip_no = deposit_slip_no,
            remarks         = remarks,
        )
        new_deposit.save()

        # Delete the deposited cheques from the pending cheques table
        if selected_ids:
            cheque_details.objects.filter(id__in=selected_ids).delete()
            # ⚠️ Replace YourChequeModel with your actual model name
            # e.g. Cheque.objects.filter(id__in=selected_ids).delete()

        messages.success(request, f'Cheque #{cheque_number} deposited successfully!')

    return redirect('deposit')

def deposit_delete(request, id):
    deposit_cheque=get_object_or_404(cheque_deposit,id=id)
    deposit_cheque.delete()
    messages.success(request, f'Cheque deposit deleted successfully!')
    return redirect('deposit')



@login_required
def report_home(request):
    available_cheque=cheque_details.objects.all()
    cheque_deposits=cheque_deposit.objects.all()
     
    
    return render(request,"report.html",{"cheque_deposits":available_cheque,"cheque_deposits":cheque_deposits})



@login_required
def setting_home(request):
    return render(request,"setting.html")


def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("currentpassword")
        new_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmpassword")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('setting')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('setting')

        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, "Password changed successfully. Please log in again.")
        return redirect('login')

    return redirect('setting')
@login_required
def help_home(request): 
    return render(request,"help.html")


def logout_view(request):
    logout(request)
    return redirect('login')



def login_support(request):
    return render(request,"support_login.html")



# Create your views here.


#delete a login user

def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('login')

#deleting all data
def data_delete(request):
    
    # Delete all cheque deposits
    cheque_deposit.objects.all().delete()
    cheque_details.objects.all().delete()
    
    messages.success(request, 'All cheque data deleted successfully!')
    return redirect('dashboard')

