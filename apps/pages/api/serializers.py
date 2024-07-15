from rest_framework import serializers

from apps.pages.models import Banner, OrderTypes, MainPage, Phone, Email, SocialLink, Address, PaymentMethod, Contacts, \
    StaticPage
from apps.product.models import Category


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
    order_types = OrderTypesSerializer(many=True)
    delivery_conditions = OrderTypesSerializer(many=True, source='deliveryconditions_set')
    methods_of_payment = OrderTypesSerializer(many=True, source='methodsofpayment_set')

    class Meta:
        model = MainPage
        fields = ['meta_title', 'meta_description', 'meta_image', 'order_types',
                  'delivery_conditions', 'methods_of_payment']


class HomePageSerializer(serializers.Serializer):
    categories = CategorySerializer(many=True)
    banners = BannerSerializer(many=True)
    main_page = MainPageSerializer()


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
