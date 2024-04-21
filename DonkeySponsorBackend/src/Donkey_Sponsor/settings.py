import io
from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
import google.auth
from google.cloud import secretmanager
import environ

envfile = os.environ.get('ENV_FILE_NAME', '.env')
load_dotenv(envfile)

AUTH_USER_MODEL = 'users_management.User'

#==================================| Django |==================================#

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*)7a)!lb@0-+v3p3ve$ejzghtny912(6=hs2ul0w)s_u1wn1jw"

env = environ.Env(
    SECRET_KEY=(str, os.getenv("SECRET_KEY")),
    DATABASE_URL=(str, os.getenv("DATABASE_URL")),
    GS_BUCKET_NAME=(str, os.getenv("GS_BUCKET_NAME")),
)

if os.getenv('ISGCP', 'true') == 'true':
    SECRET_KEY = env("SECRET_KEY")
    # Attempt to load the Project ID into the environment, safely failing on error.
    try:
        _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        pass

# Use local .env file in dev mode
if os.getenv("PYTHON_ENV") == "dev":
    DEBUG = True

# Use GCP secret manager in prod mode
elif os.getenv("GOOGLE_CLOUD_PROJECT", None):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    DEBUG = True
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.getenv("SETTINGS_NAME", "django_app_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )
    env.read_env(io.StringIO(payload))
else:
    raise Exception(
        "No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found."
    )



ALLOWED_HOSTS = ["*"]


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
    "modules.utilities.users_management",
    "modules.business.local_management",
    "modules.business.sponsoring",

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
    'axes',

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
LOGIN_REDIRECT_URL = '/'

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


#==================================| Axes |==================================#
AXES_DATABASE_MODEL = 'user_sessions.AccessAttempt'
AXES_COOLOFF_TIME = 0.0833
AXES_LOCK_OUT_AT_FAILURE = True
AXES_RESET_ON_SUCCESS = False
AXES_LOCKOUT_PARAMETERS = ["ip_address", "username"]
AXES_RESET_ON_SUCCESS = False
AXES_INCREMENTAL_TIME = 2
AXES_FAILURE_LIMIT = 5
SILENCED_SYSTEM_CHECKS = ['axes.W003'] # Axes dummy warning

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

dbname = str(os.getenv('POSTGRES_DB'))
dbhost = str(os.getenv('POSTGRES_HOST'))
dbport = os.getenv('POSTGRES_PORT')
dbuser = str(os.getenv('POSTGRES_USER'))
dbpassword = str(os.getenv('POSTGRES_PSW'))
dbport = os.getenv('POSTGRES_PORT')
dbuser = str(os.getenv('POSTGRES_USER'))
dbpassword = str(os.getenv('POSTGRES_PSW'))

# Database
if os.getenv('ISGCP', 'true') == 'false':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": dbname,
            "USER": dbuser,
            "PASSWORD": dbpassword,
            "HOST": dbhost,
            "PORT": dbport
        }
    }
else:
    DATABASES = {"default": env.db()}

if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "cloudsql-proxy"
    DATABASES["default"]["PORT"] = 5432

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

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,

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
    BASE_DIR.joinpath('frontend', 'dist'), 
)

MEDIA_ROOT =  os.path.join(os.path.dirname(BASE_DIR), "uploads")
MEDIA_URL = '/uploads/'

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
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['http://*','http://localhost:8000', 'https://donkeysponsor-donkey-sponsor-backend-jhszdcaqka-nw.a.run.app', 'https://*.a.run.app']
print(CSRF_TRUSTED_ORIGINS)