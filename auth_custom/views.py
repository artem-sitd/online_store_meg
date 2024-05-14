from ast import literal_eval

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from rest_framework import exceptions, status
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from basket.models import Basket

from .models import Avatar, Profile
from .serializers import CheckPasswordSerialize, ProfileSerializer, SignUpSerializer


# Профиль
class ProfileApiView(APIView, LoginRequiredMixin, UserPassesTestMixin):
    permission_classes = [IsAuthenticated]

    def test_func(self):
        return self.request.user.id == self.get_object().user.id

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get(self, request: Request) -> Response:
        if request.user.id is None:
            return Response(status=200)
        serialized = ProfileSerializer(Profile.objects.get(user=request.user.id))
        return Response(serialized.data, status=200)

    def post(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user.id)
        email = request.data["email"]
        phone = request.data["phone"]
        fullname = request.data["fullName"]
        profile.email = email
        profile.phone = phone
        profile.fullName = fullname
        profile.save()
        return Response(status=status.HTTP_200_OK)


# Смена пароля
class ChangePasswordApiView(APIView):
    def post(self, request: Request) -> Response:
        seriazlizer = CheckPasswordSerialize(instance=request.user, data=request.data)
        if seriazlizer.is_valid(raise_exception=True):
            seriazlizer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


# смена аватарки (работает только если аватар не установлен)
class ChangeAvatar(APIView):
    def post(self, request: Request) -> Response:
        new_avatar = request.FILES["avatar"]
        profile = Profile.objects.get(user=request.user.id)
        avatar_profile = Avatar.objects.create(
            profile_id=profile.id, src=new_avatar, alt="ddd"
        )
        return Response(status=status.HTTP_200_OK)


# Регистрация пользователя api/sign-up
class SignUpApiView(APIView):
    def post(self, request: Request) -> Response:
        data = None
        for i in request.data.dict():
            data = json.loads(i)
        serializer = SignUpSerializer(data=data)
        if User.objects.filter(username=data.get("username", None)):
            return Response(
                "Username allready exist", status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            name = data.get("name")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = User.objects.create(username=username, first_name=name)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user, fullName=name)
            Basket.objects.create(user=user)
            login(request, user)
            return Response(
                "Success, registry ok, profile created", status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Выход api/Sign-out
class SignOutApiView(APIView):
    def post(self, request: Request, format=None) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


# SIGN-IN вход в профиль
class SignInApiView(APIView):
    def post(self, request, format=None) -> Response:

        username = literal_eval(request.body.decode("utf-8")).get("username", None)
        password = literal_eval(request.body.decode("utf-8")).get("password", None)
        user = authenticate(
            username=username, password=password
        )  # проверка наличия пользователя
        if user:
            if user.is_active:
                login(request, user)
            else:
                raise exceptions.AuthenticationFailed("User inactive or deleted.")
        else:
            raise exceptions.AuthenticationFailed("Invalid username/password.")
        return Response("Добро пожаловать")
