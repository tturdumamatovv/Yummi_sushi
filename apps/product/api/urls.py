from apps.product.api.views import ProductListByCategorySlugView, SetListView, CategoryListView, ProductSearchView, ProductBonusView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('product/search/', ProductSearchView.as_view(), name='product-search'),
    path('bonus/', ProductBonusView.as_view(), name='bonus-list'),
    path('category/<slug:slug>/', ProductListByCategorySlugView.as_view(), name='category'),
    path('sets/', SetListView.as_view(), name='set-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
