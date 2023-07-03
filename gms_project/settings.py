"""
Django settings for gms_project project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import sys
from pathlib import Path
from django.urls import reverse
import dotenv
dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# export DJANGO_SETTINGS_MODULE=gms_project.settings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

ALLOWED_HOSTS = ['gms-project-env.eba-yjdxh2pf.ap-southeast-1.elasticbeanstalk.com',
                 'gmsprojectuat.cloud',
                 '*']

# Application definition

INSTALLED_APPS = [
    'custom_functions.apps.CustomfunctionsConfig',
    'accounts.apps.AccountsConfig',
    'users.apps.UsersConfig',
    'inventory.apps.InventoryConfig',
    'guests.apps.GuestsConfig',
    'gqf.apps.GqfConfig',
    'gms.apps.GmsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'single_session',
    'admin_honeypot',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gms_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "gqf/templates"),
                 os.path.join(BASE_DIR, "gms/templates"),
                 os.path.join(BASE_DIR, 'templates'),
                 ],
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

WSGI_APPLICATION = 'gms_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "gms",
#         "USER": os.getenv('DATABASE_USER'),
#         "PASSWORD": os.getenv('DATABASE_PASSWORD'),
#         "HOST": os.getenv('DATABASE_HOST'),
#         "PORT": "5432",
#         "OPTIONS": {
#             "sslmode": "require",
#         }
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "gms_uat",
        "USER": os.getenv('VAULT_USER'),
        "PASSWORD": os.getenv('VAULT_PASSWORD'),
        "HOST": os.getenv('VAULT_HOST'),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_TZ = True

# SESSION_EXPIRE_SECONDS = 900    # 15 min session timeout
SESSION_TIMEOUT_REDIRECT = 'gms_login'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'gms_project/static')
]

# LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# GMS customizations
AUTH_USER_MODEL = 'users.SystemUser'

# Messages extension
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Add the path to the 'libs' directory to PYTHONPATH
LIBS_DIR = os.path.join(BASE_DIR, 'libs')
sys.path.append(LIBS_DIR)

# https redirection, enable this only when https is available.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = False
