from .views import TagsListApiView
from django.urls import path

urlpatterns = [path('tags/', TagsListApiView.as_view()),

               ]
