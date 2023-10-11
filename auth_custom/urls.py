from django.urls import path
from .views import ProfileApiView

urlpatterns = [path('profile/', ProfileApiView.as_view())

               ]
