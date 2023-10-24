from django.urls import path
from .views import CategoryListApi, ProductApiView

urlpatterns = [path('categories/', CategoryListApi.as_view()),
               path('catalog/', ProductApiView.as_view()),
               ]
