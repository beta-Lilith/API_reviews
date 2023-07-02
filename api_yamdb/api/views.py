from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import filters, mixins, status, serializers, viewsets
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, User
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ShowTitleSerializer,
                          SignUpSerializer, TokenSerializer)


CODE_LENGTH = 13

EMAIL_SUBJECT = 'YAMDB: Код подтверждения регистрации.'
EMAIL_TEXT = '{username}! Ваш код подтверждения: {confirmation_code}'
EMAIL_FROM = 'pupkin@yamdb.ru'

USER_EXISTS = 'Данный пользователь уже существует.'
USER_NOT_FOUND = (
    'Такой пользователя не найден. Проверьте ваш логин и код подтверждения.'
)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, created = User.objects.get_or_create(username=username, email=email)
    if not created:
        raise serializers.ValidationError(USER_EXISTS)
    send_mail(
        EMAIL_SUBJECT,
        EMAIL_TEXT.format(
            username=username,
            confirmation_code=user.confirmation_code
        ),
        EMAIL_FROM,
        [user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    try:
        user = User.objects.get(
            username=username, confirmation_code=confirmation_code
        )
    except User.DoesNotExist:
        return Response(USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
    token = {
        'token': str(AccessToken.for_user(user)),
    }
    return Response(token, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = (ShowTitleSerializer, TitleSerializer)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShowTitleSerializer
        return TitleSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name', )
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name', )
    lookup_field = 'slug'
