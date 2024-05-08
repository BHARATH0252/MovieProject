from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Review
from movieapp.forms import MovieForm, ReviewForm
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


# def movie_list(request):
#     movies = Movie.objects.all()
#     return render(request, 'movies/movie_list.html', {'movies': movies})

def index(request):
    movie_list = Movie.objects.all()
    # Pass the movie_list to the template for rendering
    return render(request, 'index.html', {'movie_list': movie_list})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews})


def movie_list_view(request):
    # Retrieve a list of movie objects from the database
    movie_list = Movie.objects.all()
    # Pass the movie_list to the template for rendering
    return render(request, 'index.html', {'movie_list': movie_list})


@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:  # Ensure user is authenticated
                review = form.save(commit=False)
                review.movie = movie
                review.user = request.user
                review.save()
                messages.success(request, 'Review added successfully!')
                return redirect('movie_detail', movie_id=movie_id)
            else:
                messages.error(request, 'You need to be logged in to add a review.')
        else:
            messages.error(request, 'Form validation failed.')
    else:
        form = ReviewForm()

    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('movieapp:user_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the dashboard after successful login
            return redirect('movieapp:dashboard', username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('movieapp:index')


@login_required
def dashboard(request, username):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user  # Assign the logged-in user to the movie
            movie.save()
            return redirect('movieapp:dashboard', username=username)
    else:
        form = MovieForm()
    movies = Movie.objects.filter(added_by__username=username)
    return render(request, 'dashboard.html', {'form': form, 'movies': movies, 'username': username})


@login_required
def view_profile(request):
    # Logic to fetch and display user profile information
    return render(request, 'profile.html')
