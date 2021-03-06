from django.urls import path
from django.urls.conf import include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("documentation/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include("api.routers")),
]
