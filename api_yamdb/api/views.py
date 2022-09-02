from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from reviews.models import Category, Genre, Review, Title, Comments

from .pagination import CategoryPagination, GenrePagination, TitlesPagination
from .permissions import (AdminOrSuperuserOnly, AuthenticatedOrReadOnly,
                          AdminOrReadOnly
                          )
from .serializers import (CategorySerializer, CommentsSerializerMethod,
                          GenreSerializer, ReviewSerializer, TitlesSerializer,
                          TitlesSerializerMethod, TokenCreateSerializer,
                          UserSerializer, UserSignUpSerializer)
from users.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter


class UserSignUpViewSet(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = get_random_string(length=30)
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            'Subject',
            f'Your confirmation code {confirmation_code}',
            'admin@example.com',
            [serializer.validated_data['email']],
        )
        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK
        )


class TokenCreateViewSet(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            data={'access': str(serializer.validated_data)},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated & AdminOrSuperuserOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            serializer.validated_data.pop('role')
        serializer.save()
        return Response(serializer.data)


class ListCreateDestroyModelViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """
    Кастомный базовый вьюсет:
    Вернуть список объектов (для обработки запросов GET);
    Создать объект (для обработки запросов POST);
    Удалить объект (для обработки запросов DELETE).
    """
    pass


class GenreViewSet(ListCreateDestroyModelViewSet):
    """Вьюсет для Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = GenrePagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CategoryViewSet(ListCreateDestroyModelViewSet):
    """Вьюсет для Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = CategoryPagination
    search_fields = ('^name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для Title."""
    queryset = Title.objects.annotate(rating=Avg('review__score')).all()
    permission_classes = (AdminOrReadOnly,)
    pagination_class = TitlesPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesSerializer
        return TitlesSerializerMethod


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""
    serializer_class = CommentsSerializerMethod
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        return Comments.objects.filter(
            title=get_object_or_404(
                Title, pk=self.kwargs.get('title_id')),
            review=get_object_or_404(
                Review, pk=self.kwargs.get('review_id'))
        ).all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review, title=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
