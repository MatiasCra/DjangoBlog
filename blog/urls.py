from django.urls import path
from blog import views


urlpatterns = [
    path("", views.index, name="Home"),
    path("categories/", views.categories, name="Categories"),
    path("favourites/", views.favourites, name="Favourites"),
    path("search/", views.search, name="Search"),
    path("myposts/", views.myposts, name="MyPosts"),
    path("create/", views.create_post, name="Create"),
    path("post/update/<int:pk>", views.update_post, name="Update"),
    path("post/delete/<int:pk>", views.DeletePost.as_view(), name="Delete"),
    path("delete_success", views.delete_success, name="DeleteSuccess"),
    path("post/<int:post_id>", views.get_post, name="Post"),
    path(
        "post/favourite/<int:post_id>", views.toggle_favourite, name="ToggleFavourite"
    ),
    path("post/comment/<int:post_id>", views.make_comment, name="MakeComment"),
    path("category/create/", views.CreateCategory.as_view(), name="CreateCategory"),
    path("category/edit/<int:pk>", views.EditCategory.as_view(), name="EditCategory"),
    path("category/delete/<int:pk>", views.DeleteCategory.as_view(), name="DeleteCategory"),
    path("category/delete_success/", views.category_delete_success, name="DeleteCategory"),
]
