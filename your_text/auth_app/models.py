from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to=f'users_avatars/{datetime.now().year}/{datetime.now().month}/{datetime.now().day}',
        blank=True)
