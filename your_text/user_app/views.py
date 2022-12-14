from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .forms import UserEditForm, UserPasswordEditForm
from django.urls import reverse
import os
from django.conf import settings
from auth_app.models import User
from blog.models import UserPost
from django.http import JsonResponse
from .models import Subscription


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def personal_area(request):
    title = 'личный кабинет'

    if request.method == 'POST':
        image = str(request.user.avatar)
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if request.FILES and image:
                os.remove(os.path.join(settings.MEDIA_ROOT, image))
            form.save()
            return HttpResponseRedirect(reverse('user:personal_area'))
    else:
        form = UserEditForm(instance=request.user)

    context = {
        'title': title,
        'form': form
    }
    return render(request, 'user/personal_area.html', context)


def edit_password(request):
    title = 'смена пароля'

    if request.method == 'POST':
        form = UserPasswordEditForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = UserPasswordEditForm(request.user)

    context = {
        'title': title,
        'form': form
    }

    return render(request, 'user/edit_password.html', context)


def user_profile(request, pk):
    title = 'профиль'
    user_info = get_object_or_404(User, pk=pk)
    last_post = UserPost.objects.filter(author=user_info).order_by('-created')[:4]
    sub_ = Subscription.objects.filter(author=user_info, subscriber=request.user)
    context = {
        'title': title,
        'user_info': user_info,
        'last_post': last_post,
        'sub_': sub_
    }
    return render(request, 'user/user-profile.html', context)


def add_sub(request, pk):
    if is_ajax(request):
        if request.user.is_authenticated:
            author = get_object_or_404(User, pk=pk)
            sub_check = Subscription.objects.filter(author=author, subscriber=request.user)
            if sub_check:
                sub_check.delete()
                sub = False
            else:
                sub_now = Subscription(author=author, subscriber=request.user)
                sub_now.save()
                sub = True
            return JsonResponse({'authenticated': True, 'sub': sub})
        else:
            return JsonResponse({'authenticated': False})
