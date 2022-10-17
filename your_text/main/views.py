from django.shortcuts import render
from blog.models import UserPost


def main(request):
    title = 'главная'

    posts = UserPost.objects.all()[:3]

    context = {
        'title': title,
        'posts': posts
    }
    return render(request, 'main/index.html', context)