from job.serializer import JobSerializer
from job.job_services import get_job_list, get_job_db_by_id, add_job, get_job_list_by_user_id, get_job_by_id
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from job.job_services import get_job_db_by_id
from django.urls import reverse


def job_detail(request, job_db_id):
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


class JobAdd(LoginRequiredMixin, APIView):
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