from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import User

# This code defines three views for a Django application: UserListAPIView, LoginAPIView, and SignUpAPIView.

# The UserListAPIView class is a subclass of ListAPIView, which is a class provided by Django Rest framework that allows you to list the objects of a model.
class UserListAPIView(ListAPIView):

    # The UserListAPIView class sets the permission_classes attribute to [IsAuthenticated], which specifies that only authenticated users can access the view. 
    permission_classes = [IsAuthenticated]

    # The queryset attribute is set to User.objects.all(), which specifies that all User objects should be returned by the view. 
    queryset = User.objects.all()

    # The serializer_class attribute is set to UserSerializer, which specifies that the UserSerializer class should be used to serialize the User objects.
    serializer_class = UserSerializer

    # The filterset_fields attribute specifies which fields of the User model can be used to filter the queryset.
    filterset_fields = ['id', 'username']

# The LoginAPIView class is a subclass of GenericAPIView, which is a class provided by Django Rest framework that allows you to create custom views. 
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    # The LoginAPIView class defines a post method that handles HTTP POST requests. 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # The post method gets a LoginSerializer instance and calls its is_valid method with the raise_exception parameter set to True
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')

        # If the serializer is valid, the post method gets the authenticated user from the validated_data attribute of the serializer and creates a token for the user using the Token model.
        token, _ = Token.objects.get_or_create(user=user)

        user_serializer = UserSerializer(user)

        # # The post method then serializes the user using the UserSerializer class and returns a response with the token and the serialized user data.
        response = {
            'token': token.key,
            'user_info': user_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

# The SignUpAPIView class is also a subclass of GenericAPIView. The SignUpAPIView class defines a post method that handles HTTP POST requests. 
class SignUpAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    # The post method gets a RegisterSerializer instance and calls its is_valid method with the raise_exception parameter set to True.
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #  If the serializer is valid, the post method calls the save method of the serializer to create a new user and a token for the user. 
        token, user = serializer.save()
        user_serializer = UserSerializer(user)

        # The post method then serializes the user using the UserSerializer class and returns a response with the token and the serialized user data.
        response = {
            'token': token.key,
            'user_info': user_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

        # In summary, these views provide functionality for listing users, logging in, and signing up in a Django application. 
        # The views use serializers to convert model objects and request data into JSON format and vice versa.
