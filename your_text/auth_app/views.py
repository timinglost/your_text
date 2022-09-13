from django.shortcuts import render, HttpResponseRedirect
from .forms import UserLoginForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'вход'

    form = UserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main:index'))

    context = {
        'title': title,
        'form': form,
        'next': next,
    }

    return render(request, 'auth/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))
