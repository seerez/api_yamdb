from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'category',
        'description',
        'year'
    )
    filter_horizontal = ('genre',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
