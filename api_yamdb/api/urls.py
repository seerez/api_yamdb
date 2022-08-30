from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserSignUpViewSet, TokenCreateViewSet, UserViewSet

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', UserSignUpViewSet.as_view()),
    path('v1/auth/token/', TokenCreateViewSet.as_view()),
    path('v1/', include(v1_router.urls))
]
