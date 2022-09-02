from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comments, Genre, Review, Title

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
            raise serializers.ValidationError('Неверный код подтверждения')
        return RefreshToken.for_user(user).access_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'bio', 'email', 'first_name', 'last_name', 'role', 'username'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода информации."""
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitlesSerializerMethod(serializers.ModelSerializer):
    """Сериалайзер для изменения информации."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        required=True,
        many=False,
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        required=True,
        many=True,
        queryset=Genre.objects.all(),
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class CommentsSerializerMethod(serializers.ModelSerializer):
    """Сериалайзер для комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
