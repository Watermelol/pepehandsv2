"""
Django settings for FYP project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import mimetypes


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vq2eu+uifnl8395y^d(dm_x0tv0vzql-o@x@nn4#=9sg02k&1d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.2', 'myfinb-maia.herokuapp.com', '127.0.0.1', 'localhost', 'poetic-abacus-279809.et.r.appspot.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Maia.apps.MaiaConfig',
    "crispy_forms",

    # SSL
    'sslserver',

    # Stripe
    'djstripe',

    # Social Login
    'social_django'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Social Login
    'social_django.middleware.SocialAuthExceptionMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'FYP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Social Login
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'FYP.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '35.197.143.212',
        'USER': 'bobbytee123',
        'PASSWORD': 'bobbytee123',
        'NAME': 'maia',
    }
}
# else:
#     # Running locally so connect to either a local MySQL instance or connect to
#     # Cloud SQL via the proxy. To start the proxy via command line:
#     #
#     #     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
#     #
#     # See https://cloud.google.com/sql/docs/mysql-connect-proxy
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'HOST': '127.0.0.1',
#             'PORT': '3306',
#             'NAME': 'maia',
#             'USER': 'bobbytee123',
#             'PASSWORD': 'bobbytee123',
#         }
#     }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR , 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
    'social.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',


    'django.contrib.auth.backends.ModelBackend',
]

SESSION_COOKIE_SAMESITE = None

# Strip (Payment API)
STRIPE_PUBLISHABLE_KEY = 'pk_test_51I6dyZGqnTLl5E4LDDu98qjEmrY6l8HDWEebGLR4KFEUEpfHFqlb6fqVFNoTexVZSbnRjf2cV8iheN0qXif3JJ9l000N1zqO8k'
STRIPE_SECRET_KEY = 'sk_test_51I6dyZGqnTLl5E4LnP4tVfXPzSLeyYo7wXgVYu3nlpHGBK5ei4861lp5F8XdCtSXVKRrEuEwIa90hyVYgmIdU7t100dStUYw0S'

# Social Login Setting
SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'
SOCIAL_AUTH_LOGIN_ERROR_URL = 'login'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = 'end_user_agreement'

SOCIAL_AUTH_FACEBOOK_KEY = '760189331511410'      # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '6d830789e6bfac6778502afd35893d6e'  # Facebook App Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '834873067898-776t64ftlbtf1a8daoereog14urjvfad.apps.googleusercontent.com' # Google App ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'nQwZPu7rFROW-rMJdI-T8MEL' # Google App Secret

SOCIAL_AUTH_TWITTER_KEY = '82XF7d0LnpKrW8OefxYvQ3DNi'
SOCIAL_AUTH_TWITTER_SECRET = 'IbapHQuOlvPubsJLTqzm5fUhMBdYs5nVGiQK9doYpkIc49o3WD'

# End Social Login Setting

# Strip Setting

STRIPE_TEST_PUBLIC_KEY = 'pk_test_51I6dyZGqnTLl5E4LDDu98qjEmrY6l8HDWEebGLR4KFEUEpfHFqlb6fqVFNoTexVZSbnRjf2cV8iheN0qXif3JJ9l000N1zqO8k'
STRIPE_TEST_SECRET_KEY = 'sk_test_51I6dyZGqnTLl5E4LnP4tVfXPzSLeyYo7wXgVYu3nlpHGBK5ei4861lp5F8XdCtSXVKRrEuEwIa90hyVYgmIdU7t100dStUYw0S'
STRIPE_LIVE_MODE = False
DJSTRIPE_WEBHOOK_SECRET = "whsec_Y9V01TtaxH60hnKe09s0p22PBT25B99C" 
DJSTRIPE_USE_NATIVE_JSONFIELD = True 
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id" 


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

mimetypes.add_type("text/css", ".css", True)
