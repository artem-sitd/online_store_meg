from rest_framework import generics, status, exceptions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import ProfileSerializer, SignUpSerializer
from .models import Profile
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout, login
from rest_framework.response import Response
from rest_framework.views import APIView


# Все профили пользователей
class ProfileApiView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Регистрация пользователя api/sign-up
class SignUpApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


# Выход api/Sign-out
class SignOutApiView(generics.views.APIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class MyBasicAuthentication(BasicAuthentication):

    def authenticate(self, request):
        user = super(MyBasicAuthentication, self).authenticate(request)
        login(request, user)
        return user

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


