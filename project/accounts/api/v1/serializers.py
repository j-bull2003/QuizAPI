from django.contrib.auth import authenticate
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.db.models import Avg

from accounts.models import User
from quiz.models import Quiz

# This code defines three serializers for a Django project: UserSerializer, LoginSerializer, and RegisterSerializer. 
# Serializers are used to convert Django models and querysets into JSON format and vice versa.

# The UserSerializer class is a subclass of serializers.ModelSerializer, which is a class provided by Django Rest framework that allows you to serialize Django models.
class UserSerializer(serializers.ModelSerializer):

    # The avg_score field is calculated by filtering the Quiz model by the user and aggregating the average score.
    avg_score = serializers.SerializerMethodField(label='Average Score', read_only=True, method_name='get_avg_score')

    # The completed_quizzes field is calculated by filtering the Quiz model by the user and counting the number of quizzes. 
    completed_quizzes = serializers.SerializerMethodField(label='Completed Quizzes', read_only=True,
                                                          method_name='get_completed_quizzes')

    def get_avg_score(self, obj):
        avg_score = Quiz.objects.filter(user=obj, score__isnull=False).aggregate(Avg('score'))['score__avg']
        return 0 if avg_score is None else avg_score

    def get_completed_quizzes(self, obj):
        return Quiz.objects.filter(user=obj, score__isnull=False).count()

    # The Meta class specifies the User model and the fields that should be included in the serialized representation of a User object.
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'date_joined',
            'avg_score',
            'completed_quizzes'
        ]

# The LoginSerializer class is a subclass of serializers.Serializer, which is a class provided by Django Rest framework that allows you to define custom serializers. 
class LoginSerializer(serializers.Serializer):

    # The LoginSerializer class defines two fields: username and password, and it includes a validate method that authenticates the user using the provided credentials. 
    username = serializers.CharField(label=_('Username'), required=True)
    password = serializers.CharField(label=_('Password'), required=True)

    # If the authentication is successful, the validate method returns the authenticated user. 
    def validate(self, attrs: dict):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(self.context['request'], username=username, password=password)

        # If the authentication fails, it raises a validation error.
        if not user:
            raise serializers.ValidationError(_('Invalid credentials!'))

        attrs.update({'user': user})
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

# The RegisterSerializer class is also a subclass of serializers.Serializer
class RegisterSerializer(serializers.Serializer):

    # The RegisterSerializer class defines two fields: username and password, and it includes a create method that creates a new user using the provided credentials. 
    username = serializers.CharField(label=_('Username'), required=True, write_only=True)
    password = serializers.CharField(label=_('Password'), required=True, write_only=True)

    # The create method sets the password for the new user and saves the user to the database. 
    def create(self, validated_data):
        username = validated_data.pop('username', '')
        password = validated_data.pop('password', '')

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        # It also creates a token for the user using the Token model.
        user_token, _ = Token.objects.get_or_create(user=user)

        return user_token, user

    def update(self, instance, validated_data):
        pass
