from django.db import models
from ckeditor.fields import RichTextField
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["date", "title"]
