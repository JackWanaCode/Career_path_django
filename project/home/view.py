
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from .forms import SignUpForm

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from job.models import JobDb
from job.job_services import get_job_list, get_job_db_by_id, add_job
from rest_framework.response import Response
from rest_framework import status
from django.utils.safestring import mark_safe
from job.job_services import get_job_list_by_user_id


def home(request):
    jobs = JobDb.objects.all()
    return render(request, 'home.html', {'jobs': jobs})

def about(request):
    return render(request, 'about.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    # jobs = JobDb.objects.all()
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'GET':
        return render(request, 'account.html', {})


def job_detail(request, job_db_id):
    print(job_db_id)
    job_db_obj = get_job_db_by_id(job_db_id)
    if job_db_obj is not None:
        success = add_job(job_db_id, request.user)
        if success:
            print("Successful add job")
        else:
            print("Job can't add to viewed list at the moment")
        data = {
            'job_db_obj': job_db_obj,
            'descrip': mark_safe(job_db_obj.html_description)
        }
        return render(request, 'job_detail.html', data)
    else:
        return HttpResponseRedirect(reverse('account'))
