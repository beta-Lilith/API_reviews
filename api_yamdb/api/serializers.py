from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    EMAIL_LENGTH, USER_NAME_LENGTH,
    Category, Comment, Genre, Review, Title, User,
)
from reviews.validators import validate_username, validate_year


NOT_UNIQUE_REVIEW = 'Вы не можете добавить более одного отзыва на произведение'


class SignUpSerializer(serializers.Serializer):
    """Сериализация данных для регистрации."""

    username = serializers.CharField(
        required=True,
        max_length=USER_NAME_LENGTH,
        validators=(validate_username,),
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_LENGTH,
    )


class TokenSerializer(serializers.Serializer):
    """Сериализация данных для получения токена."""

    username = serializers.CharField(
        required=True,
        max_length=USER_NAME_LENGTH,
        validators=(validate_username,),
    )
    confirmation_code = serializers.CharField(
        required=True,
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, name):
        validate_username(name)
        return name


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация данных для категорий."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация данных для жанров."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class ShowTitleSerializer(serializers.ModelSerializer):
    """Сериализация данных для отображения произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(
        many=True,
    )
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = fields


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация данных для произведений."""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    year = serializers.IntegerField(
        validators=(validate_year,),
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация данных для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(
                title=get_object_or_404(
                    Title,
                    id=self.context['view'].kwargs.get('title_id')
                ),
                author=request.user
            ).exists():
                raise serializers.ValidationError(NOT_UNIQUE_REVIEW)
        return data

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация данных для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
