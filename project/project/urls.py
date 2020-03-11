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
from webapp.home import views as homeviews
from webapp.account import views as account_views
from webapp.job import views as job_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('mo/', include('job.urls')),
    #endpoint point to home
    path('', homeviews.home, name='home'),
    path('home', homeviews.home, name='home'),
    path('about', homeviews.about, name='about'),
    path('login', homeviews.user_login, name='login'),
    path('signup', homeviews.signup, name='signup'),
    path('logout', homeviews.user_logout, name='logout'),
    path('web/job_detail/<job_db_id>/', homeviews.job_detail, name='job_detail'),
    path('.well-known/pki-validation/4FE5B963FE941166B49146CCAF2BB5B4.txt', homeviews.ssl_validate),

    #endpoint handler account management include profile and application
    path('web/account', account_views.Account.as_view(), name='account'),
    path("web/profile/<profile_id>/", account_views.Profile.as_view(), name='profile_handler'),
    path("web/create_profile", account_views.CreateProfile.as_view(), name='create_profile'),
    path("web/update_profile/<profile_id>/", account_views.UpdateProfile.as_view(), name='update_profile'),


    #endpoint handler job management
    path('web/<position>/<location>', job_views.JobList.as_view(), name='job_search'),
    path('web/viewed_jobs/<job_id>/', job_views.ViewedJobsHandler.as_view(), name='viewed_job'),
    path("web/job_add/<job_db_id>/", job_views.JobAdd.as_view(), name='job_add')
]