from django import forms
from .models import Movie, Review,Category,Profile
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

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)  # Allow empty search query
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='All Categories', required=False)



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['bio']  # Add more fields as needed

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']