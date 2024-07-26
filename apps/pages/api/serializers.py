from rest_framework import serializers

from apps.product.models import Category
from apps.orders.models import PercentCashback
from apps.pages.models import (
    Banner,
    OrderTypes,
    MainPage,
    Phone,
    Email,
    SocialLink,
    Address,
    PaymentMethod,
    Contacts,
    StaticPage
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'name', 'description', 'image']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'image_desktop', 'image_mobile', 'link', 'is_active', 'created_at']


class OrderTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTypes
        fields = ['title', 'description', 'image']


class MainPageSerializer(serializers.ModelSerializer):
    order_types = OrderTypesSerializer(many=True, read_only=True)
    delivery_conditions = OrderTypesSerializer(many=True, read_only=True)
    methods_of_payment = OrderTypesSerializer(many=True, read_only=True)

    class Meta:
        model = MainPage
        fields = ['icon', 'phone', 'meta_title', 'meta_description', 'meta_image', 'order_types',
                  'delivery_conditions', 'methods_of_payment']


class HomePageSerializer(serializers.Serializer):
    categories = CategorySerializer(many=True)
    banners = BannerSerializer(many=True)
    main_page = MainPageSerializer()
    cash_back = serializers.SerializerMethodField()

    def get_cash_back(self, obj):
        percents = PercentCashback.objects.all().first()
        if not percents:
            percents = PercentCashback.objects.create(mobile_percent=5, web_percent=3)
        return {
            'web': percents.web_percent,
            'mobile': percents.mobile_percent,
        }


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['phone']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['email']


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['link', 'icon']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['link', 'icon']


class ContactsSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True, source='phone_set')
    emails = EmailSerializer(many=True, source='email_set')
    social_links = SocialLinkSerializer(many=True, source='sociallink_set')
    addresses = AddressSerializer(many=True, source='address_set')
    payment_methods = PaymentMethodSerializer(many=True, source='paymentmethod_set')

    class Meta:
        model = Contacts
        fields = ['phones', 'emails', 'social_links', 'addresses', 'payment_methods']


class StaticPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticPage
        fields = ['title', 'slug', 'description', 'meta_title',
                  'meta_description', ]


class LayOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPage
        fields = ['icon', 'phone']
