from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User


class LoginTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="admin123",
        )

    # Test 1 - Login page loads
    def test_login_page_loads(self):
        response = self.client.get(
            reverse("accounts:login")
        )

        self.assertEqual(response.status_code, 200)

    # Test 2 - Successful Login
    def test_valid_login(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "john",
                "password": "admin123",
            },
        )

        self.assertNotEqual(
            response.wsgi_request.user.is_authenticated,
            False,
        )

    # Test 3 - Wrong Password
    def test_invalid_login(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "john",
                "password": "wrong-password",
            },
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated,
            False,
        )

    # Test 4 - Login Redirect
    def test_login_redirect(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "john",
                "password": "admin123",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)