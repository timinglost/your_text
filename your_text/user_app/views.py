from django.shortcuts import render, HttpResponseRedirect
from .forms import UserEditForm, UserPasswordEditForm
from django.urls import reverse
import os
from django.conf import settings


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

