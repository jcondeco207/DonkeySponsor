from rest_framework import serializers
from . import models

from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import   authenticate
from django.contrib.auth.models import Permission
from axes.models import AccessAttempt

class UserSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.User
            fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'role')
            extra_kwargs = {'password': {'write_only': True}}

      def to_representation(self, instance):
            representation = super().to_representation(instance)
            user = instance

            # Flag if user is blocked
            try:
                  #failures_since_start
                  attempts = AccessAttempt.objects.get(username=user.username)
                  representation['isBlocked'] = attempts.failures_since_start
            except AccessAttempt.DoesNotExist:
                  representation['isBlocked'] = False

            # User Role
            representation['role'] = user.role.name

            return representation

class CreateUserSerializer(serializers.Serializer):
      username = serializers.CharField()
      first_name = serializers.CharField()
      last_name = serializers.CharField()
      email = serializers.CharField()
      password = serializers.CharField()
      role = serializers.CharField()

class RoleSerializer(serializers.Serializer):
      role = serializers.CharField()

class AuthSerializer(serializers.Serializer):
      '''serializer for the user authentication object'''
      username = serializers.CharField()
      password = serializers.CharField(
             style={'input_type': 'password'},
             trim_whitespace=False
      )
      def validate(self, attrs):
            username = attrs.get('username')
            password = attrs.get('password')

            user = authenticate(
                   request=self.context.get('request'),
                   username=username,
                   password=password
            )

            if not user:
                  msg = ('Unable to authenticate with provided credentials')
                  raise serializers.ValidationError(msg, code='authentication')

            attrs['user'] = user
            return

class AuthSerializer2(serializers.Serializer):
      '''serializer for the user authentication object'''
      username = serializers.CharField()
      password = serializers.CharField(
             style={'input_type': 'password'},
             trim_whitespace=False
      )
      authenticator = serializers.CharField()

      def validate(self, attrs):
            username = attrs.get('username')
            password = attrs.get('password')
            authenticator = attrs.get('authenticator')

            user = authenticate(
                   request=self.context.get('request'),
                   username=username,
                   password=password,
                   authenticator=authenticator
            )

            if not user:
                  msg = ('Unable to authenticate with provided credentials')
                  raise serializers.ValidationError(msg, code='authentication')

            attrs['user'] = user
            return

class URLSerializer(serializers.Serializer):
      url = serializers.CharField()

class RoleSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Role
            fields = ('id', 'name')
