from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import NotFound

from apps.product.api.serializers import ProductSerializer, SetSerializer
from apps.product.models import Category, Product, Set


# Create your views here.
class ProductListByCategorySlugView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise NotFound("Категория не найдена")
        return Product.objects.filter(category=category)


class SetListView(generics.ListAPIView):
    serializer_class = SetSerializer

    def get_queryset(self):
        return Set.objects.prefetch_related(
            'products__product__ingredients',
            'products__product__toppings',
            'products__size'
        )
