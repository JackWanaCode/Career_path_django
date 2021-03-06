import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_field):
        """Creates and save a new user"""
        if not email:
            raise ValueError('User must have email address')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(self._db)

        return user
