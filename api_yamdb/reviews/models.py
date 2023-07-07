import secrets
import string

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# User
USER_NAME_LENGTH = 150
EMAIL_LENGTH = 254
ROLE_LENGTH = 10
CODE_LENGTH = 13
REGEX = r'^[\w.@+-]+\Z'
NOT_REGEX_NAME = 'Недопустимое имя пользователя.'
NOT_UNIQUE_NAME = {'unique': "Это имя пользователя уже существует."}
NOT_UNIQUE_EMAIL = {'unique': "Этот email уже кем-то занят."}
# Categoty, Genre
NAME_LENGTH = 256
SLUG_LENGTH = 50
REGEX_FOR_SLUG = r'^[-a-zA-Z0-9_]+$'
NOT_REGEX_SLUG = ('Slug должен содержать только '
                  'буквы, цифры, дефисы и подчеркивания.')

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)

CODE = ''.join(secrets.choice(
    string.ascii_letters + string.digits) for i in range(CODE_LENGTH))


class User(AbstractUser):
    username = models.CharField(
        'логин',
        unique=True,
        error_messages=NOT_UNIQUE_NAME,
        validators=[RegexValidator(
            regex=REGEX,
            message=NOT_REGEX_NAME)],
        max_length=USER_NAME_LENGTH,
    )
    email = models.EmailField(
        'email',
        unique=True,
        error_messages=NOT_UNIQUE_EMAIL,
        max_length=EMAIL_LENGTH,
    )
    first_name = models.CharField(
        'имя',
        max_length=USER_NAME_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=USER_NAME_LENGTH,
        blank=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    role = models.CharField(
        'роль',
        choices=ROLES,
        default=USER,
        max_length=ROLE_LENGTH,
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH,
        default=CODE,
    )

    @property
    def is_user(self):
        self.role == USER

    @property
    def is_moderator(self):
        self.role == MODERATOR

    @property
    def is_admin(self):
        self.role == ADMIN

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']
