from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserManagerTests(TestCase):
    def test_create_user_generates_employee_id_when_missing(self):
        User = get_user_model()

        user = User.objects.create_user(username="john", password="secret")

        self.assertTrue(user.employee_id.startswith("EMP"))
        self.assertRegex(user.employee_id, r"^EMP\d{5}$")
