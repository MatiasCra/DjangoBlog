from unicodedata import name
from django.urls import path
from blog import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('categories/', views.categories, name='Categories'),
    path('myposts/', views.myposts, name='MyPosts'),
    path('create/', views.CreatePost.as_view(), name='Create'),
    path('post/<int:post_id>', views.get_post, name='Post')
]