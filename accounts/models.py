from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def custom_upload_to(instance, filename):
    try:
        old_instance = Profile.objects.get(pk=instance.pk)
        if old_instance.avatar.url != "/media/" + Profile.default_avatar:
            old_instance.avatar.delete()
    except ObjectDoesNotExist:
        pass
    return "profiles/" + filename


class Profile(models.Model):
    default_avatar = "profiles/default.png"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=custom_upload_to, blank=True, default=default_avatar
    )
    bio = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user}'s profile"

    def set_avatar(self, avatar=default_avatar):
        if avatar is not None:
            self.avatar = avatar
        else:
            self.avatar = Profile.default_avatar

    def avatar_url(user):
        url = None
        try:
            url = Profile.objects.get(user=user).avatar.url
        except ObjectDoesNotExist:
            pass
        except ValueError:
            pass

        if url is None:
            url = str(settings.MEDIA_URL) + "profiles/default.png"
        return url


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get("created", False):
        Profile.objects.get_or_create(user=instance)
