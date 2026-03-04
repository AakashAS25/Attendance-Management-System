from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_wfh, name='request_wfh'),
    path('status/', views.wfh_status, name='wfh_status'),
    path('manage/', views.manage_wfh, name='manage_wfh'),
    path('approve/<int:id>/', views.approve_wfh, name='approve_wfh'),
    path('reject/<int:id>/', views.reject_wfh, name='reject_wfh'),
]