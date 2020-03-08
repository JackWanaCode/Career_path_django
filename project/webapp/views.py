from job.serializer import JobSerializer
from job.job_services import get_job_list
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


class JobList(APIView):
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


class Account(APIView):
    """
    get account data.
    """
    def get(self, request, format=None):
        user_id = request.user.id
        if user_id:
            profile_list = account_service.get_all_profile(user_id)
            return render(request, 'account.html', {'profile_list': profile_list})

    # def post(self, request, format=None):
    #     serializer = JobSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateProfile(FormView):
    """create a new profile"""
    template_name = 'create_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        print("created profile")
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
        print('get is called')
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

    # def put(self, request, format=None):
    #     pass

    def delete(self, request, profile_id, format=None):
        print('delete is called')
        profile = self.get_object(profile_id)
        if profile:
            profile.delete()
            print('profile deleted')
            return render(request, 'account.html', status=status.HTTP_301_MOVED_PERMANENTLY)
        else:
            print('profile NOT deleted')
            return Response("Profile is None", status=status.HTTP_404_NOT_FOUND)


