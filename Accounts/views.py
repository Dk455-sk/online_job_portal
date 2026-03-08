from django.shortcuts import render,redirect
from .forms import registerform,loginform
from Employer.models import PostJob, Emp_profile_update
from .models import Register_master,Jobseeker_Profile
from Job .models import JobApplication,PostJob,SavedJob
from django.contrib import messages
from django.views.decorators.cache import never_cache
# Create your views here.
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

def job_detail(request, id):

    job = get_object_or_404(PostJob, id=id)

    if request.method == "POST":

        email = request.session.get("email")

        if not email:
            return JsonResponse({
                "status": "error",
                "message": "Please login first"
            })

        user = Register_master.objects.get(email=email)

        # prevent duplicate apply
        already_applied = JobApplication.objects.filter(
            applicant=user,
            job=job
        ).exists()

        if already_applied:
            return JsonResponse({
                "status": "error",
                "message": "You already applied for this job"
            })

        JobApplication.objects.create(
            applicant=user,
            job=job,
            status="Pending",
        )

        return JsonResponse({
            "status": "success",
            "message": "Job applied successfully"
        })

    return render(request, "job_detail.html", {
        "job": job
    })
def remove_saved_job(request):

    if request.method == "POST":

        saved_id = request.POST.get("saved_id")

        try:
            saved_job = SavedJob.objects.get(id=saved_id)
            saved_job.delete()

            return JsonResponse({
                "status": "success",
                "message": "Saved job removed successfully"
            })

        except SavedJob.DoesNotExist:

            return JsonResponse({
                "status": "error",
                "message": "Saved job not found"
            })

def saved_jobs(request):

    email = request.session.get("email")

    # Check if user logged in
    if not email:
        messages.warning(request, "please login to see more job")
        return redirect("login")

    try:
        user = Register_master.objects.get(email=email)
    except Register_master.DoesNotExist:
        messages.error(request, "User not found. Please login again.")
        return redirect("login")

    saved = SavedJob.objects.filter(user=user)

    return render(request, "saved_jobs.html", {"saved": saved})


# @login_required
def applyjob_list(request):

    jobs = PostJob.objects.all()

    # FILTERING
    keyword = request.GET.get("keyword")
    location = request.GET.get("location")
    job_type = request.GET.get("type")

    if keyword:
        jobs = jobs.filter(
            Q(Job_name__icontains=keyword) |
            Q(Job_Skill__icontains=keyword) |
            Q(employee__company_Name__icontains=keyword)
        )

    if location:
        jobs = jobs.filter(Location__icontains=location)

    if job_type:
        jobs = jobs.filter(Job_Type=job_type)

    if request.method == "POST":

        email = request.session.get("email")

        if not email:
            return JsonResponse({
                "status": "error",
                "message": "Please login first"
            })

        user = Register_master.objects.get(email=email)

        job_id = request.POST.get("job_id")
        action = request.POST.get("action")

        job = PostJob.objects.get(id=job_id)

        if action == "apply":

            if JobApplication.objects.filter(job=job, applicant=user).exists():
                return JsonResponse({
                    "status": "warning",
                    "message": "You already applied for this job"
                })

            JobApplication.objects.create(job=job, applicant=user,status="Pending")

            return JsonResponse({
                "status": "success",
                "message": "Job applied successfully"
            })

        elif action == "save":

            if SavedJob.objects.filter(job=job, user=user).exists():
                return JsonResponse({
                    "status": "warning",
                    "message": "Job already saved"
                })

            SavedJob.objects.create(job=job, user=user)

            return JsonResponse({
                "status": "success",
                "message": "Job saved successfully"
            })

    return render(request, "applyjob_list.html", {"edata": jobs})
            

