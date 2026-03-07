from Accounts.views import* 
from django.urls import path
urlpatterns=[
    path('register/',Register,name="register"),
    path('login/',Login,name="login"),
    path('employer_dashboard/',employer_dashboard,name="employer_dashboard"),
    path('jobseeker_dashboard/',jobseeker_dashboard,name="jobseeker_dashboard"),
    path('jobseeker_profile/',jobseeker_profile,name="jobseeker_profile"),
    path('logout/', Logout, name="logout"),
    path('viewdata/',viewdata,name="viewdata"),
    path('applyjob_list',applyjob_list,name="applyjob_list"),
    path("saved_jobs/",saved_jobs, name="saved_jobs"),
    path("remove_saved_job/",remove_saved_job, name="remove_saved_job"),
    path("job/<int:id>/",job_detail, name="job_detail"),
]