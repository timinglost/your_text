from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('create/', create_post, name='create'),
    path('main/page/<int:page>/', main_post_list, name='main'),
    path('top/page/<int:page>/', top_post_list, name='top'),
    path('author/<slug:author>/page/<int:page>/', author_post_list, name='author'),
    path('post/<int:pk>/', user_post, name='post'),
    path('post/like/<int:post_pk>/', like_post, name='like'),
    path('post/comment/<int:post_pk>', comment_post, name='comment'),
    path('sub/page/<int:page>/', sub_post_list, name='sub_authors'),
]
