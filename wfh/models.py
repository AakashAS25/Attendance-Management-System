from django.db import models
from django.contrib.auth.models import User

class WorkFromHome(models.Model):

    STATUS = (
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    reason = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
class Meta:
    unique_together = ('user','date')