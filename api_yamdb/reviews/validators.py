import re

from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.settings import BAD_NAMES, REGEX


# Func validate_username
NOT_REGEX_NAME = 'Нельзя использовать в имени: {used_chars}'
FORBIDDEN_NAME = '{name} использовать нельзя в качестве имени пользователя!'
# Func validate_year
FUTURE_YEAR = (
    'Неверно указан год создания произведения: {value}.'
    'Год создания не может быть больше текущего года: {year_now}'
)


def validate_username(name):
    """Валидация имени пользователя."""
    if name in BAD_NAMES:
        raise ValidationError(FORBIDDEN_NAME.format(name=BAD_NAMES))
    used_wrong_chars = ''.join(set(re.sub(REGEX, '', name)))
    if used_wrong_chars:
        raise ValidationError(
            NOT_REGEX_NAME.format(used_chars=used_wrong_chars)
        )
    return name


def validate_year(value):
    """Валидация года создания произведения."""
    year_now = timezone.now().year
    if value > year_now:
        raise ValidationError(
            FUTURE_YEAR.format(value=value, year_now=year_now)
        )
    return value
