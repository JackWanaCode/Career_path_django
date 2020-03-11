from job.serializer import JobSerializer
from job.job_services import get_job_list, get_job_db_by_id, add_job, get_job_list_by_user_id, get_job_by_id
from account import account_service
from webapp.forms import ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from account.account_service import get_all_profile
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core import serializers
import json
from django.contrib.auth.mixins import LoginRequiredMixin


class JobList(LoginRequiredMixin, APIView):
    """
    List all job, or create a new job data.
    """
    def get(self, request, position, location, format=None):
        jobs = get_job_list(position, location)
        if request.user.id:
            return render(request, 'job_search.html', {'jobs': jobs, 'user_id': request.user.id})
        else:
            return render(request, 'job_search.html', {'jobs': jobs})

    def post(self, request, format=None):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Account(LoginRequiredMixin, APIView):
    """
    get account data.
    """

    def get(self, request, format=None):
        print('get is called')
        user_id = request.user.id
        if user_id:
            profile_list = account_service.get_all_profile(user_id)
            job_list = get_job_list_by_user_id(user_id)
            data = {
                'profile_list': profile_list,
                'job_list': job_list
            }
            return render(request, 'account.html', data)


class ViewedJobsHandler(LoginRequiredMixin, APIView):

    def get_object(self, job_id):
        job = get_job_by_id(job_id)
        if job:
            return job
        else:
            raise Http404


    def put(self, request, job_id, format=None):
        print('put is called')
        print(request.data)
        job = self.get_object(job_id)
        if not job:
            return Response("job is not existed", status=status.HTTP_400_BAD_REQUEST)
        if 'status' in request.data:
            print('status', request.data['status'])
            job.status = request.data['status']
        if 'note' in request.data:
            job.note = request.data['note']
        if 'interview' in request.data:
            job.interview = request.data['interview']
        if 'applied' in request.data:
            job.applied = request.data['applied']
        job.save()
        return Response("Viewed Job is updated", status=status.HTTP_200_OK)

    def delete(self, request, job_id, format=None):
        print('delete is called')
        job = self.get_object(job_id)
        if not job:
            return Response("job is not existed", status=status.HTTP_400_BAD_REQUEST)
        job.delete()
        return render(request, 'account.html')


class CreateProfile(LoginRequiredMixin, FormView):
    """create a new profile"""
    template_name = 'create_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        profile = account_service.create_profile(
            user=self.request.user,
            position=form.cleaned_data.get('position'),
            location=form.cleaned_data.get('location'),
            skills=form.cleaned_data.get('skills')
        )
        if profile is not None:
            return super(CreateProfile, self).form_valid(form)
        else:
            return Response("profile is None", status=status.HTTP_400_BAD_REQUEST)


class UpdateProfile(LoginRequiredMixin, FormView):
    template_name = 'create_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account')
    print('update profile class')

    def form_valid(self, form):
        print('update profile is called')
        profile_id = self.kwargs['profile_id']
        profile = account_service.get_profile_by_id(profile_id)
        if profile is not None:
            profile.position = form.cleaned_data.get('position')
            profile.location = form.cleaned_data.get('location')
            profile.skills = form.cleaned_data.get('skills')
            profile.save()
            return super(UpdateProfile, self).form_valid(form)
        else:
            return Response("profile is None", status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    """get and update profile"""
    # http_method_names = ['GET', 'PUT', 'DELETE']

    def get_object(self, profile_id):
        # profile = account_service.get_profile_by_id(profile_id)
        # self.check_object_permissions(self.request, profile)
        # return profile
        profile = account_service.get_profile_by_id(profile_id)
        if profile:
            return profile
        else:
            raise Http404

    def get(self, request, profile_id, format=None):
        profile = self.get_object(profile_id)
        response = {
            'data': {
                'user_id': profile.user.id,
                'position': profile.position,
                'location': profile.location,
                'skills': profile.skills
            },
        }

        return Response(json.dumps(response), status=status.HTTP_200_OK)

    def delete(self, request, profile_id, format=None):
        profile = self.get_object(profile_id)
        if profile:
            profile.delete()
            return render(request, 'account.html')
        else:
            print('profile NOT deleted')
            return Response("Profile is None", status=status.HTTP_404_NOT_FOUND)


class JobAdd(APIView):
    """get or post job that seen by user"""

    def get(self, request, job_id, format=None):
        job = get_job_db_by_id(job_id)
        if job:
            response = {
                'data': {
                    'user_id': job.user.id,
                    'position': job.position,
                    'location': job.location,
                    'description': job.description,
                    'html_description': job.html_description,
                    'link': job.link,
                    'applied': job.applied,
                    'status': job.status,
                    'note': job.note,
                    'skills': job.skills,
                },
            }
            return Response(json.dumps(response), status=status.HTTP_200_OK)
        return None

    def post(self, request, job_db_id, format=None):
        job = add_job(job_db_id, request.user)
        if job:
            response = {
                'data': {
                    'user_id': job.user.id,
                    'position': job.position,
                    'location': job.location,
                },
            }
            return Response(json.dumps(response), status=status.HTTP_201_CREATED)
        else:
            return Response("Job can't be added", status=status.HTTP_400_BAD_REQUEST)

