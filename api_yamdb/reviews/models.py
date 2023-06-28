from django.contrib.auth.models import AbstractUser
from django.db import models


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
