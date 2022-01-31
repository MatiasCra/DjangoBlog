from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from .forms import CategoryForm, PostForm
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Profile
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from .models import Category, Comment, Post, Tag, Favourite
from django.http import HttpResponse, HttpResponseNotModified
import json
from django.core.paginator import Paginator, EmptyPage

POSTS_PER_PAGE = 9


def index(request):
    posts_queryset = Post.objects.all().order_by("-date")
    posts_paginator = Paginator(posts_queryset, POSTS_PER_PAGE)
    try:
        if page := request.GET.get("page"):
            page_obj = posts_paginator.page(page)
        else:
            page_obj = posts_paginator.page(1)
    except EmptyPage:
        page_obj = posts_paginator.page(1)

    no_posts_message = "No posts written yet."

    return render(
        request,
        "blog/index.html",
        {"page": "Blog", "page_obj": page_obj, "no_posts_message": no_posts_message},
    )


@user_passes_test(lambda user: user.is_authenticated)
def favourites(request):
    posts_queryset = [
        post
        for post in Post.objects.all()
        if Favourite.objects.filter(user=request.user, post=post.id).count() > 0
    ]
    no_posts_message = "No favourites added yet."

    posts_paginator = Paginator(posts_queryset, POSTS_PER_PAGE)
    try:
        if page := request.GET.get("page"):
            page_obj = posts_paginator.page(page)
        else:
            page_obj = posts_paginator.page(1)
    except EmptyPage:
        page_obj = posts_paginator.page(1)

    return render(
        request,
        "blog/index.html",
        {
            "page": "Favourites",
            "no_posts_message": no_posts_message,
            "page_obj": page_obj,
        },
    )


def search(request):
    title = request.GET.get("title", None)
    cat = request.GET.get("category")
    tags = request.GET.getlist("tags")
    if title is not None or cat is not None or tags:
        posts = Post.objects.all()
        if title:
            posts = posts.filter(title__icontains=title)

        if cat and cat != "-1":
            posts = posts.filter(category=cat)

        if tags:
            posts_to_exclude = []
            for post in posts:
                if not post.has_all_tags(tags):
                    posts_to_exclude.append(post.id)

            posts = posts.exclude(id__in=posts_to_exclude)

        posts_paginator = Paginator(posts, POSTS_PER_PAGE)

        try:
            if page := request.GET.get("page"):
                page_obj = posts_paginator.page(page)
            else:
                page_obj = posts_paginator.page(1)
        except EmptyPage:
            page_obj = posts_paginator.page(1)

        no_posts_message = "No posts found."
        return render(
            request,
            "blog/index.html",
            {
                "page": "Posts",
                "page_obj": page_obj,
                "no_posts_message": no_posts_message,
            },
        )
    else:
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(
            request,
            "blog/search.html",
            {"page": "Search", "categories": categories, "tags": tags},
        )


def categories(request):
    if request.method == "GET":
        category = request.GET.get("category")
        if category is not None:
            posts = Post.objects.filter(category=category)
            cat_name = Category.objects.get(id=category).name
            no_posts_message = f"No posts in the {cat_name} category yet."

            posts_paginator = Paginator(posts, POSTS_PER_PAGE)
            try:
                if page := request.GET.get("page"):
                    page_obj = posts_paginator.page(page)
                else:
                    page_obj = posts_paginator.page(1)
            except EmptyPage:
                page_obj = posts_paginator.page(1)

            return render(
                request,
                "blog/index.html",
                {
                    "page": cat_name,
                    "page_obj": page_obj,
                    "no_posts_message": no_posts_message,
                },
            )

    cats = Category.objects.all()
    return render(
        request, "blog/categories.html", {"page": "Categories", "categories": cats}
    )


def myposts(request):
    posts = Post.objects.filter(user=request.user.id).order_by("-date")
    no_posts_message = "No posts written yet."

    posts_paginator = Paginator(posts, POSTS_PER_PAGE)

    try:
        if page := request.GET.get("page"):
            page_obj = posts_paginator.page(page)
        else:
            page_obj = posts_paginator.page(1)
    except EmptyPage:
        page_obj = posts_paginator.page(1)

    return render(
        request,
        "blog/index.html",
        {
            "page": "My Posts",
            "page_obj": page_obj,
            "no_posts_message": no_posts_message,
        },
    )


