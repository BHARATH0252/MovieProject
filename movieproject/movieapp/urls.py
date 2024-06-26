from django.urls import path
from . import views

app_name = 'movieapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/add/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/review/', views.add_review, name='add_review'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('profile/<str:username>/', views.viewprofile, name='viewprofile'),
    path('movies/', views.movie_list_view, name='movie_list'),
    path('search/', views.movie_search, name='movie_search'),
    path('movie/edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('update-profile/<str:username>/', views.update_profile, name='update_profile'), 
    path('movies/category/', views.movies_by_category, name='movies_by_category'),
    path('movies/category/<int:category_id>/', views.movies_by_category, name='movies_by_category'),
    path('All', views.movie_all, name='movie_all'),
]
