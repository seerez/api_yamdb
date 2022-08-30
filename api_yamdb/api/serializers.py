from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя недоступно')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Имя занято')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с этим адресом электронной почты уже существует'
            )
        return value


class TokenCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Wrong confirmation_code')
        return RefreshToken.for_user(user).access_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'bio', 'email', 'first_name', 'last_name', 'role', 'username'
        )
