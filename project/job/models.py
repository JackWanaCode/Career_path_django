from django.db import models
from django.conf import settings


class JobDb(models.Model):
    """Jobs that scrapped from internet"""
    company = models.CharField(max_length=40)
    location = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=5000)
    date_post = models.IntegerField()
    html_description = models.TextField()

    def __str__(self):
        return self.company + " | " + self.position + " | " + self.location

class Job(models.Model):
    """Jobs that seen by user"""
    company = models.CharField(max_length=40)
    location = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    description = models.TextField()
    html_description = models.TextField()
    link = models.CharField(max_length=5000)
    applied = models.DateTimeField(blank=True, null=True)
    interview = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    skills = models.CharField(max_length=500)

    def __str__(self):
        return self.company + " | " + self.position + " | " + self.location
