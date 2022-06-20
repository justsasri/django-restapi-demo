from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from rest_framework.test import APIClient

User = get_user_model()


@tag("api", "current_user")
class TestAPICurrentUserEndpoint(StaticLiveServerTestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin",
            password="admin_password",
            email="admin@mail.com",
        )
        self.demouser = User.objects.create_superuser(
            username="demo",
            password="demo_password",
            email="admin@mail.com",
        )
        self.client = APIClient()
        self.super_credentials = {"username": "admin", "password": "admin_password"}
        self.demo_credentials = {"username": "demo", "password": "demo_password"}
