from django.db import models
from django.contrib.auth.models import User

class LeaveRequest(models.Model):

    LEAVE_TYPE = (
        ('Paid', 'Paid Leave'),
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
    )

    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE)

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.leave_type}"