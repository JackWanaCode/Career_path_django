from django.db import models


class JobDb(models.Model):

    company = models.CharField(max_length=40)
    location = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=5000)
    date_post = models.IntegerField()
    html_description = models.TextField()

    def __str__(self):
        return self.company + " | " + self.position + " | " + self.location


