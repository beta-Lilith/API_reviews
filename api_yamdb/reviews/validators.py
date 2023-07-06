from django.core.exceptions import ValidationError
from django.utils import timezone


FORBIDDEN_NAME = 'Имя me использовать нельзя!'
ERROR_MESSAGE = 'Неверно указан год создания произведения: {value}'


def validate_username(name):
    if name == 'me':
        raise ValidationError(FORBIDDEN_NAME)
    return name


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(ERROR_MESSAGE.format(value=value))
    return value
