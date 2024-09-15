from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import MovPost, Platform, Category, Film_Genre
# Create your views here.

class HomeView(ListView):
    model = MovPost
    template_name = 'index.html'
    context_object_name = 'posts'

class BlogView(TemplateView):
    template_name = 'blog.html'

class BlogDetailView(TemplateView):
    template_name = 'blog-details.html'


class CelebritiesView(TemplateView):
    template_name = 'celebrities.html'


class MovDetailView(DetailView):
    model = MovPost
    template_name = 'movie-details.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform'] = self.object.platform.all()
        context['film_genre'] = self.object.film_genre.all()
        return context


class MoviesView(TemplateView):
    template_name = 'movies.html'

class TopMoviesView(TemplateView):
    template_name = 'top-movies.html'
