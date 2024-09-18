from django.db import models
from django.contrib.auth.models import User

from config import settings


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MovPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    mov_author = models.CharField(max_length=100)
    director = models.CharField(max_length=35)
    time = models.DurationField()
    date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateField()
    language = models.CharField(max_length=100)
    platform = models.ManyToManyField('Platform', blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True)
    video_link = models.URLField(blank=True)
    film_genre = models.ManyToManyField('Film_Genre', blank=True)
    actors = models.ManyToManyField('Actor', blank=True)

    def __str__(self):
        return self.title


class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Film_Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    body = models.TextField()
    mov_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', blank=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(MovPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(MovPost, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"
