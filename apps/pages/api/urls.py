from django.urls import path
from .views import (
    HomePageView,
    ContactsView,
    StaticPageDetailView,
    LayOutView,
    BannersView
)

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('static-pages/<slug:slug>/', StaticPageDetailView.as_view(), name='static-page-detail'),
    path('banners/', BannersView.as_view(), name='banners'),

    path('static-pages/about-us/', StaticPageDetailView.as_view(), name='about-us-page'),
    path('static-pages/delivery/', StaticPageDetailView.as_view(), name='about-us-page'),
    path('layout/', LayOutView.as_view(), name='layout'),
]
