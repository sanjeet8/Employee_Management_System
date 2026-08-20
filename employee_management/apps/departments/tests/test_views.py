from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.accounts.constants import UserRole
from apps.employees.models import Employee, EmploymentType
from apps.employees.services import EmployeeService
from apps.departments.models import Department

class DepartmentViewTest(TestCase):
    
    # Setup
    def setUp(self):
        self.engineering = Department.objects.create(
            name="Engineering",
            code="ENG",
            description="Engineering Department",
        )

        self.hr_department = Department.objects.create(
            name="Human Resources",
            code="HR",
            description="HR Department",
        )

    # Helper to create users
    def create_user(self, username, role):
        User = get_user_model()

        user = User.objects.create_user(
            username=username,
            password="password123",
            email=f"{username}@example.com",
            role=role,
        )

        group, _ = Group.objects.get_or_create(
            name=role,
        )

        user.groups.add(group)

        return user
    
    # Anonymous user
    def test_anonymous_user_redirected(self):
        response = self.client.get(
            reverse("departments:department-list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            "accounts/login/",
            response.url,
        )

    # HR sees all departments
    def test_hr_sees_all_departments(self):
        hr = self.create_user(
            "hr",
            UserRole.HR,
        )

        logged_in = self.client.login(
            username="hr",
            password="password123",
        )
        print("HR LOGIN:", logged_in)

        response = self.client.get(
            reverse("departments:department-list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        departments = response.context["departments"]

        self.assertEqual(
            departments.count(),
            2,
        )

    # Employee sees only their department
    def test_employee_sees_only_own_department(self):
        employee = EmployeeService.create_employee(
            validated_data={
                "username": "rahul",
                "password": "password123",
                "first_name": "Rahul",
                "last_name": "Test",
                "email": "rahul@example.com",
                "role": UserRole.EMPLOYEE,
                "department": self.engineering,
                "manager": None,
                "joining_date": "2026-01-01",
                "employment_type": EmploymentType.FULL_TIME,
                "salary": 50000,
                "is_active": True,
            }
        )

        self.client.login(
            username="rahul",
            password="password123",
        )

        response = self.client.get(
            reverse("departments:department-list")
        )

        departments = response.context["departments"]

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertEqual(
            departments[0],
            self.engineering,
        )

    # Manager sees only their department
    def test_manager_sees_only_own_department(self):
        manager = EmployeeService.create_employee(
            validated_data={
                "username": "pankaj",
                "password": "password123",
                "first_name": "Pankaj",
                "last_name": "Test",
                "email": "pankaj@example.com",
                "role": UserRole.MANAGER,
                "department": self.engineering,
                "manager": None,
                "joining_date": "2026-01-01",
                "employment_type": EmploymentType.FULL_TIME,
                "salary": 70000,
                "is_active": True,
            }
        )

        self.client.login(
            username="pankaj",
            password="password123",
        )

        response = self.client.get(
            reverse("departments:department-list")
        )

        departments = response.context["departments"]

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertEqual(
            departments[0],
            self.engineering,
        )

    # Admin sees all
    def test_admin_sees_all_departments(self):
        User = get_user_model()

        admin = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@example.com",
        )

        self.client.login(
            username="admin",
            password="admin123",
        )

        response = self.client.get(
            reverse("departments:department-list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        departments = response.context["departments"]

        self.assertEqual(
            departments.count(),
            2,
        )

    # Search test
    def test_hr_can_search_departments(self):
        hr = self.create_user(
            "hr",
            UserRole.HR,
        )

        self.client.login(
            username="hr",
            password="password123",
        )

        response = self.client.get(
            reverse("departments:department-list"),
            {"search": "Engineering"},
        )

        departments = response.context["departments"]

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertEqual(
            departments[0],
            self.engineering,
        )

    # And for an employee, searching for another department should not leak it:
    def test_employee_cannot_search_other_department(self):
        employee = EmployeeService.create_employee(
            validated_data={
                "username": "rahul",
                "password": "password123",
                "first_name": "Rahul",
                "last_name": "Test",
                "email": "rahul@example.com",
                "role": UserRole.EMPLOYEE,
                "department": self.engineering,
                "manager": None,
                "joining_date": "2026-01-01",
                "employment_type": EmploymentType.FULL_TIME,
                "salary": 50000,
                "is_active": True,
            }
        )

        self.client.login(
            username="rahul",
            password="password123",
        )

        response = self.client.get(
            reverse("departments:department-list"),
            {"search": "Human Resources"},
        )

        departments = response.context["departments"]

        self.assertEqual(
            departments.count(),
            0,
        )

    # HR can create
    def test_hr_can_create_department(self):
        hr = self.create_user(
            "hr",
            UserRole.HR,
        )

        self.client.login(
            username="hr",
            password="password123",
        )

        response = self.client.post(
            reverse("departments:department-create"),
            {
                "name": "Finance",
                "code": "FIN",
                "description": "Finance Department",
                "is_active": True,
            }
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            Department.objects.filter(
                name="Finance",
            ).exists()
        )

    # Employee cannot create
    def test_employee_cannot_create_department(self):
        employee = EmployeeService.create_employee(
            validated_data={
                "username": "rahul",
                "password": "password123",
                "first_name": "Rahul",
                "last_name": "Test",
                "email": "rahul@example.com",
                "role": UserRole.EMPLOYEE,
                "department": self.engineering,
                "manager": None,
                "joining_date": "2026-01-01",
                "employment_type": EmploymentType.FULL_TIME,
                "salary": 50000,
                "is_active": True,
            }
        )

        self.client.login(
            username="rahul",
            password="password123",
        )

        response = self.client.get(
            reverse("departments:department-create"),
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    # Manager cannot create
    def test_manager_cannot_create_department(self):
        manager = EmployeeService.create_employee(
            validated_data={
                "username": "pankaj",
                "password": "password123",
                "first_name": "Pankaj",
                "last_name": "Test",
                "email": "pankaj@example.com",
                "role": UserRole.MANAGER,
                "department": self.engineering,
                "manager": None,
                "joining_date": "2026-01-01",
                "employment_type": EmploymentType.FULL_TIME,
                "salary": 70000,
                "is_active": True,
            }
        )

        self.client.login(
            username="pankaj",
            password="password123",
        )

        response = self.client.get(
            reverse("departments:department-create"),
        )

        self.assertEqual(
            response.status_code,
            403,
        )