from django.urls import path
from job import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("account", views.JobList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)