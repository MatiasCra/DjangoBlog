from django.shortcuts import render
from .forms import PostForm
from django.views.generic.edit import UpdateView, CreateView, DeleteView

# from django.views.generic import ListView
from accounts.models import Profile
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Category, Post, Tag
from django.http import HttpResponse
import json


def index(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "blog/index.html", {"page": "Blog", "posts": posts})


def categories(request):
    if request.method == "GET":
        category = request.GET.get("category")
        if category is not None:
            posts = Post.objects.filter(category=category)
            return render(
                request, "blog/index.html", {"page": "Categories", "posts": posts}
            )

    cats = Category.objects.all()
    return render(
        request, "blog/categories.html", {"page": "Categories", "categories": cats}
    )


def myposts(request):
    posts = Post.objects.filter(user=request.user.id).order_by("-date")
    return render(request, "blog/myposts.html", {"page": "My Posts", "posts": posts})


def delete_success(request):
    return render(
        request,
        "pages/page_delete_success.html",
        {"avatar": Profile.avatar_url(request.user.id), "page": "Post deleted"},
    )


def get_post(request, post_id):
    post = Post.objects.get(id=post_id)
    author_avatar_url = Profile.avatar_url(post.user)
    return render(
        request,
        "blog/post.html",
        {"page": post.title, "post": post, "avatar": author_avatar_url},
    )


class UpdatePost(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = Post
    success_url = "/pages/"

    def test_func(self):
        post = Post.objects.get(id=self.kwargs["pk"])
        return (
            self.request.user.is_authenticated and self.request.user.id == post.user.id
        )

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        avatar = Profile.avatar_url(self.request.user.id)
        context["avatar"] = avatar
        context["page"] = "Edit post"
        context["action_title"] = "Edit post"
        return context


class CreatePost(UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        avatar = Profile.avatar_url(self.request.user.id)
        context["avatar"] = avatar
        context["page"] = "Create post"
        context["action_title"] = "Create Post"
        return context


class DeletePost(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/blog/delete_success"

    def test_func(self):
        post = Post.objects.get(id=self.kwargs["pk"])
        return (
            self.request.user.is_authenticated and self.request.user.id == post.user.id
        )

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)
        avatar = Profile.avatar_url(self.request.user.id)
        context["avatar"] = avatar
        context["page"] = "Delete post"
        return context


def add_tag(request):
    if request.method == "POST":
        tag_name = json.loads(request.body.decode("utf-8")).get("tag")
        tag = Tag(name=tag_name)
        tag.save()
        return HttpResponse(tag.id)
