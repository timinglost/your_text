from django.urls import path
from .views import *

app_name = 'user_app'

urlpatterns = [
    path('personal_area/', personal_area, name='personal_area'),
    path('edit_password/', edit_password, name='edit_password'),
    path('user_profile/<int:pk>', user_profile, name='user_profile'),
    path('author_sub/<int:pk>/', add_sub, name='author_sub'),
]
