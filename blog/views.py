from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from .forms import PostForm
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist

# from django.views.generic import ListView
from accounts.models import Profile
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
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
        "blog/post_delete_success.html",
        {"page": "Post deleted"},
    )


def get_post(request, post_id):
    post = Post.objects.get(id=post_id)
    tags = post.tags.all()
    author_avatar_url = Profile.avatar_url(post.user)
    return render(
        request,
        "blog/post.html",
        {"page": post.title, "post": post, "tags": tags, "avatar": author_avatar_url},
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


@user_passes_test(lambda user: user.is_authenticated)
def create_post(request):
    if request.method == "POST":
        files = request.FILES
        data = request.POST.copy()

        data.update(user=request.user)
        tags = data.getlist("tags")

        tag_ids = []
        for tag_info in tags:
            if not tag_info.isspace() and tag_info != "":
                try:
                    tag = Tag.objects.get(id=tag_info)
                    tag_ids.append(tag.id)

                except (ObjectDoesNotExist, ValueError):
                    if not tag_info.isnumeric():
                        tag = Tag(name=tag_info)
                        tag.save()
                        tag_ids.append(tag.id)

                except IntegrityError:
                    tag = Tag.objects.get(name=tag_info)
                    tag_ids.append(tag.id)
                    
        print("IDS:", tag_ids)
        data.pop("tags")
        data.update({"tags": tag_ids})
            
        print("\nDATA:\n", data.lists, "\n")

        form = PostForm(data=data, files=files)
        if form.is_valid():
            form.save()
            return redirect("Home")
        else:
            print("\n\n", form.errors)

        return HttpResponse("Something went wrong :(")

    if request.method == "GET":
        avatar = Profile.avatar_url(request.user.id)
        tags = Tag.objects.all()
        page = "Create post"
        action_title = "Create Post"
        form = PostForm()
        return render(
            request,
            "blog/post_form.html",
            {
                "avatar": avatar,
                "tags": tags,
                "page": page,
                "action_title": action_title,
                "form": form,
            },
        )


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
        context["post"] = self.object.title
        return context


def add_tag(request):
    if request.method == "POST":
        tag_name = json.loads(request.body.decode("utf-8")).get("tag")
        tag = Tag(name=tag_name)
        tag.save()
        return HttpResponse(tag.id)
