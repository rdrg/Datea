from django.db import models
from django.contrib.auth.models import User
from datea_report.models import Report

# Create your models here.

class ReportVote(models.Model):
    
    created = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(default=1)
    author = models.ForeignKey(User, related_name="votes")
    report = models.ForeignKey(Report, related_name="votes")