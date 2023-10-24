from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from rest_framework import generics, status, exceptions
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from django.contrib.auth.models import User

from .serializers import ProfileSerializer, SignUpSerializer
from .models import Profile, Avatar
from django.contrib.auth import logout, login, authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from ast import literal_eval


# Все профили пользователей
class ProfileApiView(RetrieveUpdateAPIView, LoginRequiredMixin, UserPassesTestMixin):
    permission_classes = [IsAuthenticated]
    success_url = reverse_lazy('auth_custom:profile')
    serializer_class = ProfileSerializer

    def test_func(self):
        return self.request.user.id == self.get_object().user.id

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


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
