from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile
from django.contrib.auth.models import User


# Инфо о всех профилях
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


# Регистрация пользователя sign-up
class SignUpSerializer(serializers.ModelSerializer):

    # first_name = serializers.CharField(required=True, max_length=50)
    # username = serializers.CharField(required=True,
    #                                  validators=[UniqueValidator(queryset=User.objects.all())])
    # password = serializers.CharField(write_only=True, required=True,
    #                                  validators=[validate_password], style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name')

