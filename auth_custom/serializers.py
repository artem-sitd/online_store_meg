from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .models import Profile, Avatar
from django.contrib.auth.models import User


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ('src', 'alt')


# Профиль
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

#Смена пароля
class CheckPasswordSerialize(serializers.ModelSerializer):
    currentPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('currentPassword', 'newPassword')

    #СМЕНА ПАРОЛЯ
    def validate(self, attrs):
        user = self.instance
        currentPassword = attrs.pop('currentPassword')
        if not user.check_password(currentPassword):
            raise serializers.ValidationError('Старый пароль неверный')

        return attrs

    # СМЕНА ПАРОЛЯ
    def update(self, instance, validated_data):
        newPassword = validated_data.pop('newPassword')
        instance.set_password(newPassword)
        instance.save()
        return instance
