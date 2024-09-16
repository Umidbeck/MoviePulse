from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import MovPost, Platform, Category, Film_Genre
# Create your views here.

class HomeView(ListView):
    model = MovPost
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-date']

class BlogView(ListView):
    model = MovPost
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ['-date']

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


class MoviesView(ListView):
    model = MovPost
    template_name = 'movies.html'
    context_object_name = 'posts'
    ordering = ['-date']


class TopMoviesView(ListView):
    model = MovPost
    template_name = 'top-movies.html'
    context_object_name = 'posts'
    ordering = ['-date']


class SearchView(ListView):
    model = MovPost
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 2


    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = query.lower()
            return MovPost.objects.filter(title__icontains=query)


