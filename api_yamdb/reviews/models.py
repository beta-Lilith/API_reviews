from django.contrib.auth.models import AbstractUser
from django.db import models


NAME_LENGTH: int = 256
SLUG_LENGTH: int = 50

ROLE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        'логин',
        unique=True,
        max_length=150,
    )
    email = models.EmailField(
        'email',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    role = models.CharField(
        'роль',
        choices=ROLE,
        default='user',
        max_length=10,
        blank=True,
    )


class Category(models.Model):
    '''Категории.'''
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название категории')
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Жанры.'''
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='slug',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Произведения.'''
    name = models.CharField(
        max_length=NAME_LENGTH,
        db_index=True,
        verbose_name='Название произведения'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        help_text='Выберите категорию',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр произведения',
        help_text='Выберите жанр'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        db_index=True,
        verbose_name='Год создания произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    '''Жанры и произведения.'''
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre} {self.title}'
