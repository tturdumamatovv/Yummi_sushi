import django_filters

from apps.product.models import Product


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['title']
