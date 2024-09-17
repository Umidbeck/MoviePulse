from django.contrib import admin
from .models import MovPost, Category, Film_Genre, Platform, Comment, Actor, Like
# Register your models here.

admin.site.register(MovPost)
admin.site.register(Category)
admin.site.register(Film_Genre)
admin.site.register(Platform)
admin.site.register(Actor)
admin.site.register(Comment)
admin.site.register(Like)
