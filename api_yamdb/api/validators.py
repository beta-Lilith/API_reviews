from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


def validate_slug(value):
    message = ('Slug должен содержать только '
               'буквы, цифры, дефисы и подчеркивания.')
    slug_validator = RegexValidator(
        regex=r'^[-a-zA-Z0-9_]+$',
        message=message
    )
    if slug_validator(value):
        raise ValidationError(message)
    return value


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'Неверно указан год создания произведения: {value}'
        )
    return value
