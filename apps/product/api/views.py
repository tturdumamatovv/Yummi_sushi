from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, response
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.product.api.filters import ProductFilter
from apps.product.api.serializers import ProductSerializer, CategoryProductSerializer, \
    CategoryOnlySerializer, ProductSizeWithBonusSerializer, \
    ProductSizeIdListSerializer  # , SetSerializer
from apps.product.models import Category, Product, ProductSize  # Set


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductBonusView(generics.ListAPIView):
    queryset = ProductSize.objects.filter(
        product__bonuses=True,
        bonus_price__gt=0
    )
    serializer_class = ProductSizeWithBonusSerializer


class ProductListByCategorySlugView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise NotFound("Категория не найдена")

        products = Product.objects.filter(category=category, product_sizes__isnull=False).distinct().order_by('order')
        # sets = Set.objects.filter(category=category)

        product_serializer = ProductSerializer(products, many=True, context={'request': request})
        # set_serializer = SetSerializer(sets, many=True, context={'request': request})

        return Response({
            'products': product_serializer.data,
            # 'sets': set_serializer.data
        })


# class SetListView(generics.ListAPIView):
#     serializer_class = SetSerializer
#
#     def get_queryset(self):
#         return Set.objects.prefetch_related(
#             'products__product__ingredients',
#             'products__product__toppings',
#             'products__size'
#         )


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryProductSerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.prefetch_related('products', 'sets').all()
        serializer = CategoryProductSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryOnlyListView(generics.ListAPIView):
    serializer_class = CategoryOnlySerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategoryOnlySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


class PopularProducts(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_popular=True)


class CheckProductSizes(APIView):
    def post(self, request):
        serializer = ProductSizeIdListSerializer(data=request.data)
        if serializer.is_valid():
            size_ids = serializer.validated_data['sizes']
            # Получаем нужные объекты из базы данных
            sizes = ProductSize.objects.filter(id__in=size_ids).select_related('product', 'size')
            response_data = {}

            for size in sizes:
                # Добавляем ID размера и актуальную цену в ответ
                response_data[size.id] = size.get_price() or None

            # Добавляем те ID размеров, которые не были найдены в базе данных, со значением None
            missing_sizes = set(size_ids) - set(response_data.keys())
            response_data.update({size_id: None for size_id in missing_sizes})

            return Response(response_data)

        return Response(serializer.errors, status=400)