from django.urls import path
from blog import views


urlpatterns = [
    path('', views.index, name='Home'),
    path('categories/', views.categories, name='Categories'),
    path('myposts/', views.myposts, name='MyPosts'),
    path('create/', views.create_post, name='Create'),
    path('post/delete/<int:pk>', views.DeletePost.as_view(), name='Delete'),
    path('delete_success', views.delete_success, name='DeleteSuccess'),
    path('post/<int:post_id>', views.get_post, name='Post'),
    path('tag/add/', views.add_tag, name='NewTag'),
]