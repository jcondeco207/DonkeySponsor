from pathlib import Path
from datetime import timedelta

#==================================| Django |==================================#

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*)7a)!lb@0-+v3p3ve$ejzghtny912(6=hs2ul0w)s_u1wn1jw"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_spectacular", # Swagger/Redoc
    "rest_framework",
    "rest_framework.authtoken",
    "knox",
    "modules.api",
    "modules.utilities.core",

    #TFA
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_email',  # <- if you want email capability.
    'two_factor',
    'two_factor.plugins.phonenumber',  # <- if you want phone number capability.
    'two_factor.plugins.email',  # <- if you want email capability.
    'two_factor.plugins.yubikey',  # <- for yubikey capability.
    'otp_yubikey',
    'two_factor.plugins.webauthn',

    #graphql
    "graphene_django"
]

GRAPHENE = {
    "SCHEMA": "Donkey_Sponsor.schema.schema"
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    #TFA
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

ROOT_URLCONF = "Donkey_Sponsor.urls"

WSGI_APPLICATION = "Donkey_Sponsor.wsgi.application"

#==================================| Two Factor Auth |==================================#

TWO_FACTOR_WEBAUTHN_RP_NAME="Donkey_Sponsor"
LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = '/two_factor:profile'

#==================================| Knox |==================================#

REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(hours=4),
  'USER_SERIALIZER': 'knox.serializers.UserSerializer',
  'TOKEN_LIMIT_PER_USER': 3,
  'AUTO_REFRESH': False,
  'AUTH_HEADER_PREFIX': 'Bearer'
}


#==================================| Templates |==================================#
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('frontend')],
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

#==================================| Databases |==================================#

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


#==================================| DRF |==================================#

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}



LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#==================================| Static files |==================================#

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR.joinpath('frontend', 'dist'),  # new
)

#==================================| DRF Spectacular |==================================#

SPECTACULAR_SETTINGS = {
    'TITLE': 'Donkey Sponsor',
    'DESCRIPTION': 'Developed by João Condeço and Bernardo Vitorino',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': [],
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_SPLIT_RESPONSE': True,
    'PRESERVE_REFERENCES': False,
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_spectacular.schema.SchemaGenerator',
    'SERVE_URLCONF': 'Donkey_Sponsor.urls',
    'TAGS': [  # tags to categorize API classes
    ],
}

#==================================| Settings needed for React |==================================#

CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies
SESSION_COOKIE_HTTPONLY = True
