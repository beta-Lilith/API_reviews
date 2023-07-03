from django.contrib import admin
from .models import Category, Genre, GenreTitle, Title, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'year', 'description'
    )  # , 'rating'
    search_fields = ('name', 'category', 'year')
    list_filter = ('category', 'genre')
    empty_value_display = '-пусто-'


@admin.register(GenreTitle)
class GenreTitle(admin.ModelAdmin):
    list_display = (
        'title', 'genre'
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'confirmation_code', 'first_name', 'last_name', 'bio', 'role'
    )
    list_editable = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'
