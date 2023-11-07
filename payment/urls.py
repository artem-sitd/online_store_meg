from django.urls import path, include
from .views import PaymentApiView

urlpatterns = [path('payment/<int:id>', PaymentApiView.as_view()),
               path('payment-someone', PaymentApiView.as_view()),
               ]
