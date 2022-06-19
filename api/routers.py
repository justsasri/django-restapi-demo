from django.urls import re_path
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import CategoryViewSet, CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("categories", CategoryViewSet, basename="category")
router.register("courses", CourseViewSet, basename="course")
router.register("lessons", LessonViewSet, basename="lesson")


app_name = "v1"


urlpatterns = router.urls + [
    re_path(r"^auth/token/login/?$", TokenCreateView.as_view(), name="login"),
    re_path(r"^auth/token/logout/?$", TokenDestroyView.as_view(), name="logout"),
    re_path(r"^auth/jwt/create/?", jwt_views.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^auth/jwt/refresh/?", jwt_views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^auth/jwt/verify/?", jwt_views.TokenVerifyView.as_view(), name="jwt-verify"),
]
