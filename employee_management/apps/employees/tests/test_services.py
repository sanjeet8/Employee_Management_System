from datetime import date
from decimal import Decimal
from django.test import TestCase

from apps.accounts.constants import UserRole
from apps.departments.models import Department
from apps.employees.models import Employee, EmploymentType
from apps.employees.services import EmployeeService

class EmployeeServiceTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name = "Engineering",
            code = "ENG",
        )
        self.hr_department = Department.objects.create(
            name = "HR",
            code = "HR",
        )

    def test_create_employee(self):
        employee = EmployeeService.create_employee(
            validated_data={
                "username": "john",
                "password": "john@123",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "role": UserRole.EMPLOYEE,
                "department": self.department,
                "manager": None,
                "joining_date": date.today(),
                "employment_type": EmploymentType.FULL_TIME,
                "salary": Decimal("50000.00"),
                "is_active": True,
            }
        )

        self.assertIsNotNone(employee.pk)

        self.assertEqual(employee.user.username, "john")

        self.assertEqual(
            employee.department,
            self.department,
        )

        self.assertTrue(
            employee.user.role,
            UserRole.EMPLOYEE,
        )

        self.assertEqual(
            Employee.objects.count(), 1,
        )

        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.assertEqual(
            User.objects.count(), 1
        )

    def test_update_employee(self):
        employee = EmployeeService.create_employee(
            validated_data={
                "username": "john",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "role": UserRole.EMPLOYEE,
                "department": self.department,
                "manager": None,
                "joining_date": date.today(),
                "employment_type": EmploymentType.FULL_TIME,
                "salary": Decimal("50000.00"),
                "is_active": True,
            }
        )

        EmployeeService.update_employee(
            employee=employee,
            validated_data={
                "first_name": "Johnny",
                "last_name": "Doe",
                "email": "johnny@example.com",
                "role": UserRole.MANAGER,
                "department": self.hr_department,
                "manager": None,
                "joining_date": employee.joining_date,
                "employment_type": EmploymentType.FULL_TIME,
                "salary": Decimal("70000.00"),
                "is_active": True,
            },
        )

        employee.refresh_from_db()
        employee.user.refresh_from_db()

        # User updated
        self.assertEqual(
            employee.user.first_name,
            "Johnny",
        )

        self.assertEqual(
            employee.user.email,
            "johnny@example.com",
        )

        self.assertEqual(
            employee.user.role,
            UserRole.MANAGER,
        )

        # Employee updated
        self.assertEqual(
            employee.department,
            self.hr_department,
        )

        self.assertEqual(
            employee.salary,
            Decimal("70000.00"),
        )

        # Group changed
        self.assertTrue(
            employee.user.groups.filter(
                name=UserRole.MANAGER,
            ).exists()
        )

        # And make sure the old group was removed:
        self.assertFalse(
            employee.user.groups.filter(
                name=UserRole.EMPLOYEE,
            ).exists()
        )

    def test_deactivate_employee(self):
        manager = EmployeeService.create_employee(
            validated_data={
                "username": "manager",
                "password": "manager123",
                "first_name": "Manager",
                "last_name": "User",
                "email": "manager@example.com",
                "role": UserRole.MANAGER,
                "department": self.department,
                "manager": None,
                "joining_date": date.today(),
                "employment_type": EmploymentType.FULL_TIME,
                "salary": Decimal("60000.00"),
                "is_active": True,
            }
        )

        subordinate = EmployeeService.create_employee(
            validated_data={
                "username": "subordinate",
                "password": "subordinate123",
                "first_name": "Sub",
                "last_name": "User",
                "email": "subordinate@example.com",
                "role": UserRole.EMPLOYEE,
                "department": self.department,
                "manager": manager,
                "joining_date": date.today(),
                "employment_type": EmploymentType.FULL_TIME,
                "salary": Decimal("45000.00"),
                "is_active": True,
            }
        )

        result = EmployeeService.deactivate_employee(employee=manager)

        manager.refresh_from_db()
        manager.user.refresh_from_db()
        subordinate.refresh_from_db()

        self.assertIs(result, manager)
        self.assertFalse(manager.is_active)
        self.assertFalse(manager.user.is_active)
        self.assertIsNone(subordinate.manager)

