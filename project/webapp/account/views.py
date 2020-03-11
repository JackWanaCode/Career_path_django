from job.job_services import get_job_list, get_job_db_by_id, add_job, get_job_list_by_user_id, get_job_by_id
from account import account_service
from webapp.account.forms import ProfileForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import Http404
import json
from django.contrib.auth.mixins import LoginRequiredMixin


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


class Profile(LoginRequiredMixin, APIView):
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
