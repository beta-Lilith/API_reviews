from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


REGEX_FOR_SLUG = r'^[-a-zA-Z0-9_]+$'
NOT_REGEX_SLUG = ('Slug должен содержать только '
                  'буквы, цифры, дефисы и подчеркивания.')
NAME_LENGTH = 256
SLUG_LENGTH = 50

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
        unique=True,
        verbose_name='Название категории',
        help_text='Укажите название категории'
    )
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=REGEX_FOR_SLUG,
            message=NOT_REGEX_SLUG)],
        verbose_name='slug',
        help_text='Укажите slug категории'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Жанры.'''
    name = models.CharField(
        max_length=NAME_LENGTH,
        unique=True,
        verbose_name='Название жанра',
        help_text='Укажите название жанра'
    )
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=REGEX_FOR_SLUG,
            message=NOT_REGEX_SLUG)],
        verbose_name='slug',
        help_text='Укажите slug жанра'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Произведения.'''
    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название произведения',
        help_text='Укажите название произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения',
        help_text='Добавьте описание произведения'
    )
    category = models.ForeignKey(
        Category,
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
    year = models.PositiveIntegerField(
        db_index=True,
        verbose_name='Год создания произведения',
        help_text='Укажите год создания произведения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    '''Жанры и произведения.'''
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
        help_text='Выберите жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Выберите произведение'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.genre} {self.title}'
