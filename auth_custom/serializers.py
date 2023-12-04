from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("src", "alt")


# Профиль
class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False)

    class Meta:
        model = Profile
        fields = ("fullName", "email", "phone", "avatar")


# Регистрация пользователя sign-up
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "first_name")


# Смена пароля
class CheckPasswordSerialize(serializers.ModelSerializer):
    currentPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("currentPassword", "newPassword")

    # СМЕНА ПАРОЛЯ
    def validate(self, attrs: OrderedDict) -> OrderedDict:
        user = self.instance
        currentPassword = attrs.pop("currentPassword")
        if not user.check_password(currentPassword):
            raise serializers.ValidationError("Старый пароль неверный")

        return attrs

    # СМЕНА ПАРОЛЯ
    def update(self, instance: User, validated_data: dict) -> User:
        newpassword = validated_data.pop("newPassword")
        instance.set_password(newpassword)
        instance.save()
        return instance
