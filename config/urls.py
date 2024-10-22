"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.authentication.api.urls')),
    path('api/v1/orders/', include('apps.orders.api.urls')),
    path('api/v1/products/', include('apps.product.api.urls')),
    path('api/v1/pages/', include('apps.pages.api.urls')),
    # path('api/v1/chat/', include('apps.support_admin_chat.api.urls')),
    # path('support/', include('apps.support_admin_chat.urls')),
    path('api/v2/chat/', include('apps.chat.api.urls'))
]

urlpatterns += [
    path("", include("apps.openapi.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
