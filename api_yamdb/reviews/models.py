from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import CODE_DEFAULT, CODE_LENGTH
from .validators import validate_year, validate_username

# User
USER_NAME_LENGTH = 150
EMAIL_LENGTH = 254
NOT_UNIQUE_NAME = {'unique': "Это имя пользователя уже существует."}
NOT_UNIQUE_EMAIL = {'unique': "Этот email уже кем-то занят."}
# Categoty, Genre,Review
NAME_LENGTH = 256
SLUG_LENGTH = 50
MIN_SCORE = 1
MAX_SCORE = 10
SCORE_ERROR = 'Укажите значение от {MIN_SCORE} до {MAX_SCORE}.'
# __str__ info
USER_INFO = (
    'Имя пользователя: {username:.15} '
    'Почта: {email}, '
    'Имя: {first_name}, '
    'Фамилия: {last_name}, '
    'Биография: {bio:.15}, '
    'Права доступа: {role}.'
)
TITLE_INFO = (
    'Название: {name:.15}, '
    'Категория: {category}, '
    'Жанр: {genre}, '
    'Описание: {description:.15}, '
    'Год: {year}.'
)
REVIEW_COMMENT_INFO = (
    'Текст: {self.text:.15}, '
    'Автор: {self.author}, '
    'Дата публикации: {self.pub_date}.'
)
# Roles
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """Модель пользователя."""

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
        help_text='Расскажите о себе.',
    )
    role = models.CharField(
        'роль',
        choices=ROLES,
        default=USER,
        max_length=max(len(role) for role, _ in ROLES),
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH,
        default=CODE_DEFAULT,
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
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return USER_INFO.format(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            bio=self.bio,
            role=self.role,
        )


class SlugName(models.Model):
    """Родительский класс для объектов с полями 'name' и 'slug'."""

    name = models.CharField(
        'название',
        max_length=NAME_LENGTH,
        unique=True,
        help_text='Укажите название',
    )
    slug = models.SlugField(
        'уникальный фрагмент URL-адреса',
        max_length=SLUG_LENGTH,
        unique=True,
        help_text='Укажите уникальный фрагмент URL-адреса',
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(SlugName):
    """Категории."""

    class Meta(SlugName.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(SlugName):
    """Жанры."""

    class Meta(SlugName.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        'название произведения',
        max_length=NAME_LENGTH,
        help_text='Укажите название произведения',
    )
    description = models.TextField(
        'описание произведения',
        blank=True,
        null=True,
        help_text='Добавьте описание произведения',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='категория произведения',
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        help_text='Выберите категорию',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр произведения',
        through='GenreTitle',
        help_text='Выберите жанр',
    )
    year = models.PositiveIntegerField(
        'год создания произведения',
        validators=(validate_year,),
        db_index=True,
        help_text='Укажите год создания произведения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return TITLE_INFO.format(
            name=self.name,
            category=self.category,
            genre=self.genre,
            description=self.description,
            year=self.year,
        )


class GenreTitle(models.Model):
    """Жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        verbose_name='жанр',
        on_delete=models.CASCADE,
        help_text='Выберите жанр',
    )
    title = models.ForeignKey(
        Title,
        verbose_name='произведение',
        on_delete=models.CASCADE,
        help_text='Выберите произведение',
    )

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'

    def __str__(self):
        return f'{self.genre} {self.title}'


class TextAuthorDate(models.Model):
    """Родительский класс для объектов с полями
    'text', 'author' и 'pub_date'.
    """

    text = models.TextField(
        'текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        default_related_name = '%(class)ss'

    def __str__(self):
        return REVIEW_COMMENT_INFO.format(
            text=self.text,
            author=self.author,
            pub_date=self.pub_date,
        )


class Review(TextAuthorDate):
    """Отзывы на произведения."""

    title = models.ForeignKey(
        Title,
        verbose_name='произведение',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        'рейтинг',
        validators=(
            MinValueValidator(MIN_SCORE, SCORE_ERROR),
            MaxValueValidator(MAX_SCORE, SCORE_ERROR),
        )
    )

    class Meta(TextAuthorDate.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review',
            ),
        ]


class Comment(TextAuthorDate):
    """Комментарии к отзывам."""

    review = models.ForeignKey(
        Review,
        verbose_name='отзыв',
        on_delete=models.CASCADE,
    )

    class Meta(TextAuthorDate.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
