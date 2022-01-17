from django.shortcuts import render
from .forms import PostForm
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.edit import DeleteView
from accounts.models import Profile
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Post


def index(request):
    return render(request, "blog/index.html", {"page": "Blog"})


def categories(request):
    return render(request, "blog/categories.html", {"page": "Categories"})


def myposts(request):
    return render(request, "blog/myposts.html", {"page": "My posts"})


def delete_success(request):
    return render(
        request,
        "pages/page_delete_success.html",
        {
            "avatar": Profile.avatar_url(request.user.id),
            "page": "Post deleted"
        },
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
