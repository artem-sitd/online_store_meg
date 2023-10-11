from django.shortcuts import render
from rest_framework import generics
from .serializers import ProfileSerializer, SignUpSerializer
from .models import Profile
from rest_framework.permissions import AllowAny


class ProfileApiView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SignUpApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
