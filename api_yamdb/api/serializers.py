from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from rewiews.models import Category, Genre, Title
from .validators import validate_slug, validate_year


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[validate_slug]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[validate_slug]
    )

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
