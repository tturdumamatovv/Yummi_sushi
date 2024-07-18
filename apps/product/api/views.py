from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.product.api.filters import ProductFilter
from apps.product.api.serializers import ProductSerializer, SetSerializer, CategoryProductSerializer
from apps.product.models import Category, Product, Set


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductListByCategorySlugView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise NotFound("Категория не найдена")

        products = Product.objects.filter(category=category)
        sets = Set.objects.filter(category=category)

        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        set_serializer = SetSerializer(sets, many=True, context={'request': request})

        return Response({
            'products': product_serializer.data,
            'sets': set_serializer.data
        })


class SetListView(generics.ListAPIView):
    serializer_class = SetSerializer

    def get_queryset(self):
        return Set.objects.prefetch_related(
            'products__product__ingredients',
            'products__product__toppings',
            'products__size'
        )


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryProductSerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.prefetch_related('products', 'sets').all()
        serializer = CategoryProductSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)
