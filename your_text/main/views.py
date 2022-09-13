from django.shortcuts import render


def main(request):
    title = 'главная'

    context = {
        'title': title,
    }
    return render(request, 'main/index.html', context)