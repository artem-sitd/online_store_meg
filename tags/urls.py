from django.urls import path

from .views import TagsListApiView

urlpatterns = [
    path("tags/", TagsListApiView.as_view()),
]
