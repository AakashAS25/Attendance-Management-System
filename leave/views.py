from datetime import date
from wfh.models import WorkFromHome
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import LeaveRequest


@login_required
def request_leave(request):

    if request.method == "POST":

        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        today = date.today()

        start_date_obj = date.fromisoformat(start_date)
        end_date_obj = date.fromisoformat(end_date)

        if start_date_obj < today or end_date_obj < today:
            return render(request,'leave_request.html',{
                'error':'You cannot request leave for past dates'
            })

        if end_date_obj < start_date_obj:
            return render(request,'leave_request.html',{
                'error':'End date cannot be before start date'
            })
        
        wfh_exists = WorkFromHome.objects.filter(
            user=request.user,
            date__gte=start_date_obj,
            date__lte=end_date_obj
        ).exists()

        if wfh_exists:
            return render(request,'leave_request.html',{
                'error':'WFH already requested during this period'
            })

        LeaveRequest.objects.create(
            user=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        

        return render(request,'leave_request.html',{'success':'Leave request submitted'})

    return render(request,'leave_request.html',{'today':date.today()})

@login_required
def leave_status(request):

    leaves = LeaveRequest.objects.filter(
        user=request.user
    ).order_by('-start_date')

    return render(
        request,
        'leave_status.html',
        {'leaves': leaves}
    )

@staff_member_required
def manage_leaves(request):

    leaves = LeaveRequest.objects.all().order_by('-start_date')

    return render(request,'manage_leaves.html',{'leaves':leaves})

@staff_member_required
def approve_leave(request, id):

    leave = LeaveRequest.objects.get(id=id)
    leave.status = "Approved"
    leave.save()

    return redirect('manage_leaves')


@staff_member_required
def reject_leave(request, id):

    leave = LeaveRequest.objects.get(id=id)
    leave.status = "Rejected"
    leave.save()

    return redirect('manage_leaves')