from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from rest_framework.test import APIClient

from api.models import Category, Course, Lesson

User = get_user_model()


@tag("api", "course")
class TestAPILMSEndpoint(StaticLiveServerTestCase):
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
        # Demo Data
        self.category = Category(name="Programming")
        self.category.save()
        self.course = Course(
            owner=self.demouser,
            name="Belajar Programming Bersama Sasri",
            category=self.category,
            price=50000,
        )
        self.course.save()
        self.lesson_1 = Lesson(course=self.course, title="Lesson pertama", duration=10)
        self.lesson_2 = Lesson(course=self.course, title="Lesson kedua", duration=5)
        self.lesson_1.save()
        self.lesson_2.save()
        # Client & Credentials
        self.client = APIClient()
        self.super_credentials = {"username": "admin", "password": "admin_password"}
        self.demo_credentials = {"username": "demo", "password": "demo_password"}

    def client_login(self):
        res = self.client.post("/api/auth/token/login/", data=self.demo_credentials)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + res.json()["auth_token"])

    def test_list_categories(self):
        self.client_login()
        res = self.client.get("/api/categories/")
        self.assertEqual(res.status_code, 200)

    def test_create_category(self):
        self.client_login()
        payload = {"parent": self.category.id, "name": "Python"}
        res = self.client.post("/api/categories/", data=payload)
        self.assertContains(res, status_code=201, text="Python")

    def test_retrieve_category(self):
        self.client_login()
        res = self.client.get(f"/api/categories/{self.category.id}/")
        self.assertContains(res, status_code=200, text="Programming")

    def test_update_category(self):
        self.client_login()
        payload = {"name": "Pemrograman"}
        res = self.client.put(f"/api/categories/{self.category.id}/", data=payload)
        self.assertContains(res, status_code=200, text="Pemrograman")

    def test_delete_category(self):
        self.client_login()
        res = self.client.delete(f"/api/categories/{self.category.id}/")
        self.assertEqual(res.status_code, 204)

    def test_list_course(self):
        self.client_login()
        res = self.client.get("/api/courses/")
        self.assertEqual(res.status_code, 200)

    def test_create_course(self):
        self.client_login()
        payload = {
            "category": self.category.id,
            "name": "Belajar Data Analysis",
            "description": "belajar Data Analysis",
            "price": 100000,
        }
        res = self.client.post("/api/courses/", data=payload)
        self.assertContains(res, status_code=201, text="Belajar Data Analysis")

    def test_retrieve_course(self):
        self.client_login()
        res = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertContains(res, status_code=200, text="Programming")

    def test_update_courses(self):
        self.client_login()
        payload = {
            "name": "Belajar Data Analysis Untuk Pemula",
            "description": "belajar Data Analysis",
            "price": 100000,
        }
        res = self.client.put(f"/api/courses/{self.course.id}/", data=payload)
        self.assertContains(res, status_code=200, text="Belajar Data Analysis Untuk Pemula")

    def test_delete_courses(self):
        self.client_login()
        res = self.client.delete(f"/api/courses/{self.course.id}/")
        self.assertEqual(res.status_code, 204)

    def test_list_lesson(self):
        self.client_login()
        res = self.client.get("/api/lessons/")
        self.assertEqual(res.status_code, 200)

    def test_add_new_lesson_to_selected_course(self):
        self.client_login()
        payload = {
            "course": self.course.id,
            "title": "Pertemuan ketiga",
            "description": "Pelajaran ketiga pertemuan ketiga",
            "duration": 3,
        }
        res = self.client.post("/api/lessons/", data=payload)
        self.assertContains(res, status_code=201, text="Pertemuan ketiga")
        # Verify lesson added successfully
        course = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertContains(course, status_code=200, text="Pertemuan ketiga")

    def test_update_a_lesson(self):
        self.client_login()
        payload = {
            "course": self.course.id,
            "title": "Pertemuan ke-1",
            "description": "Pelajaran ketiga pertemuan ke-1",
            "duration": 4,
        }
        res = self.client.put(f"/api/lessons/{self.lesson_1.id}/", data=payload)
        self.assertContains(res, status_code=200, text="Pertemuan ke-1")
        # Verify lesson updated successfully
        course = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertContains(course, status_code=200, text="Pertemuan ke-1")

    def test_remove_a_lesson_from_selected_course(self):
        self.client_login()
        res = self.client.delete(f"/api/lessons/{self.lesson_1.id}/")
        self.assertEqual(res.status_code, 204)
        # Verify lesson deleted successfully
        course = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertNotContains(course, status_code=200, text="Pertemuan Pertama")
