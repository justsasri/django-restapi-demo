from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

app_name = "v1"

urlpatterns = router.urls
