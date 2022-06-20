import dj_database_url
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # NOQA
from .base import MIDDLEWARE, env

DATABASES["default"] = dj_database_url.config(conn_max_age=600)  # NOQA

ALLOWED_HOSTS = [
    "*.simpel.test:8000",
    "www.%s" % env("SITE_DOMAIN"),
    env("SITE_DOMAIN"),
]

if env("ALLOW_WILD_CARD"):
    ALLOWED_HOSTS += [".%s" % env("SITE_DOMAIN")]

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5500"]
CORS_ALLOWED_ORIGIN_REGEXES = ["http://127.0.0.1:5500"]

######################################################
# STATICFILES STORAGE
######################################################

if env("STORAGE_TYPE") == "whitenoise":
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    MIDDLEWARE = MIDDLEWARE + [
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]
elif env("STORAGE_TYPE") == "cloudinary":
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": env("CLOUDINARY_CLOUD_NAME"),
        "API_KEY": env("CLOUDINARY_API_KEY"),
        "API_SECRET": env("CLOUDINARY_API_SECRET"),
    }
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


######################################################
# SENTRY
######################################################

if env("SENTRY_DSN") not in ["", None]:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        auto_session_tracking=False,
        send_default_pii=True,
    )

if env("DEPLOYMENT_ENV") == "heroku":
    django_heroku.settings(locals())
