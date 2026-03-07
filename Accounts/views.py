from django.shortcuts import render,redirect
from .forms import registerform,loginform
from Employer.models import PostJob, Emp_profile_update
from .models import Register_master,Jobseeker_Profile
from Job .models import JobApplication,PostJob,SavedJob
from django.contrib import messages
# Create your views here.
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def job_detail(request, id):

    job = get_object_or_404(PostJob, id=id)

    return render(request, "job_detail.html", {
        "job": job
    })

def remove_saved_job(request):

    if request.method == "POST":

        saved_id = request.POST.get("saved_id")

        try:
            saved_job = SavedJob.objects.get(id=saved_id)
            saved_job.delete()
            messages.success(request, "Saved job removed successfully!")

        except SavedJob.DoesNotExist:
            messages.warning(request, "Saved job not found")

    return redirect("saved_jobs")

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

@login_required
def applyjob_list(request):

    jobs = PostJob.objects.all()

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

        job_id = request.POST.get("job_id")
        action = request.POST.get("action")

        job = PostJob.objects.get(id=job_id)

        user_email = request.session["email"]
        if not user_email:
            return redirect("login")
        user_obj = Register_master.objects.get(email=user_email)

        # APPLY JOB
        if action == "apply":

            if JobApplication.objects.filter(job=job, applicant=user_obj).exists():
                messages.warning(request, "You already applied for this job")
            else:
                JobApplication.objects.create(job=job, applicant=user_obj)
                messages.success(request, "Job Applied Successfully!")

        # SAVE JOB
        elif action == "save":

            if SavedJob.objects.filter(job=job, user=user_obj).exists():
                messages.warning(request, "Job already saved")
            else:
                SavedJob.objects.create(job=job, user=user_obj)
                messages.success(request, "Job Saved Successfully!")

        return redirect("applyjob_list")

    return render(request, "applyjob_list.html", {"edata": jobs})
            

def jobseeker_profile(request):
    email = request.session.get("email")
    if not email:
        return redirect("login")  # Optional safety check
    user = Register_master.objects.get(email=email)

    try:
        profile = Jobseeker_Profile.objects.get(user=user)
    except Jobseeker_Profile.DoesNotExist:
        profile = None

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.password = request.POST.get("pwd")
        user.mobile = request.POST.get("mobile")
        user.address = request.POST.get("adds")
        user.save()

        if profile:
            profile.skills = request.POST.get("skills")
            profile.experience_years = request.POST.get("experience_years")
            profile.qualification = request.POST.get("qualification")
            profile.preffered_location= request.POST.get("preffered_location")

            if request.FILES.get("resume"):
                profile.resume = request.FILES.get("resume")

            if request.FILES.get("Id_proof"):
                profile.Id_proof = request.FILES.get("Id_proof")

            profile.save()

        else:
            Jobseeker_Profile.objects.create(
                user=user,
                skills=request.POST.get("skills"),
                experience_years=request.POST.get("experience_years"),
                qualification=request.POST.get("qualification"),
                preffered_location=request.POST.get("preffered_location"),
                resume=request.FILES.get("resume"),
                Id_proof=request.FILES.get("Id_proof"),
            )

        return redirect("jobseeker_profile")

    return render(request, "jobseeker_profile.html", {"data": user, "profile": profile})




def viewdata(request):
    ob=Register_master.objects.all()
    return render(request,"viewdata.html",{"data":ob})

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
# def jobseeker_dashboard(request):
#     name=request.session.get("name")
#     return render(request,"jobseeker_dashboard.html",{"jname":name})
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
    msg=""
    if request.method=="POST":
        formobj=registerform(request.POST)
        if formobj.is_valid():
            formobj.save()
            msg="Register success...."
        else:
            msg="Register fail..."
    formobj=registerform()
    
            
    return render(request,"register.html",{"form":formobj,"msg":msg})



def Login(request):
    if request.method=="POST":
        formobj=loginform(request.POST)
        email=formobj.data.get("email")
        password=formobj.data.get("password")
        try:
            ob=Register_master.objects.get(email=email,password=password)
            request.session["name"]=ob.name
            request.session["email"]=ob.email

            if ob.rolename=="jobseeker":
                return redirect("jobseeker_dashboard")

            elif ob.rolename=="employer":
                return redirect("employer_dashboard")

        except Exception as e:
            return render(request,"login.html",
                          {"msg":"invalid username & password"})

    formobj=loginform()
    return render(request,"login.html",{'form':formobj})

def Logout(request):
    request.session.flush()   # Clears all session data
    return redirect('home') 