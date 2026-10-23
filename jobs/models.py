from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)

    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.IntegerField()
    status = models.CharField(max_length=100)
    applied_date = models.DateField()
