from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .forms import CreatePost
from django.urls import reverse
from .models import UserPost, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_like_pk(user):
    likes = Like.objects.filter(user_id=user)
    answer = [];
    for like in likes:
        answer.append(like.post_id.pk)
    return answer


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
    likes = get_like_pk(request.user)

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
        'likes': likes
    }

    return render(request, 'blog/post-list.html', context)


def author_post_list(request, author, page=1):
    title = 'посты'

    posts = UserPost.objects.filter(author__username=author)
    likes = get_like_pk(request.user)

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
        'author': author,
        'likes': likes
    }

    return render(request, 'blog/author-post.html', context)


def user_post(request, pk):
    title = 'пост'

    post = get_object_or_404(UserPost, pk=pk)
    likes = get_like_pk(request.user)

    context = {
        'title': title,
        'post': post,
        'likes': likes
    }

    return render(request, 'blog/post.html', context)


def like_post(request, post_pk):
    if is_ajax(request):
        post = get_object_or_404(UserPost, pk=post_pk)
        like = Like.objects.filter(user_id=request.user, post_id=post_pk)
        if like:
            post.like_count -= 1
            post.save()
            like.delete()
        else:
            post.like_count += 1
            post.save()
            like = Like(user_id=request.user, post_id=post)
            like.save()
        like_count = post.like_count
        return JsonResponse({'like_count': like_count})
