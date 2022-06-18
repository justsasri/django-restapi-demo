from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestAuthentication(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(
            username="admin",
            password="admin",
            email="admin@mail.com",
        )
        return super().setUp()

    def test_authtoken_login_with_valid_credentials(self):
        credential = {"username": "admin", "password": "admin"}
        res = self.client.post("/api/auth/token/login/", data=credential)
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "token")

    def test_jwt_create_token_with_valid_credentials(self):
        credential = {"username": "admin", "password": "admin"}
        res = self.client.post("/api/auth/jwt/create/", data=credential)
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "access")
        self.assertContains(res, "refresh")
