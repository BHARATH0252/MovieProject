from django.db import models
from django.contrib.auth.models import User
from django import forms

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='media/posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # Define the default ordering for queries
        ordering = ['title']

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.movie.title} - {self.user.username}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']