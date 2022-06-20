"""
    Note: Semua test untuk endpoints authentication sudah di test, check:
    https://github.com/sunscrapers/djoser/tree/master/testproject
"""
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from rest_framework.test import APIClient

User = get_user_model()


@tag("api", "authentication")
class TestAPIAuthentication(StaticLiveServerTestCase):
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

    def test_authtoken_login(self):
        res = self.client.post("/api/auth/token/login/", data=self.demo_credentials)
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "token")

    def test_authtoken_logout(self):
        # login
        login_res = self.client.post("/api/auth/token/login/", data=self.demo_credentials)
        token = login_res.json()["auth_token"]
        # logout
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        logout_res = self.client.post("/api/auth/token/logout/")
        self.assertEqual(logout_res.status_code, 204)

    def test_jwt_create_token(self):
        res = self.client.post("/api/auth/jwt/create/", data=self.demo_credentials)
        self.assertEqual(200, res.status_code)
        self.assertContains(res, "refresh")
        self.assertContains(res, "access")

    def test_jwt_verify_token(self):
        pass

    def test_jwt_refresh_token(self):
        pass


@tag("api")
class TestAPIUserEndpoint(StaticLiveServerTestCase):
    def test_list_users(self):
        pass

    def test_create_user(self):
        pass

    def test_retrieve_user(self):
        pass

    def test_update_user(self):
        pass

    def test_delete_user(self):
        pass

    def test_activate_user(self):
        pass

    def test_resend_activation(self):
        pass

    def test_reset_password(self):
        pass

    def test_reset_password_confirmation(self):
        pass

    def test_reset_username(self):
        pass

    def test_reset_username_confirmation(self):
        pass


@tag("api")
class TestAPICurrentUserEndpoint(StaticLiveServerTestCase):
    def test_retrieve_user(self):
        pass

    def test_update_user(self):
        pass

    def test_delete_user(self):
        pass

    def test_set_password(self):
        pass

    def test_set_username(self):
        pass
