from django.urls import path
from webapp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("<position>/<location>", views.JobList.as_view()),
    path("account", views.Account.as_view(), name='account'),
    path("profile", views.Profile.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)