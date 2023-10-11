from django.urls import path
from .views import ProductDetailReview, ProductDetailApiView

urlpatterns = [
    path('product/<int:pk>/', ProductDetailApiView.as_view()),
    path('product/<int:pk>/review/', ProductDetailReview.as_view())
]
