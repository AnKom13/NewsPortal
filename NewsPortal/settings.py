"""
Django settings for NewsPortal project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os.path
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Start Django-environ
env = environ.Env(DEBUG=(bool, False))
# reading .env file
env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-nip0hb^3g7!(jwi*x=+(f8eql_wp-t8_7s+@#_e%6!0(i84v!3'
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get("DEBUG", default=0)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # подключение плоских страниц
    'django.contrib.sites',
    'django.contrib.flatpages',

    # подключение allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.google',

    'news',
    'django_filters',
    "django_apscheduler",
]

LOGIN_URL = '/accounts/login/'
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                #                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPortal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

LOGIN_REDIRECT_URL = '/pages'

# 45c82dcfb34eba8a5cca97b63e2389cf

# здесь указываем уже свою ПОЛНУЮ почту, с которой будут отправляться письма
# DEFAULT_FROM_EMAIL = 'ankom888@yandex.ru'

# адрес сервера Яндекс-почты для всех один и тот же
# EMAIL_HOST = 'smtp.yandex.ru'

# порт smtp сервера тоже одинаковый
# EMAIL_PORT = 465

# ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
# EMAIL_HOST_USER = 'ankom888'

# пароль от почты (Это не пароль электронной почты, а код авторизации)
# EMAIL_HOST_PASSWORD = 'pixlyxzaswkxqqsl'

# Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно
# EMAIL_USE_SSL = True

# беру из окружения, но там только текст, поэтому использую int,bool
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')

# мыло от которого будет происходить авто рассылка менеджерам
SERVER_EMAIL = 'ankom888@yandex.ru'

# префикс в теме письма при рассылке mail_managers (По умолчанию Django)
EMAIL_SUBJECT_PREFIX = '!!!'

MANAGERS = (
    ('Ivan', 'ivan48@yandex.ru'),
    #    ('Andrey', 'ankom888@yandex.ru')
    ('Andrey', 'ankom@list.ru'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_URL = 'http://127.0.0.1:8000'

# CELERY_BROKER_URL = 'redis://default:9mnCL6AVXg4InQF0CVBJ41kUYV4LVXjo@redis-19984.c304.europe-west1-2.gce.cloud.redislabs.com:19984'
CELERY_BROKER_URL = 'redis://default:NgwzTSqdVCqAFoAlzD5pKjHnUWw0F3mI@redis-14393.c135.eu-central-1-1.ec2.redns.redis-cloud.com:14393'

CELERY_RESULT_BACKEND = 'redis://default:NgwzTSqdVCqAFoAlzD5pKjHnUWw0F3mI@redis-14393.c135.eu-central-1-1.ec2.redns.redis-cloud.com:14393'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Кеширование
CACHES = {
    'default': {
        'TIMEOUT': 60,  # стандартное время ожидания в минуту (по умолчанию это 5 минут — 300 секунд)
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        # куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    },
}
