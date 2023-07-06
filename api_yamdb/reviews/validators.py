from django.core.exceptions import ValidationError
from django.utils import timezone


FORBIDDEN_NAME = 'Имя me использовать нельзя!'
ERROR_MESSAGE = ('Неверно указан год создания произведения: {year}.'
                 'Год создания не может быть больше текущего года: {year_now}')


def validate_username(name):
    if name == 'me':
        raise ValidationError(FORBIDDEN_NAME)
    return name


def validate_year(value):
    if value > timezone.now().year:
        ERROR_MESSAGE.format(year=value, year_now=timezone.now().year)
    return value
