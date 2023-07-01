from rest_framework import serializers

from reviews.models import (
    User,
    CODE_LENGTH, REGEX, USER_NAME_LENGTH
)


FORBIDDEN_NAME = 'Имя "me" использовать нельзя!'


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(FORBIDDEN_NAME)
        return name


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=REGEX,
        max_length=USER_NAME_LENGTH,
    )
    confirmation_code = serializers.CharField(
        max_length=CODE_LENGTH,
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
