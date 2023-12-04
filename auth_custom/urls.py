from django.urls import path

from .views import (
    ChangeAvatar,
    ChangePasswordApiView,
    ProfileApiView,
    SignInApiView,
    SignOutApiView,
    SignUpApiView,
)

urlpatterns = [
    path("profile", ProfileApiView.as_view(), name="profile"),
    path("profile/password", ChangePasswordApiView.as_view(), name="change_password"),
    path("profile/avatar", ChangeAvatar.as_view(), name="change_avatar"),
    path("sign-up", SignUpApiView.as_view(), name="sign-up"),
    path("sign-in", SignInApiView.as_view(), name="sign-in"),
    path("sign-out", SignOutApiView.as_view(), name="sign-out"),
]
