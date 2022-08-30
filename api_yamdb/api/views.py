from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import views, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import (
    AdminOrSuperuserOnly
)
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    TokenCreateSerializer
)

User = get_user_model()


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
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if serializer.validated_data.get('role'):
                    serializer.validated_data.pop('role')
                serializer.save()
                return Response(serializer.data)
