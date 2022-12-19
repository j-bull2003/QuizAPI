from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import User


class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'username']


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        token, _ = Token.objects.get_or_create(user=user)

        user_serializer = UserSerializer(user)

        response = {
            'token': token.key,
            'user_info': user_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class SignUpAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token, user = serializer.save()
        user_serializer = UserSerializer(user)

        response = {
            'token': token.key,
            'user_info': user_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
