from unicodedata import category
from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.exceptions import ObjectDoesNotExist


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


def custom_upload_to(instance, filename):
    try:
        old_instance = Post.objects.get(pk=instance.pk)
        if old_instance.image is not None:
            old_instance.image.delete()
    except ObjectDoesNotExist:
        pass
    return "profiles/" + filename


class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    image = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=CASCADE)
    tags = models.ManyToManyField("Tag")
    category = models.ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["date", "title"]


class Tag(models.Model):
    name = models.CharField(max_length=40)

    def post_count(self):
        try:
            return Post.objects.count(tag__contains=self.name)
        except ObjectDoesNotExist:
            return 0

    def __str__(self):
        return self.name
