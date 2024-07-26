from django.urls import path
from .views import (
    CreateOrderView,
    OrderPreviewView,
    ReportCreateView,
    RestaurantListView,
    ListOrderView
)

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', ListOrderView.as_view(), name='order-list'),
    path('order-preview/', OrderPreviewView.as_view(), name='order-preview'),
    path('reports/', ReportCreateView.as_view(), name='create-report'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
]
