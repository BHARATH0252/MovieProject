from django import forms
from .models import Movie, Review ,Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)  # Allow empty search query
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='All Categories', required=False)