from django.db import models
from auth_app.models import User


class UserPost(models.Model):
    title = models.CharField(
        max_length=64,
    )

    image = models.ImageField(
        upload_to='blogs_images',
        blank=True)

    content = models.TextField(
        blank=True,
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    like_count = models.DecimalField(
        max_digits=8,
        decimal_places=0,
        default=0
    )

    comment_count = models.DecimalField(
        max_digits=8,
        decimal_places=0,
        default=0
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class Comment(models.Model):
    text = models.TextField(
        blank=False,
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post_id = models.ForeignKey(
        UserPost,
        on_delete=models.CASCADE
    )


class Like(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post_id = models.ForeignKey(
        UserPost,
        on_delete=models.CASCADE
    )
