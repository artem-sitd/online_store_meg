from django.urls import path
from .views import CategoryListApi, ProductApiView,LimitedProductsApiView, BannersApiView

urlpatterns = [path('categories/', CategoryListApi.as_view()),
               path('catalog/', ProductApiView.as_view()),
               # path('products/popular/', ),
               path('products/limited', LimitedProductsApiView.as_view()),
               # path('sales', ...),
               path('banners', BannersApiView.as_view()),

               ]
