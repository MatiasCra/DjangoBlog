from django.contrib import admin
from .models import Category, Tag, Post, Favourite, Comment


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Favourite)