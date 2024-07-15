from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.pages.models import Banner, MainPage, Contacts
from apps.product.models import Category
from apps.pages.api.serializers import HomePageSerializer, ContactsSerializer


class HomePageView(generics.GenericAPIView):
    serializer_class = HomePageSerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        banners = Banner.objects.filter(is_active=True)
        main_page = MainPage.objects.first()

        serializer = self.get_serializer({'categories': categories, 'banners': banners, 'main_page': main_page})
        return Response(serializer.data)


class ContactsView(generics.GenericAPIView):
    serializer_class = ContactsSerializer

    def get(self, request, *args, **kwargs):
        contacts = Contacts.objects.first()
        serializer = self.get_serializer(contacts)
        return Response(serializer.data)