from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Review, Category, Profile ,User
from movieapp.forms import MovieForm, ReviewForm, SearchForm
from .forms import UserRegistrationForm, UserForm ,UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout,update_session_auth_hash
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save

def index(request):
    categories_with_movies = Category.objects.order_by('name').values('id', 'name')
    category_id_to_name = {category['id']: category['name'] for category in categories_with_movies}
    categories = Category.objects.order_by('name')
    movies_by_category = {}
    for category_id, category_name in category_id_to_name.items():
        movies = Movie.objects.filter(category=category_id)
        movies_by_category[category_name] = movies
    context = {
      'movies_by_category': movies_by_category,
      'categories': categories,  # Add the retrieved categories to the context
    }
    return render(request, 'index.html', context)

# Movie functions
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    if reviews.exists():
        average_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        average_rating = None

    context = {'movie': movie, 'reviews': reviews, 'average_rating': average_rating}
    return render(request, 'movies/movie_detail.html', context)


def movie_list_view(request):
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    movies_by_genre = {}
    for genre in genres:
        movies = Movie.objects.filter(genre=genre)
        movies_by_genre[genre] = movies
    return render(request, 'index.html', {'movies_by_genre': movies_by_genre})


@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('movieapp:dashboard', username=request.user.username)
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                review = form.save(commit=False)
                review.movie = movie
                review.user = request.user
                review.save()
                messages.success(request, 'Review added successfully!')
                return redirect('movieapp:movie_detail', movie_id=movie_id)
            else:
                messages.error(request, 'You need to be logged in to add a review.')
        else:
            messages.error(request, 'Form validation failed.')
    else:
        form = ReviewForm()
    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})

def movie_search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            movies = Movie.objects.all()
            if query:
                movies = movies.filter(title__icontains=query)
            if category:
                movies = movies.filter(category=category)
            return render(request, 'search_results.html', {'movies': movies})
    else:
        form = SearchForm()
    return render(request, 'search_results.html', {'form': form})


def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect(reverse('movieapp:dashboard', kwargs={'username': request.user.username}))
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/edit_movie.html', {'form': form})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.added_by == request.user:
        movie.delete()
        messages.success(request, 'Movie deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this movie.')
    return redirect(reverse('movieapp:dashboard', kwargs={'username': request.user.username}))

#User Functions
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
    return render(request, 'profile.html')

def viewprofile(request, username):
    # Retrieve the user object
    user = get_object_or_404(User, username=username)
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    return render(request, 'profile.html', {'user': user, 'profile': profile})


def update_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('movieapp:viewprofile',username=username)  
    else:
        form = UserUpdateForm(instance=user)
    context = {'form': form}
    return render(request, 'update_profile.html', context)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)