from .models import ContactInfo


def info(request):
    info = ContactInfo.objects.first()

    return {
       'info': info,
    }