def delete_success(request):
    return render(
        request,
        "blog/post_delete_success.html",
        {"page": "Post Deleted"},
    )


def category_delete_success(request):
    return render(
        request,
        "blog/category_delete_success.html",
        {"page": "Category Deleted"},
    )


def get_post(request, post_id):
    post = Post.objects.get(id=post_id)
    tags = post.tags.all()
    author_avatar_url = Profile.avatar_url(post.user)
    is_fav = Favourite.is_favourited(user_id=request.user.id, post_id=post_id)
    return render(
        request,
        "blog/post.html",
        {
            "page": post.title,
            "post": post,
            "is_fav": is_fav,
            "tags": tags,
            "avatar": author_avatar_url,
        },
    )


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

        data.pop("tags")
        data.update({"tags": tag_ids})

        form = PostForm(data=data, files=files)
        if files and form.is_valid():
            form.save()
            return redirect("Home")
        else:
            return HttpResponse(form.errors)

    if request.method == "GET":
        tags = Tag.objects.all()
        page = "Create post"
        action_title = "Create Post"
        form = PostForm()
        return render(
            request,
            "blog/post_form.html",
            {
                "tags": tags,
                "page": page,
                "action_title": action_title,
                "form": form,
            },
        )


@user_passes_test(lambda user: user.is_authenticated)
def update_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        files = request.FILES
        image = files.get("image")
        if image:
            post.image = image

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

        data.pop("tags")
        data.update({"tags": tag_ids})

        form = PostForm(data=data, files=files)
        if form.is_valid():
            post.title = data.get("title")
            post.subtitle = data.get("subtitle")
            post.content = data.get("content")
            post.category = Category.objects.get(id=data.get("category"))

            for tag in tag_ids:
                post.tags.add(Tag.objects.get(id=tag))

            for tag in post.tags.all():
                if tag.id not in tag_ids:
                    post.tags.remove(tag)

            post.save()

            return redirect("Home")
        else:
            return HttpResponse(form.errors)

    if request.method == "GET":
        if request.user.id != post.user.id:
            return redirect("Home")
        tags = Tag.objects.all()
        page = "Edit post"
        action_title = "Edit Post"
        data = post.__dict__
        data["category"] = post.category.id
        form = PostForm(initial=data)
        post_tags = post.tags.all()
        return render(
            request,
            "blog/post_form.html",
            {
                "tags": tags,
                "post_tags": post_tags,
                "post_id": post.id,
                "page": page,
                "action_title": action_title,
                "form": form,
            },
        )

    return HttpResponse(f"TODO: {pk}")


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
        context["page"] = "Delete post"
        context["post"] = self.object.title
        return context


@user_passes_test(lambda user: user.is_authenticated)
def toggle_favourite(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if Favourite.is_favourited(user_id=request.user.id, post_id=post_id):
            fav = Favourite.objects.get(user=request.user.id, post=post_id)
            fav.delete()
            return HttpResponse("Deleted")
        else:
            fav = Favourite(user=request.user, post=post)
            fav.save()
            return HttpResponse("Created")
    except ObjectDoesNotExist:
        pass

    return HttpResponseNotModified()


@user_passes_test(lambda user: user.is_authenticated)
def make_comment(request, post_id):
    body = json.loads(request.body)
    content = body["content"]
    if not content.isspace() and content != "":
        comment = Comment(
            content=content, user=request.user, post=Post.objects.get(id=post_id)
        )
        comment.save()
        return HttpResponse()
    else:
        return HttpResponseNotModified()


class CreateCategory(UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = "/blog/categories/"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context["page"] = "Create Category"
        return context


class EditCategory(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = "/blog/categories/"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["page"] = "Edit Category"
        return context


class DeleteCategory(UserPassesTestMixin, DeleteView):
    model = Category
    success_url = "/blog/category/delete_success/"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)
        context["page"] = "Delete Category"
        return context