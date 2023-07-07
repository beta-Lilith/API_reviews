import re

from django.core.exceptions import ValidationError
from django.utils import timezone


REGEX = r'^[\w.@+-]+'
NOT_ALLOWED_NAME = 'me'
FORBIDDEN_NAME = 'Имя {name} использовать нельзя!'
NOT_REGEX_NAME = (
    'Можно использовать только буквы, символы {allowed_chars} и цифры, '
    'вы использовали: {used_chars}'
)
ERROR_MESSAGE = 'Неверно указан год создания произведения: {value}'


def check_regex(REGEX):
    allowed_chars = ''
    for symbol in range(256):
        char = chr(symbol)
        if re.match(REGEX, char) and re.match(r'\W', char):
            allowed_chars += char
    return allowed_chars


def validate_username(name):
    if name == NOT_ALLOWED_NAME:
        raise ValidationError(FORBIDDEN_NAME.format(name=NOT_ALLOWED_NAME))
    used_wrong_chars = ' '.join(re.sub(REGEX, '', name))
    if used_wrong_chars:
        allowed_chars = ' '.join(check_regex(REGEX))
        raise ValidationError(
            NOT_REGEX_NAME.format(
                allowed_chars=allowed_chars,
                used_chars=used_wrong_chars,
            )
        )


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(ERROR_MESSAGE.format(value=value))
    return value
