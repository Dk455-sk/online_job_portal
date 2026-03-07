from .views import*
from django.urls import path
urlpatterns=[
    path('empprofile/',Emp_profile,name="empprofile"),
    path('jobpost/',Job_post,name="jobpost"),
    # path('jobpost/<int:id>/',Job_post,name="jobpost"),
    path('Job_list/',Job_list,name="Job_list"),
    path('jobdelete/<int:id>/', Job_delete, name='job_delete'),
]