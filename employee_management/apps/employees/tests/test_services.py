from datetime import date
from django.test import TestCase

from apps.accounts.models import User
from apps.departments.models import Department
from apps.employees.models import Employee
from apps.employees.services import EmployeeService

class EmployeeServiceTests(TestCase):
    def setUp(self):
        self.departments = Department.objects.create(
            name = "Engineering",
            code = "ENG",
        )

    def test_create_employee(self):
        employee = EmployeeService.create_employee(
            username="john",
            password="admin123",
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            department=self.departments,
            joining_date=date.today(),
            employment_type="FULL_TIME",
            salary=50000,
        )

        self.assertIsInstance(employee, Employee)

        self.assertEqual(employee.user.username, "john")

        self.assertEqual(
            employee.department.name,
            "Engineering",
        )

        self.assertTrue(
            employee.user.employee_id.startswith("EMP")
        )