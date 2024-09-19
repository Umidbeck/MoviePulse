from django.urls import path
from .views import HomeView, BlogView, CelebritiesView, BlogDetailView, MovDetailView, MoviesView,TopMoviesView, SearchView, ActorsView, LikePostView


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('actors/', ActorsView.as_view(), name='actors'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blogs/', BlogDetailView.as_view(), name='blog-details'),
    path('movies/', MoviesView.as_view(), name='movies'),
    path('movies/<int:pk>/', MovDetailView.as_view(), name='movies-detail'),
    path('celebrities/<int:pk>/', CelebritiesView.as_view(), name='celebrities'),
    path('top-movies/', TopMoviesView.as_view(), name='top-movies'),
    path('search/', SearchView.as_view(), name='search'),
    path('like/post/<int:post_id>/', LikePostView.as_view(), name='like_post'),
]