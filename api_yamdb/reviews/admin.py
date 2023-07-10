from django.contrib import admin

from .models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)


CHAR_SLICE = 100


@admin.display(description='пользователь')
def author_name(obj):
    return obj.author.username


@admin.display(description='произведения')
def title_name(obj):
    return obj.title.name


@admin.display(description='жанр')
def genre_name(obj):
    return obj.genre.name


@admin.display(description='категория')
def category_name(obj):
    return obj.category.name


@admin.display(description='отзывы')
def review_text(obj):
    return obj.review.text[:CHAR_SLICE]


@admin.display(description='текст')
def self_text(obj):
    return obj.text[:CHAR_SLICE]


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', category_name, 'year', 'description'
    )
    search_fields = ('name', 'category', 'year')
    list_filter = ('category', 'genre')
    empty_value_display = '-пусто-'


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


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        title_name, genre_name
    )
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'id', title_name, self_text, author_name, 'score', 'pub_date'
    )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', review_text, self_text, author_name, 'pub_date'
    )
    empty_value_display = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'confirmation_code',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    list_editable = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'
