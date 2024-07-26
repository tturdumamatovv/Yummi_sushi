from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User, UserAddress


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    pass


class UserAddressInline(admin.StackedInline):
    model = UserAddress
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'full_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'date_of_birth', 'email', 'profile_picture', 'bonus')}),
        # (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'last_order')}),
        (_('Other'), {'fields': ( 'fcm_token', 'receive_notifications')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number', 'full_name')
    ordering = ('phone_number',)
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [UserAddressInline]
