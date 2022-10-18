from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('create/', create_post, name='create'),
    path('main/page/<int:page>/', main_post_list, name='main'),
    path('author/<slug:author>/page/<int:page>/', author_post_list, name='author'),
    path('post/<int:pk>/', user_post, name='post'),
]
