from django.db import models
from  django.contrib.auth.models import User

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
    time = models.TimeField()
    date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateField()
    language = models.CharField(max_length=100)
    platform = models.ManyToManyField('Platform', blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True)
    video_link = models.URLField(blank=True)
    film_genre = models.ManyToManyField('Film_Genre', blank=True)

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