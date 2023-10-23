from django.urls import path, include
from .views import ProfileApiView, SignUpApiView, SignOutApiView, SignInApiView

urlpatterns = [path('profile/', ProfileApiView.as_view()),
               path('sign-up', SignUpApiView.as_view()),
               path('sign-in', SignInApiView.as_view()),
               path('sign-out', SignOutApiView.as_view(), name='sign-out'),
               ]
