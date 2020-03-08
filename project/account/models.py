from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    position = models.CharField(max_length=128)
    location = models.CharField(max_length=1024)
    skills = models.CharField(max_length=500)

    class Meta:
        ordering: ['created']
    def __str__(self):
        return self.id
