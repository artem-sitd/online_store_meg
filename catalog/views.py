from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer, ProductSerializer
from product.models import Product, Reviews, ProductImage
from rest_framework.response import Response


class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Все продукты с использованием сериализатора, но так не рботает пагинация
class ProductApiView(APIView):
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        queryset = Product.objects.all()
        # fields = [{'id': i.pk,
        #            'category': i.category.id,
        #            'price': i.price,
        #            'count': i.count,
        #            'date': i.date,
        #            'title': i.title,
        #            'description': i.description,
        #            'free_delivery': i.free_delivery,
        #            'images': [{'src': str(image.src),
        #                        'alt': image.alt} for image in
        #                       ProductImage.objects.filter(product_id=i.pk)],
        #            'tags': [{'id': t.id, 'name': t.name}
        #                     for j in Product.objects.filter(id=i.pk)
        #                     for t in j.tags.all()],
        #            'reviews': len(Reviews.objects.filter(product_id=i.pk)),
        #            'rating': i.rating,
        #            }
        #           for i in queryset],

        #Второй способ (оба работают)
        dict_fields=[]
        new_fields={}
        for i in queryset:
            new_fields['id']=i.pk
            new_fields['category']=i.category.id
            new_fields['price']=i.price
            new_fields['count']=i.count
            new_fields['date']=i.date
            new_fields['title']=i.title
            new_fields['description']=i.description
            new_fields['free_delivery']=i.free_delivery
            new_fields['images']=[{'src': str(image.src),
                               'alt': image.alt} for image in
                              ProductImage.objects.filter(product_id=i.pk)]
            new_fields['tags']=[{'id': t.id, 'name': t.name}
                            for j in Product.objects.filter(id=i.pk)
                            for t in j.tags.all()],
            new_fields['reviews']=len(Reviews.objects.filter(product_id=i.pk))
            new_fields['rating']=i.rating
            dict_fields.append(new_fields)
        paginator=Paginator(dict_fields, 2)
        return Response({'items': dict_fields, 'currentPage': 'currentPage', 'lastPage': 'lastPage'})

class TestApi(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer