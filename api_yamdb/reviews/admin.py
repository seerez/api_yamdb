from django.contrib import admin

from .models import Category, Genre, Title


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'category',
        'description',
        'year'
    )
    filter_horizontal = ('genre',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Category, CategoryAdmin)
