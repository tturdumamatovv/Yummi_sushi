from django.urls import path
from .views import HomePageView, ContactsView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),

]
