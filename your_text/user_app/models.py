from django.db import models
from auth_app.models import User


class Subscription(models.Model):
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE
    )

    subscriber = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE
    )
