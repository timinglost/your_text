from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .forms import CreatePost
from django.urls import reverse
from .models import UserPost, Like, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse
from user_app.models import Subscription


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

    posts = UserPost.objects.all().order_by('-created')
    if request.user.is_authenticated:
        likes = get_like_pk(request.user)
    else:
        likes = []

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

    posts = UserPost.objects.filter(author__username=author).order_by('-created')
    if request.user.is_authenticated:
        likes = get_like_pk(request.user)
    else:
        likes = []

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


def top_post_list(request, page=1):
    title = 'посты'

    posts = UserPost.objects.all().order_by('-like_count')
    if request.user.is_authenticated:
        likes = get_like_pk(request.user)
    else:
        likes = []

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

    return render(request, 'blog/top-post-list.html', context)


def sub_post_list(request, page=1):
    title = 'посты'
    sub_ = Subscription.objects.filter(subscriber=request.user)
    sub = []
    for s in sub_:
        sub.append(s.author)
    posts_ = UserPost.objects.all().order_by('-created')
    posts = []
    for post in posts_:
        if post.author in sub:
            posts.append(post)
    if request.user.is_authenticated:
        likes = get_like_pk(request.user)
    else:
        likes = []

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

    return render(request, 'blog/sub-post.html', context)


def user_post(request, pk):
    title = 'пост'

    post = get_object_or_404(UserPost, pk=pk)
    if request.user.is_authenticated:
        likes = get_like_pk(request.user)
    else:
        likes = []
    comments = Comment.objects.filter(post_id=pk).order_by('-created')

    context = {
        'title': title,
        'post': post,
        'likes': likes,
        'comments': comments
    }

    return render(request, 'blog/post.html', context)


def like_post(request, post_pk):
    if is_ajax(request):
        if request.user.is_authenticated:
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
            return JsonResponse({'like_count': like_count, 'authenticated': True})
        else:
            return JsonResponse({'authenticated': False})


def comment_post(request, post_pk):
    if is_ajax(request):
        post = get_object_or_404(UserPost, pk=post_pk)
        comment = Comment(
            text=request.POST['text'],
            author=request.user,
            post_id=post
        )
        comment.save()
        post.comment_count += 1
        post.save()
        comments = Comment.objects.filter(post_id=post_pk).order_by('-created')

        context = {
            'comments': comments
        }
        result = render_to_string('blog/includes/comment.html', context)

        return JsonResponse({'result': result, 'comment_count': post.comment_count})
