from django.db import models


class ContactInfo(models.Model):
    email = models.EmailField(
        max_length=254,
        blank=False
    )

    phone = models.CharField(
        max_length=20,
        blank=False
    )

    city = models.CharField(
        max_length=100,
        blank=False
    )

    address = models.TextField(
        blank=False
    )
