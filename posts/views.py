from lib2to3.fixes.fix_input import context

from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import MovPost, Platform, Category, Film_Genre, Actor
from .forms import CommentForm


# Create your views here.

class HomeView(ListView):
    model = MovPost
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-date']

    # def get_queryset(self):
    #     today = timezone.now().date()
    #     return MovPost.objects.filter(premiere_date__gte=today)


class BlogView(ListView):
    model = MovPost
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ['-date']

    def get_queryset(self):
        today = timezone.now().date()
        return MovPost.objects.filter(release_date__gte=today)


class BlogDetailView(TemplateView):
    template_name = 'blog-details.html'


class CelebritiesView(DetailView):
    model = Actor
    template_name = 'celebrities.html'
    context_object_name = 'post'


class ActorsView(ListView):
    model = Actor
    template_name = 'index-2.html'
    context_object_name = 'posts'


class MovDetailView(DetailView):
    model = MovPost
    template_name = 'movie-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['platform'] = self.object.platform.all()
        context['film_genre'] = self.object.film_genre.all()
        context['actors'] = self.object.actors.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('movies-detail', pk=self.object.pk)
        return redirect('movies-detail', pk=self.object.pk)


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
