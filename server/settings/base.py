import os
from urllib.parse import urlparse

import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-secret-key"),
    SITE_ID=(int, 1),
    SENTRY_DSN=(str, ""),
    SITE_DOMAIN=(str, "localhost"),
    DEPLOYMENT_ENV=(str, "heroku"),
    ALLOW_WILD_CARD=(bool, True),
    STORAGE_TYPE=(str, "whitenoise"),
    CLOUDINARY_CLOUD_NAME=(str, ""),
    CLOUDINARY_API_KEY=(str, ""),
    CLOUDINARY_API_SECRET=(str, ""),
)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SITE_ID = env("SITE_ID")
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ROOT_URLCONF = "server.urls"
WSGI_APPLICATION = "server.wsgi.application"

##############################################################################
# HOST & CORS SETTINGS
##############################################################################

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5500"]
    CORS_ALLOWED_ORIGIN_REGEXES = ["http://127.0.0.1:5500"]


##############################################################################
# APPS & MIDDLEWARES
##############################################################################

INSTALLED_APPS = [
    "app",
    "api",
    "mptt",
    "djoser",
    "corsheaders",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular_sidecar",
    "drf_spectacular",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

##############################################################################
# AUTHENTICATION
##############################################################################

LOGIN_URL = "dashboard-login"

AUTH_USER_MODEL = "api.User"

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

##############################################################################
# INTERNATIONALIZATION
##############################################################################

LANGUAGE_CODE = env("LANGUAGE_CODE", str, "id-ID")
TIME_ZONE = env("LANGUAGE_CODE", str, "Asia/Jakarta")
USE_I18N = env("USE_I18N", bool, True)
USE_L10N = env("USE_L10N", bool, True)
# django import_export bug Timezone Localtime, disable for import!
USE_TZ = env("USE_TZ", bool, False)

LANGUAGES = [
    ("id-ID", "Indonesia"),
    ("en-US", "English (United States)"),
]

##############################################################################
# STATICFILE & STORAGE
##############################################################################

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"

##############################################################################
# DATABASE
##############################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

######################################################
# EMAIL
######################################################

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

##############################################################################
# SESSION & CACHE
##############################################################################

REDIS_URL = env("REDIS_URL", str, "redis://:local_password@127.0.0.1:6379/0")

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 15  # Logout if inactive for 15 minutes
SESSION_SAVE_EVERY_REQUEST = True

if REDIS_URL:
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    SESSION_CACHE_ALIAS = "default"
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        },
    }

##############################################################################
# QUEUES
##############################################################################

REDIS_SSL = env("REDIS_SSL", bool, False)
RQ_DATABASE = 1
RQ_URL = urlparse(REDIS_URL)

RQ_QUEUES = {
    "default": {
        "HOST": RQ_URL.hostname,
        "USERNAME": RQ_URL.username,
        "PASSWORD": RQ_URL.password,
        "PORT": RQ_URL.port,
        "DB": RQ_DATABASE,
        "SSL": bool(REDIS_SSL),
        "SSL_CERT_REQS": None,
    },
}

##############################################################################
# SESSION & CACHE
##############################################################################

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},
}

##############################################################################
# REST FRAMEWORK
##############################################################################

DEFAULT_RENDERER_CLASSES = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

REST_FRAMEWORK = {
    "PAGE_SIZE": 40,
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
}

##############################################################################
# REST FRAMEWORK DOC
##############################################################################

SPECTACULAR_SETTINGS = {
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    # General schema metadata. Refer to spec for valid inputs
    # https://spec.openapis.org/oas/v3.0.3#openapi-object
    "TITLE": "REST API Portofolio",
    "DESCRIPTION": "Job Seeker Rest API By Rizki Sasri Dwitama",
    "TOS": None,
    "CONTACT": {
        "name": "Rizki Sasri Dwitama",
        "url": "https://www.linkedin.com",
        "email": "sasri.project@gmail.com",
    },
    # Optional: MUST contain "name", MAY contain URL
    "LICENSE": {},
    # Statically set schema version. May also be an empty string. When used together with
    # view versioning, will become '0.0.0 (v2)' for 'v2' versioned requests.
    # Set VERSION to None if only the request version should be rendered.
    "VERSION": "1.0.0",
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    # e.g. [{'url': 'https://example.com/v1', 'description': 'Text'}, ...]
    "SERVERS": [],
    # Tags defined in the global scope
    "TAGS": [],
    # Optional: MUST contain 'url', may contain "description"
    "EXTERNAL_DOCS": {},
    # Arbitrary specification extensions attached to the schema's info object.
    # https://swagger.io/specification/#specification-extensions
    "EXTENSIONS_INFO": {},
    # Arbitrary specification extensions attached to the schema's root object.
    # https://swagger.io/specification/#specification-extensions
    "EXTENSIONS_ROOT": {},
}
