from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import generics, status, exceptions
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, SignUpSerializer, CheckPasswordSerialize
from .models import Profile, Avatar
from django.contrib.auth import logout, login, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from ast import literal_eval


# Профиль
class ProfileApiView(RetrieveUpdateAPIView, LoginRequiredMixin, UserPassesTestMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def test_func(self):
        return self.request.user.id == self.get_object().user.id

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


# Смена пароля
class ChangePasswordApiView(APIView):
    def post(self, request):
        seriazlizer = CheckPasswordSerialize(instance=request.user, data=request.data)
        if seriazlizer.is_valid(raise_exception=True):
            seriazlizer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Вот этот вот не работает
        return Response(status=status.HTTP_403_FORBIDDEN)

#смена аватарки (арботает только если аватар не установлен)
class ChangeAvatar(APIView):
    def post(self, request):
        new_avatar = request.FILES["avatar"]
        profile = Profile.objects.get(user=request.user.id)
        avatar_profile = Avatar.objects.create(profile_id=profile.id, src=new_avatar, alt='ddd')
        return Response(status=status.HTTP_200_OK)


# Регистрация пользователя api/sign-up
class SignUpApiView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        serializer = SignUpSerializer(data=data)
        if User.objects.filter(username=data.get('username', None)):
            return Response('Username allready exist', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            name = data.get('name')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = User.objects.create(username=username, first_name=name)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user, fullName=name)
            login(request, user)
            return Response('Success, registry ok, profile created', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Выход api/Sign-out
class SignOutApiView(APIView):
    def post(self, request, format=None):
        print(request.data)
        logout(request)
        return Response(status=status.HTTP_200_OK)


# SIGN-IN вход в профиль
class SignInApiView(APIView):
    def post(self, request, format=None):
        username = literal_eval(request.body.decode('utf-8')).get('username', None)
        password = literal_eval(request.body.decode('utf-8')).get('password', None)
        user = authenticate(username=username, password=password)  # проверка наличия пользователя
        if user:
            if user.is_active:
                login(request, user)
            else:
                raise exceptions.AuthenticationFailed('User inactive or deleted.')
        else:
            raise exceptions.AuthenticationFailed('Invalid username/password.')
        return Response("Добро пожаловать")
