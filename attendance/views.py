from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Attendance
from leave.models import LeaveRequest
from wfh.models import WorkFromHome

@login_required
def mark_attendance(request):

    today = date.today()

    leave = LeaveRequest.objects.filter(
        user=request.user,
        start_date__lte=today,
        end_date__gte=today,
        status="Approved"
    )

    if leave.exists():
        return render(request,'attendance.html',
        {'error':'You are on leave today'})

    wfh = WorkFromHome.objects.filter(
        user=request.user,
        date=today,
        status="Approved"
    )

    if wfh.exists():
        status = "WFH"

    already_marked = Attendance.objects.filter(user=request.user, date=today).exists()

    if request.method == "POST":

        if already_marked:
            return render(request,'attendance.html',{'error':'Attendance already marked today'})

        status = request.POST.get('status')

        Attendance.objects.create(
            user=request.user,
            date=today,
            status=status
        )
        

        return render(request,'attendance.html',{'success':'Attendance marked successfully'})

    return render(request,'attendance.html',{'already_marked':already_marked})

@login_required
def attendance_history(request):

    records = Attendance.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(
        request,
        'attendance_history.html',
        {'records':records}
    )