from django.urls import path
from django.contrib.auth import views
from .views import ProfileApiView, SignUpApiView, SignOutApiView

urlpatterns = [path('profile/', ProfileApiView.as_view()),
               path('sign-up/', SignUpApiView.as_view()),
               path('sign-in/', views.LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
               path('sign-out/', SignOutApiView.as_view(), name='sign-out'),

               ]
