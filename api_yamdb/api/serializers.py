from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category, Genre, Title, User,
    CODE_LENGTH, REGEX, USER_NAME_LENGTH,
)
from .validators import validate_year


FORBIDDEN_NAME = 'Имя me использовать нельзя!'


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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ShowTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    # rating = serializers.IntegerField(read_only=True, source='')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField(
        validators=[validate_year]
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
