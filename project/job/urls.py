from django.urls import path
from job import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("<position>/<location>", views.JobList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)