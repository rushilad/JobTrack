from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm
from django.db.models import Q



def home(request):
    return render(request, "jobs/home.html")


@login_required
def job_list(request):

    search = request.GET.get("search")
    status = request.GET.get("status")

    jobs = Job.objects.filter(user=request.user)

    # Search
    if search:
        jobs = jobs.filter(
            Q(company__icontains=search) |
            Q(role__icontains=search) |
            Q(location__icontains=search) |
            Q(status__icontains=search)
        )

    # Status filter
    if status:
        jobs = jobs.filter(status__iexact=status)

    return render(request, "jobs/job_list.html", {
        "jobs": jobs,
        "search": search,
        "status": status
    })

@login_required
def add_job(request):

    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect("job_list")

    else:
        form = JobForm()

    return render(request, "jobs/add_job.html", {"form": form})

@login_required
def edit_job(request, job_id):

    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect("job_list")

    else:
        form = JobForm(instance=job)

    return render(request, "jobs/edit_job.html", {"form": form, "job": job})

@login_required
def delete_job(request,job_id):

    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == "POST":
        job.delete()
        return redirect("job_list")


    return render(request, "jobs/delete_job.html", {"job": job})

@login_required
def dashboard(request):

    total_jobs = Job.objects.count()

    applied = Job.objects.filter(status="APPLIED").count()

    interview = Job.objects.filter(status="INTERVIEW").count()

    selected = Job.objects.filter(status="SELECTED").count()

    rejected = Job.objects.filter(status="REJECTED").count()

    context = {
        "total_jobs": total_jobs,
        "applied": applied,
        "interview": interview,
        "selected": selected,
        "rejected": rejected,
    }

    return render(request, "jobs/dashboard.html", context)

def signup(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:

        form = UserCreationForm()

    return render(request, "jobs/signup.html", {"form":form})

def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(

                username=username,
                password=password

            )

            if user is not None:

                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()


    return render(request, "jobs/login.html", {"form": form})    

def logout_view(request):
    logout(request)
    return redirect("home")