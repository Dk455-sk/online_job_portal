from django.db import models
from Accounts .models import*
from Employer .models import *
# Create your models here.
class JobApplication(models.Model):
    STATUS_CHOICE=[
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
    ]
    job=models.ForeignKey(PostJob,on_delete=models.CASCADE)
    applicant=models.ForeignKey(Register_master,on_delete=models.CASCADE)
    applied_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=30,choices=STATUS_CHOICE,default="pending")

    def __str__(self):
        return f"{self.applicant} applied for {self.job.Job_name}"


class SavedJob(models.Model):
    user = models.ForeignKey(Register_master, on_delete=models.CASCADE)
    job = models.ForeignKey(PostJob, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user} saved {self.job}"