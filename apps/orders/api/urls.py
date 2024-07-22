
from django.urls import path
from .views import CreateOrderView, OrderPreviewView, ReportCreateView

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('order-preview/', OrderPreviewView.as_view(), name='order-preview'),
    path('reports/', ReportCreateView.as_view(), name='create-report'),

]
