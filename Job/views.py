from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from Accounts.models import *
from Employer.models import *

def jobseekeer_applications(request):
    email=request.session.get("email")
    if not email:
        return redirect("login")
    user=get_object_or_404(Register_master,email=email)
    applications=JobApplication.objects.filter(applicant=user)
    return render(request,"jobseeker_applications.html",{"applications":applications})

def employer_applications(request):

    email = request.session.get("email")
    if not email:
        return redirect("login")

    user = get_object_or_404(Register_master, email=email)
    employer = get_object_or_404(Emp_profile_update,email=user)

    applications = JobApplication.objects.filter(
        job__employee=employer
    ).select_related("applicant", "job").prefetch_related(
        "applicant__jobseeker_profile_set"
    )

    # Accept / Reject
    if request.method == "POST":
        app_id = request.POST.get("app_id")
        action = request.POST.get("action")

        application = get_object_or_404(
            JobApplication,
            id=app_id,
            job__employee=employer
        )

        if application.status == "Pending":
            if action == "accept":
                application.status = "Accepted"
            elif action == "reject":
                application.status = "Rejected"
            application.save()

        return redirect("employer_applications")

    return render(request, "employer_applications.html", {
        "applications": applications
    })