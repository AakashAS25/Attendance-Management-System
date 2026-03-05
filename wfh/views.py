from datetime import date
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import WorkFromHome
from leave.models import LeaveRequest
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def request_wfh(request):

    if request.method == "POST":

        wfh_date = request.POST.get('date')
        reason = request.POST.get('reason')

        today = date.today()
        selected_date = date.fromisoformat(wfh_date)

        if selected_date < today:
            return render(request,'wfh_request.html',{
                'error':'You cannot request WFH for past dates'
            })
        
        leave_exists = LeaveRequest.objects.filter(
            user=request.user,
            start_date__lte=selected_date,
            end_date__gte=selected_date
        ).exists()

        if leave_exists:
            return render(request,'wfh_request.html',{
                'error':'Leave already requested for this date'
            })

        WorkFromHome.objects.create(
            user=request.user,
            date=date,
            reason=reason
        )

        return render(request,'wfh_request.html',{'success':'WFH request submitted'})

    return render(request,'wfh_request.html')

@login_required
def wfh_status(request):

    requests = WorkFromHome.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(
        request,
        'wfh_status.html',
        {'requests': requests}
    )

@staff_member_required
def manage_wfh(request):

    requests = WorkFromHome.objects.all().order_by('-date')

    return render(request,'manage_wfh.html',{'requests':requests})

@staff_member_required
def approve_wfh(request,id):

    req = WorkFromHome.objects.get(id=id)
    req.status = "Approved"
    req.save()

    return redirect('manage_wfh')


@staff_member_required
def reject_wfh(request,id):

    req = WorkFromHome.objects.get(id=id)
    req.status = "Rejected"
    req.save()

    return redirect('manage_wfh')

