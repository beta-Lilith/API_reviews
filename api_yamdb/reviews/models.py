from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year, validate_username

# User
USER_NAME_LENGTH = 150
EMAIL_LENGTH = 254
CODE_LENGTH = 13
NOT_UNIQUE_NAME = {'unique': "Это имя пользователя уже существует."}
NOT_UNIQUE_EMAIL = {'unique': "Этот email уже кем-то занят."}
# Categoty, Genre
NAME_LENGTH = 256
SLUG_LENGTH = 50
CHAR_SLICE = 15
USER_INFO = (
    'Имя пользователя: {username:.15}\n'
    'Почта: {email}\n'
    'Имя: {first_name}\n'
    'Фамилия: {last_name}\n'
    'Биография: {bio:.15}\n'
    'Права доступа: {role}\n'
)
TITLE_INFO = (
    'Название: {name:.15}\n'
    'Категория: {category}\n'
    'Жанр: {genre}\n'
    'Описание: {description:.30}\n'
    'Год: {year}'
)

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        'логин',
        unique=True,
        error_messages=NOT_UNIQUE_NAME,
        validators=(validate_username,),
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
        max_length=max(len(role[1]) for role in ROLES),
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return USER_INFO.format(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            bio=self.bio,
            role=self.role,
            confirmation_code=self.confirmation_code,
        )


class CategoryGanre(models.Model):
    """Абстрактный базовый класс для категорий и жанров."""
    name = models.CharField(
        max_length=NAME_LENGTH,
        unique=True,
        verbose_name='Название',
        help_text='Укажите название'
    )
    slug = models.SlugField(
        max_length=SLUG_LENGTH,
        unique=True,
        verbose_name='Уникальный фрагмент URL-адреса',
        help_text='Укажите уникальный фрагмент URL-адреса'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGanre):
    """Категории."""

    class Meta(CategoryGanre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(CategoryGanre):
    """Жанры."""

    class Meta(CategoryGanre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
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
        validators=(validate_year,),
        db_index=True,
        verbose_name='Год создания произведения',
        help_text='Укажите год создания произведения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return TITLE_INFO.format(
            name=self.name,
            category=self.category,
            genre=self.genre,
            description=self.description,
            year=self.year
        )


class GenreTitle(models.Model):
    """Жанры и произведения."""
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
        verbose_name='Рейтинг',
        validators=(
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        )
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
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
        ordering = ('pub_date',)
