from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from attendance.models import Attendance
from leave.models import LeaveRequest
from wfh.models import WorkFromHome
from datetime import date


def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            return redirect('dashboard')

        else:
            return render(request,'login.html',{'error':'Invalid credentials'})

    return render(request,'login.html')
@login_required
def dashboard(request):

    if request.user.is_superuser:
        return redirect('admin_dashboard')

    return render(request,'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):

    today = date.today()

    total_employees = User.objects.count()

    today_attendance = Attendance.objects.filter(
        date=today
    ).count()

    pending_leaves = LeaveRequest.objects.filter(
        status="Pending"
    ).count()

    pending_wfh = WorkFromHome.objects.filter(
        status="Pending"
    ).count()

    context = {
        "total_employees": total_employees,
        "today_attendance": today_attendance,
        "pending_leaves": pending_leaves,
        "pending_wfh": pending_wfh
    }

    return render(request, "admin_dashboard.html", context)
