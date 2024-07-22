import os
from datetime import timedelta
from pathlib import Path

from decouple import config
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
STATIC_ROOT = [os.path.join(BASE_DIR, 'static'),]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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

SIMPLEUI_HOME_INFO = True
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_DEFAULT_THEME = 'simpleui.css'
SIMPLEUI_INDEX = '#'
SIMPLEUI_LOGO = '/static/icons/LOGO.svg'
SIMPLEUI_CONFIG = {
    'system_keep': True,
    # 'menus': [
    #     {
    #         'name': 'О сайте',
    #         'icon': 'fa fa-database',
    #         'url': '/admin/about_us/siteinfo/'
    #     },
    #     {
    #         'name': 'Страницы',
    #         'icon': 'fa fa-book',
    #         'models': [
    #             {
    #                 'name': 'О нас',
    #                 'icon': 'fa fa-info-circle',
    #                 'models': [
    #                     {
    #                         'name': 'Страница О нас',
    #                         'icon': 'fa fa-file-text',
    #                         'url': '/admin/about_us/aboutpage/'
    #                     },
    #                     {
    #                         'name': 'Блоки',
    #                         'icon': 'fa fa-cubes',
    #                         'url': '/admin/about_us/contentblock/'
    #                     },
    #                 ]
    #             },
    #             {
    #                 'name': 'Портфолио',
    #                 'icon': 'fa fa-folder',
    #                 'models': [
    #                     {
    #                         'name': 'Страница Портфолио',
    #                         'icon': 'fa fa-file-text',
    #                         'url': '/admin/portfolio/portfoliopage/'
    #                     },
    #                     {
    #                         'name': 'Направление',
    #                         'icon': 'fa fa-arrows',
    #                         'url': '/admin/portfolio/portfolioduration/'
    #                     },
    #                     {
    #                         'name': 'Проекты',
    #                         'icon': 'fa fa-industry',
    #                         'url': '/admin/portfolio/portfolioproject/'
    #                     },
    #                 ]
    #             },
    #             {
    #                 'name': 'Услуги',
    #                 'icon': 'fa fa-user',
    #                 'models': [
    #                     {
    #                         'name': 'Страница Услуг',
    #                         'icon': 'fa fa-file-text',
    #                         'url': '/admin/services/servicepage/'
    #                     },
    #                     {
    #                         'name': 'Услуги',
    #                         'icon': 'fa fa-cube',
    #                         'url': '/admin/services/service/'
    #                     },
    #                     {
    #                         'name': 'Блоки сервисов',
    #                         'icon': 'fa fa-cubes',
    #                         'url': '/admin/services/contentblock/'
    #                     },
    #                 ]
    #             },
    #             {
    #                 'name': 'Контакты',
    #                 'icon': 'fa fa-address-book',
    #                 'url': '/admin/contacts/contact/'
    #             },
    #         ]
    #     },
    #     {
    #         'name': 'Заявки',
    #         'icon': 'fa fa-list',
    #         'url': '/admin/contacts/application/'
    #     },
    # ]
}
