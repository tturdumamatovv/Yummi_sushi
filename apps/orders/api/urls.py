from django.urls import path
from .views import (
    CreateOrderView,
    OrderPreviewView,
    ReportCreateView,
    RestaurantListView,
    ListOrderView,
    PromoCodeDetailView,
    CreateReOrderView,
    GetMinOrderAmountView,
    get_user_orders,
    get_order_details
)

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', ListOrderView.as_view(), name='order-list'),
    path('order-preview/', OrderPreviewView.as_view(), name='order-preview'),
    path('reports/', ReportCreateView.as_view(), name='create-report'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('promocode/<str:code>/', PromoCodeDetailView.as_view(), name='promocode-detail'),
    path('reorder/<int:order_id>/', CreateReOrderView.as_view(), name='reorder'),
    path('min-order-amount/', GetMinOrderAmountView.as_view(), name='min-order-amount'),
    path('user/orders/', get_user_orders, name='user_orders'),
    path('details/', get_order_details, name='get_order_details'),
]
