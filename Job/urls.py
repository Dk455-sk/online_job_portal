from Job.views import*
from django.urls import path
urlpatterns=[
    path('employer_applications/',employer_applications,name="employer_applications"),
    path('jobseeker_applications/',jobseekeer_applications,name="jobseeker_applications"),
    # path('job/<int:id>/',job_detail,name="job_detail")
]