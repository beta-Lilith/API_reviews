from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category, Comment, Genre, Review, Title, User,
    CODE_LENGTH, EMAIL_LENGTH, REGEX, USER_NAME_LENGTH,
)
from .validators import validate_year


FORBIDDEN_NAME = 'Имя me использовать нельзя!'
NOT_UNIQUE_REVIEW = 'Вы не можете добавить более одного отзыва на произведение'


class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.RegexField(
        regex=REGEX,
        max_length=USER_NAME_LENGTH,
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
    )

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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
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


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Нельзя повторно комментировать отзыв!')
        return data

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date')
