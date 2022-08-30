from django.db.models import Avg
from rest_framework import viewsets, filters, mixins, permissions
from reviews.models import Category, Genre, Title, Review
from .serializers import TitlesSerializerMethod, TitlesSerializer, CategorySerializer, GenreSerializer, CommentSerializer, ReviewSerializer
from .pagination import CategoryPagination, GenrePagination, TitlesPagination
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAuthorOrReadOnly


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
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllPermission,)
    pagination_class = GenrePagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class CategoryViewSet(ListCreateDestroyModelViewSet):
    """Вьюсет для Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllPermission,)
    pagination_class = CategoryPagination
    search_fields = ('^name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для Title."""
    queryset = (Title.objects.all())
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    #permission_classes = (IsAuthenticatedOrReadOnly, AdminAllPermission,)
    pagination_class = TitlesPagination
    filter_backends = (filters.SearchFilter,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesSerializer
        return TitlesSerializerMethod


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
