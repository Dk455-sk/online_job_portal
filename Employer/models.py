from django.db import models
from Accounts.models import*
# Create your models here.
class Emp_profile_update(models.Model):
    email=models.ForeignKey(Register_master,on_delete=models.CASCADE)
    empid=models.CharField(max_length=100,unique=True)
    Designation=models.CharField(max_length=30)
    job_profile=models.CharField(max_length=100)
    company_Name=models.CharField(max_length=40)
    company_details=models.TextField()
    company_address=models.TextField()
    company_website=models.URLField()

    def __str__(self):
        return f"{self.email}-{self.Designation}"


class PostJob(models.Model):
    Choice=(
        ("FullTime",'Fultime'),
        ("PartTime",'Part-tiem'),
        ("Contract",'Contract'),
        ("Internship",'Internship')
    )
    employee=models.ForeignKey(Emp_profile_update,on_delete=models.CASCADE)
    Job_name=models.CharField(max_length=30)
    Job_Type=models.CharField(max_length=30,choices=Choice)
    Job_Skill=models.CharField(max_length=30)
    Experience=models.IntegerField()
    Qualification=models.CharField(max_length=30)
    Location=models.CharField(max_length=30)
    vacancies=models.CharField(max_length=30)
    opening_date=models.DateField()
    closing_date=models.DateField()
    def __str__(self):
        return f"{self.Job_name}-({self.Experience})"