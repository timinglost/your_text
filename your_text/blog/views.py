from django.shortcuts import render, HttpResponseRedirect
from .forms import CreatePost
from django.urls import reverse


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
