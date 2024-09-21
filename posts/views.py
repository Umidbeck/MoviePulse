from lib2to3.fixes.fix_input import context

from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import MovPost, Platform, Category, Film_Genre, Actor, Like
from .forms import CommentForm
from django.views import View
from django.shortcuts import get_object_or_404


# Create your views here.

class HomeView(ListView):
    model = MovPost
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Foydalanuvchi obyektini olish
        for post in context['posts']:
            post.likes_count = post.likes.count()  # Har bir post uchun like sonini olish
            post.user_liked = user.is_authenticated and post.likes.filter(
                user=user).exists()  # Foydalanuvchi like qo'shgani
        return context


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
        user = self.request.user
        context['platform'] = self.object.platform.all()
        context['film_genre'] = self.object.film_genre.all()
        context['actors'] = self.object.actors.all()
        context['likes_count'] = self.object.likes.count()  # Like sonini olish
        context['form'] = CommentForm()
        context['request'] = self.request
        # Foydalanuvchi tizimga kirganligini tekshirish
        if user.is_authenticated:
            context['user_liked'] = self.object.likes.filter(user=user).exists()  # Foydalanuvchi like qo'shgani
        else:
            context['user_liked'] = False  # Tizimga kirmagan foydalanuvchi uchun

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:  # Foydalanuvchi tizimga kirganligini tekshirish
                comment = form.save(commit=False)
                comment.user = request.user  # Foydalanuvchi ma'lumotlarini qo'shish
                comment.post = self.object  # Postga bog'lash
                comment.save()  # Commentni saqlash
                return redirect('movies-detail', pk=self.object.id)
            else:
                return redirect('login')  # Tizimga kirishni talab qilish
        return render(request, self.template_name, {'form': form, 'post': self.object})


class LikePostView(View):
    def post(self, request, post_id):
        if request.user.is_authenticated:  # Foydalanuvchi tizimga kirganligini tekshirish
            post = get_object_or_404(MovPost, id=post_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)

            if not created:
                like.delete()  # Agar like allaqachon mavjud bo'lsa, uni o'chirish

            return redirect('movies-detail', pk=post.id)
        else:
            return redirect('login')  # Tizimga kirishni talab qilish


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

    def normalize_query(self, query):
        # Kiril yozuvini lotin yozuviga o'zgartirish
        transliteration_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j',
            'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
            'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        }
        normalized_query = ''.join(transliteration_map.get(char, char) for char in query)
        return normalized_query

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            normalized_query = self.normalize_query(query)  # Normalizatsiya qilish
            # Qidiruvni amalga oshirish
            return MovPost.objects.filter(
                Q(title__icontains=query) |  # Lotin yozuvidagi qidiruv
                Q(title__icontains=normalized_query)  # Kiril yozuvidagi normalizatsiya qilingan qidiruv
            )
        return MovPost.objects.none()  # Agar qidiruv so'rovi bo'lmasa, bo'sh queryset qaytaring
