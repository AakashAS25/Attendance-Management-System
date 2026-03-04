from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_leave, name='request_leave'),
    path('status/', views.leave_status, name='leave_status'),
    path('manage/', views.manage_leaves, name='manage_leaves'),
    path('approve/<int:id>/', views.approve_leave, name='approve_leave'),
    path('reject/<int:id>/', views.reject_leave, name='reject_leave'),
]