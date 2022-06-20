import mimetypes

from .base import *  # NOQA

mimetypes.add_type("application/javascript", ".js", True)

DEBUG = True

ALLOW_ASYNC_UNSAFE = True

INTERNAL_IPS = [
    "127.0.0.1",
]

# # SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
