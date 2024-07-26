import os

from datetime import timedelta
from pathlib import Path
from decouple import config

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(' ')

PROJECT_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.sites',

]

SITE_ID = config('SITE_ID', cast=int)

DJANGO_APPS = [
    'apps.authentication',
    'apps.product',
    'apps.orders',
    'apps.pages',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'modeltranslation',
    'colorfield',

]

INSTALLED_APPS = [*DJANGO_APPS, *THIRD_PARTY_APPS, *PROJECT_APPS]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'config.middleware.LanguageMiddleware',

]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = "*"

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "authentication.User"

LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', _('Russian')),
    ('ky', _('Kyrgyz')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = ['https://foodfront.tatadev.pro/', 'https://www.foodfront.tatadev.pro/']

DEFAULT_PROFILE_PICTURE_URL = MEDIA_URL + 'profile_pictures/default-user.jpg'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=14),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Food OpenAPI",
    "DESCRIPTION": "Описание нашего API в разработке...",
    'COMPONENT_SPLIT_REQUEST': True,
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SERVE_PERMISSIONS": ("rest_framework.permissions.AllowAny",),
    "SERVE_AUTHENTICATION": ('rest_framework.authentication.SessionAuthentication',
                             'rest_framework.authentication.BasicAuthentication'),
    "PREPROCESSING_HOOKS": ("apps.openapi.preprocessors.get_urls_preprocessor",),
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "close",
    },
    "GENERATE_UNIQUE_PARAMETER_NAMES": True,
}

SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_DEFAULT_THEME = 'simpleui.css'
SIMPLEUI_INDEX = '#'
SIMPLEUI_LOGO = '/static/icons/LOGO.svg'
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menus': [
        {
            'name': 'Пользователь',
            'icon': 'fa fa-user',
            'models': [
                {
                    'name': 'Адрес Пользователя',
                    'icon': 'fa fa-home',
                    'url': '/admin/authentication/useraddress/'
                },
                {
                    'name': 'Пользователь',
                    'icon': 'fa fa-user',
                    'url': '/admin/authentication/user/'
                },
            ]
        },
        {
            'name': 'Рестораны',
            'icon': 'fa fas fa-utensils',
            'models': [
                {
                    'name': 'Рестораны',
                    'icon': 'fa fas fa-coffee',
                    'url': '/admin/orders/restaurant/'
                },
                {
                    'name': 'Заказы',
                    'icon': 'fa fas fa-archive',
                    'url': '/admin/orders/order/'
                },
                {
                    'name': 'Доставки',
                    'icon': 'fa fas fa-truck',
                    'url': '/admin/orders/delivery/'
                },
                {
                    'name': 'Отчеты',
                    'icon': 'fa fa-file',
                    'url': '/admin/orders/delivery/'
                },
            ]
        },
        {
            'name': 'Продукты',
            'icon': 'fa fas fa-hamburger',
            'models': [
                {
                    'name': 'Продукты',
                    'icon': 'fa fas fa-pizza-slice',
                    'url': '/admin/product/product/'
                },
                # {
                #     'name': 'Сеты',
                #     'icon': 'fa fas fa-pizza-slice',
                #     'url': '/admin/product/set/'
                # },
                {
                    'name': 'Добавки',
                    'icon': 'fa fas fa-bacon',
                    'url': '/admin/product/topping/'
                },
                # {
                #     'name': 'Ингредиенты',
                #     'icon': 'fa fas fa-egg',
                #     'url': '/admin/product/ingredient/'
                # },
                {
                    'name': 'Размеры',
                    'icon': 'fa fas fa-drumstick-bite',
                    'url': '/admin/product/size/'
                },
                {
                    'name': 'Тэги',
                    'icon': 'fa fas fa-tags',
                    'url': '/admin/product/tag/'
                },
            ]
        },
        {
            'name': 'Страницы',
            'icon': 'fa fa-list',
            'models': [
                {
                    'name': 'Главная страница',
                    'icon': 'fa fas fa-file',
                    'url': '/admin/pages/mainpage/'
                },
                {
                    'name': 'Статические страницы',
                    'icon': 'fa far fa-file-alt',
                    'url': '/admin/pages/staticpage/'
                },
                {
                    'name': 'Баннеры',
                    'icon': 'fa fas fa-clone',
                    'url': '/admin/pages/banner/'
                },
                {
                    'name': 'Контакты',
                    'icon': 'fa fas fa-phone',
                    'url': '/admin/pages/contacts/'
                },
            ]
        },
        {
            'name': 'Настройки',
            'icon': 'fa fa-cog',
            'models': [
                {
                    'name': 'Телеграмм',
                    'icon': 'fa fab fa-telegram',
                    'url': '/admin/orders/telegrambottoken/'
                },
                {
                    'name': 'Кэшбек',
                    'icon': 'fa fa-percent',
                    'url': '/admin/orders/percentcashback/'
                },
                {
                    'name': 'Тарифы на расстояние',
                    'icon': 'fa fa-ticket ',
                    'url': '/admin/orders/distancepricing/'
                },
            ]
        },
    ]
}
