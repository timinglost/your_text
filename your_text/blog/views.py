from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .forms import CreatePost
from django.urls import reverse
from .models import UserPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def create_post(request):
    title = 'создание поста'

    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = CreatePost()

    context = {
        'title': title,
        'form': form
    }

    return render(request, 'blog/create-post.html', context)


def main_post_list(request, page=1):
    title = 'посты'

    posts = UserPost.objects.all()

    paginator = Paginator(posts, 5)
    try:
        posts_paginator = paginator.page(page)
    except PageNotAnInteger:
        posts_paginator = paginator.page(1)
    except EmptyPage:
        posts_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'posts': posts_paginator
    }

    return render(request, 'blog/post-list.html', context)


def author_post_list(request, author, page=1):
    title = 'посты'

    posts = UserPost.objects.filter(author__username=author)

    paginator = Paginator(posts, 5)
    try:
        posts_paginator = paginator.page(page)
    except PageNotAnInteger:
        posts_paginator = paginator.page(1)
    except EmptyPage:
        posts_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'posts': posts_paginator,
        'author': author
    }

    return render(request, 'blog/author-post.html', context)


def user_post(request, pk):
    title = 'пост'

    post = get_object_or_404(UserPost, pk=pk)

    context = {
        'title': title,
        'post': post
    }

    return render(request, 'blog/post.html', context)
