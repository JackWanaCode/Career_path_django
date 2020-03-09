"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from webapp import views as webviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('mo/', include('job.urls')),
    path('web/<position>/<location>', webviews.JobList.as_view(), name='job_search'),
    path('web/account', webviews.Account.as_view(), name='account'),
    path('web/viewed_jobs/<job_id>/', webviews.ViewedJobsHandler.as_view(), name='viewed_job'),
    path("web/profile/<profile_id>/", webviews.Profile.as_view(), name='profile_handler'),
    path("web/create_profile", webviews.CreateProfile.as_view(), name='create_profile'),
    path("web/update_profile/<profile_id>/", webviews.UpdateProfile.as_view(), name='update_profile'),
    path("web/job_add/<job_db_id>/", webviews.JobAdd.as_view(), name='job_add')
]