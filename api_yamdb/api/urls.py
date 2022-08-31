from django.urls import path, include
from rest_framework import DefaultRouter
from .views import GenreViewSet, CategoryViewSet, TitlesViewSet, CommentViewSet, ReviewViewSet, UserSignUpViewSet, TokenCreateViewSet, UserViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(
    'review',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'^review/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitlesViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', UserSignUpViewSet.as_view()),
    path('v1/auth/token/', TokenCreateViewSet.as_view()),
]
