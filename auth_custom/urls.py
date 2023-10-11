from django.urls import path
from .views import ProfileApiView, SignUpApiView

urlpatterns = [path('profile/', ProfileApiView.as_view()),
               path('sign-up/', SignUpApiView.as_view())

               ]
