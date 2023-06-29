import secrets
import string

from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .serializers import SignUpSerializer, TokenSerializer


CODE_LENGTH = 13

EMAIL_SUBJECT = 'YAMDB: Код подтверждения регистрации.'
EMAIL_TEXT = 'Ваш код подтверждения: {confirmation_code}'
EMAIL_FROM = 'pupkin@yamdb.ru'

USER_EXISTS = 'Данный пользователь уже существует.'
USER_NOT_FOUND = (
    'Такой пользователя не найден.\n'
    'Проверьте ваш логин и код подтверждения.'
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
        raise serializer.ValidationError(USER_EXISTS)
    confirmation_code = ''.join(secrets.choice(
        string.ascii_letters + string.digits) for i in range(CODE_LENGTH))
    user.confirmation_code = confirmation_code  # нужно поле добавить в модели
    user.save
    send_mail(
        EMAIL_SUBJECT,
        EMAIL_TEXT.format(confirmation_code=user.confirmation_code),
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
        'token': AccessToken.for_user(user),
    }
    return Response(token, status=status.HTTP_200_OK)
