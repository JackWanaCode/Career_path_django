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
from django.urls import path
from . import view

urlpatterns = [
    path('', view.home, name='home'),
    path('home', view.home, name='home'),
    path('about', view.about, name='about'),
    path('login', view.user_login, name='login'),
    path('signup', view.signup, name='signup'),
    path('logout', view.user_logout, name='logout'),
    path('web/job_detail/<job_db_id>/', view.job_detail, name='job_detail'),
    path('.well-known/pki-validation/4FE5B963FE941166B49146CCAF2BB5B4.txt', view.ssl_validate)
]
