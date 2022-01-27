from datetime import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=40)

    def posts_in_category(self):
        try:
            return Post.objects.filter(category=self.name)
        except ObjectDoesNotExist:
            return []

    def post_count(self):
        try:
            return Post.objects.count(category=self.name)
        except ObjectDoesNotExist:
            return 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


def custom_upload_to(instance, filename):

    try:
        old_instance = Post.objects.get(pk=instance.pk)
        if old_instance.image is not None:
            if not filename:
                filename = old_instance.image.url
            old_instance.image.delete()
    except ObjectDoesNotExist:
        pass
    return "images/" + filename


class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    image = models.ImageField(upload_to=custom_upload_to, blank=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)
    category = models.ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return self.title

    def comments(self):
        try:
            return Comment.objects.filter(post=self.id).order_by("-timestamp")
        except ObjectDoesNotExist:
            return None

    def has_tag(self, tag_id: int):
        return self.tags.filter(id=tag_id).count() > 0

    def has_all_tags(self, tags_ids: list):
        for tag in tags_ids:
            if not self.has_tag(tag):
                return False
        return True

    def author_avatar(self):
        return Profile.avatar_url(self.user)

    @classmethod
    @staticmethod
    def post_with_most_comments():
        posts = Post.objects.all()
        max_amount = 0
        max_comments_post = None
        for post in posts:
            if (ammount := post.comments().count()) >= max_amount:
                max_amount = ammount
                max_comments_post = post
        print(f"The post with the most comments is: {max_comments_post}")
        return max_comments_post

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["date", "title"]


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def post_count(self):
        try:
            return Post.objects.count(tag__contains=self.name)
        except ObjectDoesNotExist:
            return 0

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)

    @classmethod
    @staticmethod
    def is_favourited(user_id, post_id):
        try:
            Favourite.objects.get(user=user_id, post=post_id)
            return True
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return f"{self.user} <==> {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def profile(self):
        try:
            return Profile.objects.get(user=self.user)
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return f"{self.user} on {self.post}: {self.content:.30}"
