from rest_framework import serializers
from .models import Profile, Avatar
from django.contrib.auth.models import User


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ('src', 'alt')


# Инфо о всех профилях
class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False)

    class Meta:
        model = Profile
        fields = ('fullName', 'email', 'phone', 'avatar')


# Регистрация пользователя sign-up
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name')
