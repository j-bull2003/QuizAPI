from django.contrib.auth import authenticate
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.db.models import Avg

from accounts.models import User
from quiz.models import Quiz


class UserSerializer(serializers.ModelSerializer):
    avg_score = serializers.SerializerMethodField(label='Average Score', read_only=True, method_name='get_avg_score')
    completed_quizzes = serializers.SerializerMethodField(label='Completed Quizzes', read_only=True,
                                                          method_name='get_completed_quizzes')

    def get_avg_score(self, obj):
        avg_score = Quiz.objects.filter(user=obj, score__isnull=False).aggregate(Avg('score'))['score__avg']
        return 0 if avg_score is None else avg_score

    def get_completed_quizzes(self, obj):
        return Quiz.objects.filter(user=obj, score__isnull=False).count()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'date_joined',
            'avg_score',
            'completed_quizzes'
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'), required=True)
    password = serializers.CharField(label=_('Password'), required=True)

    def validate(self, attrs: dict):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(self.context['request'], username=username, password=password)

        if not user:
            raise serializers.ValidationError(_('Invalid credentials!'))

        attrs.update({'user': user})
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'), required=True, write_only=True)
    password = serializers.CharField(label=_('Password'), required=True, write_only=True)

    def create(self, validated_data):
        username = validated_data.pop('username', '')
        password = validated_data.pop('password', '')

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        user_token, _ = Token.objects.get_or_create(user=user)

        return user_token, user

    def update(self, instance, validated_data):
        pass
