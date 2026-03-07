from django.db import models

# Create your models here.
class Register_master(models.Model):
    ROLE_CHOICE=(
        ('jobseeker','Jobseeker'),
        ('employer',('Employer')),    
    )
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    mobile=models.CharField(max_length=15)
    address=models.TextField()
    rolename=models.CharField(max_length=20,choices=ROLE_CHOICE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-({self.rolename})"
    


class Jobseeker_Profile(models.Model):
    user=models.ForeignKey(Register_master,on_delete=models.CASCADE)
    skills=models.TextField()
    experience_years=models.IntegerField()
    qualification=models.CharField(max_length=100)
    resume=models.FileField(upload_to='resumes/')
    Image=models.FileField(upload_to='Profile_Image/',blank=True,null=True)
    Id_proof=models.FileField(upload_to="Idproofs/",blank=True,null=True)
    preffered_location=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.user}-{self.skills}"


    