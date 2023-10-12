from django.shortcuts import render
from rest_framework import generics, status
from .serializers import ProfileSerializer, SignUpSerializer
from .models import Profile
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from rest_framework.response import Response


# Все профили пользователей
class ProfileApiView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Регистрация пользователя
class SignUpApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

# Sign-out
class SignOutApiView(generics.views.APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)
