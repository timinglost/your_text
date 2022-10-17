from django.urls import path
from .views import *

app_name = 'user_app'

urlpatterns = [
    path('personal_area/', personal_area, name='personal_area'),
    path('edit_password/', edit_password, name='edit_password'),
]
