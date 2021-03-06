""" server URL Configuration"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from app.views import LandingPageView

urlpatterns = [
    path("", LandingPageView.as_view(), name="landing-page"),
    path("admin/", include("app.urls")),
    path("api/", include("api.urls")),
    path("django-admin/", admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
