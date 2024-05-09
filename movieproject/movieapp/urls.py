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
    path('profile/', views.view_profile, name='view_profile'),
    path('movies/', views.movie_list_view, name='movie_list'),
    path('search/', views.movie_search, name='movie_search'),
    path('movie/edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
]
