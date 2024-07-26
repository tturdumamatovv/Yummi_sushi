from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.product.models import Category
from apps.pages.models import (
    Banner,
    MainPage,
    Contacts,
    StaticPage
)
from apps.pages.api.serializers import (
    HomePageSerializer,
    ContactsSerializer,
    StaticPageSerializer,
    LayOutSerializer,
    BannerSerializer
)


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


class StaticPageDetailView(generics.RetrieveAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        instance = None

        try:
            instance = StaticPage.objects.get(slug=slug)
        except StaticPage.DoesNotExist:
            if slug == 'about-us':
                instance = StaticPage.objects.create(
                    title='О нас',
                    title_ru='О нас',
                    title_ky='Биз жөнүндө',

                    description='О нас',
                    description_ru='О нас',
                    description_ky='Биз жөнүндө',
                    slug="about-us"
                )
            elif slug == 'delivery':
                instance = StaticPage.objects.create(
                    title='Доставка',
                    title_ru='Доставка',
                    title_ky='Доставка',

                    description='Доставка',
                    description_ru='Доставка',
                    description_ky='Доставка',
                    slug="delivery"
                )

        return instance

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LayOutView(generics.ListAPIView):
    queryset = MainPage.objects.all()
    serializer_class = LayOutSerializer


class BannersView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True).order_by('-created_at')

    def get_serializer(self, *args, **kwargs):
        return BannerSerializer(*args, **kwargs, context={'request': self.request})
