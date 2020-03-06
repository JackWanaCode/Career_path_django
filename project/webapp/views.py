from job.serializer import JobSerializer
from job.job_services import get_job_list
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from account.models import Profile


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
        return render(request, 'account.html')

    # def post(self, request, format=None):
    #     serializer = JobSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    """get, create new or modified a profile"""
    def get(self, request, format=None):
        return render(request, 'create_profile.html')


    def post(self, request):
        return render(request, 'home.html')
