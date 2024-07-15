from django.urls import path, include

from apps.product.api.views import ProductListByCategorySlugView

urlpatterns = [
    path('category/<slug:slug>/', ProductListByCategorySlugView.as_view(), name='category'),
]