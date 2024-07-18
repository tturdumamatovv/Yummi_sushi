from apps.product.api.views import ProductListByCategorySlugView, SetListView, CategoryListView, ProductSearchView
from django.urls import path

urlpatterns = [
    path('product/search/', ProductSearchView.as_view(), name='product-search'),

    path('category/<slug:slug>/', ProductListByCategorySlugView.as_view(), name='category'),
    path('sets/', SetListView.as_view(), name='set-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

]
