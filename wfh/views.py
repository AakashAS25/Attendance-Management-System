from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import WorkFromHome

@login_required
def request_wfh(request):

    if request.method == "POST":

        date = request.POST.get('date')
        reason = request.POST.get('reason')

        WorkFromHome.objects.create(
            user=request.user,
            date=date,
            reason=reason
        )

        return render(request,'wfh_request.html',{'success':'WFH request submitted'})

    return render(request,'wfh_request.html')