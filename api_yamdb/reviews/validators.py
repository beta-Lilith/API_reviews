import re

from django.core.exceptions import ValidationError
from django.utils import timezone


# Func validate_username
REGEX = r'^[\w.@+-]+'
NOT_REGEX_NAME = 'Нельзя использовать в имени: {used_chars}'
URL_PATH_NAME = 'me'
BAD_NAME = (URL_PATH_NAME,)
FORBIDDEN_NAME = 'Имя {name} использовать нельзя!'
# Func validate_year
FUTURE_YEAR = (
    'Неверно указан год создания произведения: {value}.'
    'Год создания не может быть больше текущего года: {year_now}'
)


def validate_username(name):
    """Валидация имени пользователя."""
    if name in BAD_NAME:
        raise ValidationError(FORBIDDEN_NAME.format(name=URL_PATH_NAME))
    used_wrong_chars = ''.join(set(re.sub(REGEX, '', name)))
    if used_wrong_chars:
        raise ValidationError(
            NOT_REGEX_NAME.format(used_chars=used_wrong_chars)
        )


def validate_year(value):
    """Валидация года создания произведения."""
    year_now = timezone.now().year
    if value > year_now:
        raise ValidationError(
            FUTURE_YEAR.format(value=value, year_now=year_now)
        )
    return value
