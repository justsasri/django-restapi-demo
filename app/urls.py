from django.urls import path

from .views import IndexView, LoginView, LogoutView

urlpatterns = [
    path("", IndexView.as_view(), name="dashboard-index"),
    path("login/", LoginView.as_view(), name="dashboard-login"),
    path("logout/", LogoutView.as_view(), name="dashboard-logout"),
]
