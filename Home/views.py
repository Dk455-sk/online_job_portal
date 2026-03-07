from django.shortcuts import render
from Employer.models import PostJob,Emp_profile_update
from Accounts.models import Register_master

def home(request):

    # Latest jobs
    jobs = PostJob.objects.all().order_by("-id")[:6]

    # Total counts
    total_jobs = PostJob.objects.count()
    total_companies = Emp_profile_update.objects.count()
    total_jobseekers = Register_master.objects.filter(rolename="jobseeker").count()

    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,
        "total_companies": total_companies,
        "total_jobseekers": total_jobseekers
    }

    return render(request, "home.html", context)