def jobseeker_profile(request):

    email = request.session.get("email")

    if not email:
        return redirect("login")

    try:
        user = Register_master.objects.get(email=email)
    except Register_master.DoesNotExist:
        messages.error(request, "User not found")
        return redirect("login")

    try:
        profile = Jobseeker_Profile.objects.get(user=user)
    except Jobseeker_Profile.DoesNotExist:
        profile = None

    if request.method == "POST":

        # Update user info
        user.name = request.POST.get("name")
        user.password = request.POST.get("pwd")
        user.mobile = request.POST.get("mobile")
        user.address = request.POST.get("adds")
        user.save()

        skills = request.POST.get("skills")
        experience = request.POST.get("experience_years")
        qualification = request.POST.get("qualification")
        location = request.POST.get("preffered_location")

        resume = request.FILES.get("resume")
        photo = request.FILES.get("profile_photo")
        idproof = request.FILES.get("Id_proof")

        if profile:

            profile.skills = skills
            profile.experience_years = experience
            profile.qualification = qualification
            profile.preffered_location = location

            if resume:
                profile.resume = resume

            if photo:
                profile.Image = photo

            if idproof:
                profile.Id_proof = idproof

            profile.save()

        else:

            profile = Jobseeker_Profile.objects.create(
                user=user,
                skills=skills,
                experience_years=experience,
                qualification=qualification,
                preffered_location=location,
                resume=resume,
                Image=photo,
                Id_proof=idproof
            )

        messages.success(request, "Profile updated successfully")
        return redirect("jobseeker_profile")

    context = {
        "data": user,
        "profile": profile
    }

    return render(request, "jobseeker_profile.html", context)




def viewdata(request):
    ob=Register_master.objects.all()
    return render(request,"viewdata.html",{"data":ob})

@never_cache
def employer_dashboard(request):

    # Get logged-in employer's email from session
    email = request.session.get("email")
    if not email:
        return redirect("login")  # redirect if not logged in

    try:
        ob = Register_master.objects.get(email=email)
        profile = Emp_profile_update.objects.get(email=ob)
    except (Register_master.DoesNotExist, Emp_profile_update.DoesNotExist):
        profile = None

    # Fetch all jobs posted by this employer
    if profile:
        jobs = PostJob.objects.filter(employee=profile)
    else:
        jobs = PostJob.objects.none()  # empty queryset if no profile

    return render(request, "employer_dashboard.html", {
        "ename": ob.name,
        "edata": jobs
    })


def jobseeker_dashboard(request):

    email = request.session.get("email")

    if not email:
        return redirect("login")

    user = Register_master.objects.get(email=email)

    # latest jobs
    jobs = PostJob.objects.all().order_by("-id")[:6]

    # statistics
    applied_count = JobApplication.objects.filter(applicant=user).count()
    saved_count = SavedJob.objects.filter(user=user).count()

    context = {
        "jname": user.name,
        "jobs": jobs,
        "applied_count": applied_count,
        "saved_count": saved_count,
    }

    return render(request, "jobseeker_dashboard.html", context)

def Register(request):

    if request.method == "POST":

        formobj = registerform(request.POST)

        if formobj.is_valid():
            formobj.save()

            return JsonResponse({
                "status": "success",
                "message": "Registration successful"
            })

        else:
            return JsonResponse({
                "status": "error",
                "message": "Registration failed"
            })

    formobj = registerform()

    return render(request, "register.html", {"form": formobj})



def Login(request):

    if request.method == "POST":

        formobj = loginform(request.POST)

        email = formobj.data.get("email")
        password = formobj.data.get("password")

        try:
            ob = Register_master.objects.get(email=email, password=password)

            request.session["name"] = ob.name
            request.session["email"] = ob.email

            if ob.rolename == "jobseeker":
                return JsonResponse({
                    "status": "success",
                    "redirect": reverse("jobseeker_dashboard")
                })

            elif ob.rolename == "employer":
                return JsonResponse({
                    "status": "success",
                    "redirect": reverse("employer_dashboard")
                })

        except Register_master.DoesNotExist:

            return JsonResponse({
                "status": "error",
                "message": "Invalid username or password"
            })

    formobj = loginform()

    return render(request, "login.html", {"form": formobj})

def Logout(request):
    request.session.flush()   # Clears all session data
    return redirect('home') 