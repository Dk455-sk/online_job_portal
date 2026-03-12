from django.shortcuts import render,redirect
from Accounts.models import *
from .models import Emp_profile_update,PostJob
from django.shortcuts import  get_object_or_404
# Create your views here.
def Job_list(request):
    email = request.session.get("email")

    try:
        ob = Register_master.objects.get(email=email)
    except Register_master.DoesNotExist:
        return render(request, "job_list.html", {
            'edata': [],
            'cdata': None,
            'error': "Your account was not found. Please login again."
        })

    # Safe profile fetch
    profile_qs = Emp_profile_update.objects.filter(email=ob)
    if profile_qs.exists():
        profile = profile_qs.first()
        jobemail = PostJob.objects.filter(employee=profile)
    else:
        profile = None
        jobemail = PostJob.objects.none()

    return render(request, "job_list.html", {
        'edata': jobemail,
        'cdata': profile,
        'error': None
    })
# 
def Job_post(request, id=None):
    email = request.session.get("email")
    ob = Register_master.objects.get(email=email)

    try:
        profile = Emp_profile_update.objects.get(email=ob)
    except Emp_profile_update.DoesNotExist:
        profile = None

    job = None
    if id:
        job = get_object_or_404(PostJob, id=id)

    if request.method == "POST":
        if job:
            # Editing existing job
            job.Job_name = request.POST.get("jname")
            job.Job_Type = request.POST.get("jtype")
            job.Job_Skill = request.POST.get("jskill")  # <-- match form input
            job.Experience = request.POST.get("exp")
            job.Qualification = request.POST.get("qualify")
            job.Location = request.POST.get("loc")
            job.vacancies = request.POST.get("vacancy")
            job.opening_date = request.POST.get("odate")
            job.closing_date = request.POST.get("cdate")
            job.save()
        else:
            # Creating new job
            PostJob.objects.create(
                employee=profile,
                Job_name=request.POST.get("jname"),
                Job_Type=request.POST.get("jtype"),
                Job_Skill=request.POST.get("jskill"),  # <-- match form input
                Experience=request.POST.get("exp"),
                Qualification=request.POST.get("qualify"),
                Location=request.POST.get("loc"),
                vacancies=request.POST.get("vacancy"),
                opening_date=request.POST.get("odate"),
                closing_date=request.POST.get("cdate")
            )
        return redirect("Job_list")

    return render(request, "job_post.html", {
        "empdata": profile,
        "jdata": job
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import PostJob, Emp_profile_update, Register_master

def Job_list(request):
    # Get logged-in user's email
    email = request.session.get("email")
    if not email:
        return redirect("login")  # redirect if not logged in

    try:
        user = Register_master.objects.get(email=email)
    except Register_master.DoesNotExist:
        return render(request, "job_list.html", {
            'edata': [],
            'cdata': None,
            'error': "Your account was not found. Please login again."
        })

    # Fetch employer profile
    profile_qs = Emp_profile_update.objects.filter(email=user)
    profile = profile_qs.first() if profile_qs.exists() else None

    # Fetch jobs for this employer
    jobs = PostJob.objects.filter(employee=profile) if profile else PostJob.objects.none()

    return render(request, "job_list.html", {
        'edata': jobs,
        'cdata': profile,
        'error': None
    })


def Job_delete(request, id):
    email = request.session.get("email")
    if not email:
        return redirect("login")

    # Get the logged-in employer profile
    user = get_object_or_404(Register_master, email=email)
    profile = get_object_or_404(Emp_profile_update, email=user)

    # Fetch the specific job that belongs to this employer
    job = get_object_or_404(PostJob, id=id, employee=profile)

    # Delete only this job
    job.delete()
    return redirect("Job_list")  # go back to job list





def Emp_profile(request):
    email = request.session.get("email")
    if not email:
        return redirect("login")
    ob = Register_master.objects.get(email=email)

    # Try to get the profile, else None
    try:
        profile = Emp_profile_update.objects.get(email=ob)
    except Emp_profile_update.DoesNotExist:
        profile = None

    if request.method == "POST":
        # Update basic user info
        ob.name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        if pwd:
            ob.password = pwd
        ob.mobile = request.POST.get("mobile")
        ob.address = request.POST.get("adds")
        ob.save()

        if profile:
            # Update existing profile
            profile.empid = request.POST.get("empid")
            profile.Designation = request.POST.get("desg")  # fix typo
            profile.job_profile = request.POST.get("jprofile")
            profile.company_Name = request.POST.get("cname")
            profile.company_details = request.POST.get("cdetails")
            profile.company_address = request.POST.get("caddress")
            profile.company_website = request.POST.get("cweb")
            profile.save()
        else:
            # Create new profile
            Emp_profile_update.objects.create(
                email = ob,
                empid = request.POST.get("empid"),
                Designation = request.POST.get("desg"),  # fix typo
                job_profile = request.POST.get("jprofile"),
                company_Name = request.POST.get("cname"),
                company_details = request.POST.get("cdetails"),
                company_address = request.POST.get("caddress"),
                company_website = request.POST.get("cweb"),
            )

        return redirect("empprofile")  

    return render(request, "emp_profile.html", {"data": ob, "profile": profile})