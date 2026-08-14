from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.accounts.constants import UserRole
from apps.departments.models import Department
from apps.employees.models import EmploymentType
from apps.employees.services import EmployeeService, Employee


class EmployeeViewTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            name="Engineering"
        )

    def create_user(self, username, role, manager=None):
        return EmployeeService.create_employee(
            validated_data={
                "username": username,
                "password": "password123",
                "first_name": username,
                "last_name": "Test",
                "email": f"{username}@test.com",
                "role": role,
                "department": self.department,
                "manager": manager,
                "joining_date": date.today(),
                "employment_type": EmploymentType.FULL_TIME,
                "salary": Decimal("50000"),
                "is_active": True,
            }
        )
    
    def test_employee_cannot_create_employee(self):
        employee = self.create_user(
            "john",
            UserRole.EMPLOYEE,
        )

        self.client.login(
            username = "john",
            password = "password123",
        )

        response = self.client.get(
            reverse("employees:employee-create")
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_hr_can_create_employee(self):
        hr = self.create_user(
            "hr_user",
            UserRole.HR,
        )

        self.client.login(
            username="hr_user",
            password="password123",
        )

        response = self.client.get(
            reverse("employees:employee-create")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_anonymous_user_redirected(self):
        response = self.client.get(
            reverse("employees:employee-create")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            "/accounts/login/",
            response.url
        )

    def test_employee_sees_only_themselves(self):
        employee1 = self.create_user(
            "john",
            UserRole.EMPLOYEE,
        )
        employee2 = self.create_user(
            "rahul",
            UserRole.EMPLOYEE
        )
        self.client.login(
            username="rahul",
            password="password123"
        )
        response = self.client.get(
            reverse("employees:employees")
        )
        self.assertEqual(response.status_code, 200)
        employees = response.context["employees"]
        self.assertEqual(
            employees.count(), 1,
        )
        self.assertEqual(
            employees.first(),
            employee2,
        )

    def test_manager_sees_only_employees(self):
        manager = self.create_user(
            "pankaj",
            UserRole.MANAGER,
        )
        employee1 = self.create_user(
            "john",
            UserRole.EMPLOYEE,
            manager=manager,
        )
        employee2 = self.create_user(
            "rahul",
            UserRole.EMPLOYEE,
            manager=manager,
        )
        employee3 = self.create_user(
            "amit",
            UserRole.EMPLOYEE,
        )
        print("Manager:", manager)
        print("Employee 1 manager:", employee1.manager)
        print("Employee 2 manager:", employee2.manager)
        self.client.login(
            username="pankaj",
            password="password123",
        )
        response = self.client.get(
            reverse("employees:employees")
        )

        self.assertEqual(response.status_code, 200)

        employees = response.context["employees"]

        self.assertEqual(
            employees.count(), 3,
        )

        self.assertIn(
            employee1,
            employees,
        )

        self.assertIn(
            employee2,
            employees,
        )

        self.assertNotIn(
            employee3,
            employees,
        )

    def test_hr_sees_everyone(self):
        hr = self.create_user(
            "hr_user",
            UserRole.HR,
        )

        self.client.login(
            username="hr_user",
            password="password123",
        )

        response = self.client.get(
            reverse("employees:employees")
        )

        employees = response.context["employees"]

        self.assertEqual(
            employees.count(),
            Employee.objects.count(),
        )