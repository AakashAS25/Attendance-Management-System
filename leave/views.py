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

        LeaveRequest.objects.create(
            user=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )

        return render(request,'leave_request.html',{'success':'Leave request submitted'})

    return render(request,'leave_request.html')

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