from django.contrib import admin
from .models import Category, Tag, Post, Favourite


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Favourite)