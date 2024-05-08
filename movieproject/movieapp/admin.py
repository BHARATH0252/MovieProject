from django.contrib import admin
from .models import Category, Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')

admin.site.register(Category)
admin.site.register(Movie, MovieAdmin)