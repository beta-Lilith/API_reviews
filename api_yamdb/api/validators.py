from django.core.exceptions import ValidationError
from django.utils import timezone

ERROR_MESSAGE = 'Неверно указан год создания произведения: {value}'


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(ERROR_MESSAGE.format(value=value))
    return value
