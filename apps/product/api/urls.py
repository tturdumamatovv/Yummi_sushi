from django.urls import path, include

from apps.product.api.views import ProductListByCategorySlugView, SetListView

urlpatterns = [
    path('category/<slug:slug>/', ProductListByCategorySlugView.as_view(), name='category'),
    path('sets/', SetListView.as_view(), name='set-list'),

]