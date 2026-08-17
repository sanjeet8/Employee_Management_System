from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.accounts.constants import UserRole
from apps.employees.models import Employee, EmploymentType
from apps.departments.models import Department
from apps.departments.services import DepartmentService

# Test setup
class DepartmentServiceTest(TestCase):

    def setUp(self):
        self.engineering = Department.objects.create(
            name="Engineering",
            code="ENG",
            description="Engineering Department",
        )
        self.hr = Department.objects.create(
            name="Human Resources",
            code="HR",
            description="HR Department",
        )

    def create_employee(self, username, role, department, is_active=True,):
        return Employee.objects.create(
            user=self.create_user(
                username=username,
                role=role,
            ),
            department=department,
            joining_date="2026-01-01",
            employment_type = EmploymentType.FULL_TIME,
            salary=50000,
            is_active=is_active,
        )
    
    def create_user(self, username, role):
        User = get_user_model()

        user = User.objects.create_user(
            username=username,
            password="password123",
            email=f"{username}@example.com",
            role=role,
        )

        group, _ = Group.objects.get_or_create(
            name = role,
        )
        user.groups.add(group)
        
        return user
    
    # Test department creation
    def test_create_department(self):
        
        department = DepartmentService.create_department(
            validated_data={
                "name": "Finance",
                "code": "FIN",
                "description": "Finance Department",
            }
        )

        self.assertIsNotNone(department.pk)

        self.assertEqual(
            department.name,
            "Finance",
        )

        self.assertEqual(
            department.code,
            "FIN"
        )

        self.assertIsNone(
            department.manager,
        )

    # Valid manager assignment
    def test_assign_valid_manager(self):
        manager = self.create_employee(
            username="pankaj",
            role=UserRole.MANAGER,
            department=self.engineering,
        )

        DepartmentService.assign_manager(
            department=self.engineering,
            manager=manager,
        )
        self.engineering.refresh_from_db()
        self.assertEqual(
            self.engineering.manager,
            manager,
        )

    # Manager from another department ❌
    def test_manager_must_belong_to_same_department(self,):
        manager = self.create_employee(
            username="pankaj",
            role=UserRole.MANAGER,
            department=self.hr
        )

        with self.assertRaises(ValueError):
            DepartmentService.assign_manager(
                department=self.engineering,
                manager=manager,
            )

    # Employee cannot become department manager ❌
    def test_employee_cannot_be_department_manager(self,):
        employee = self.create_employee(
            username="rahul",
            role=UserRole.EMPLOYEE,
            department=self.engineering,
        )

        with self.assertRaises(ValueError):
            DepartmentService.assign_manager(
                department=self.engineering,
                manager=employee,
            )

    # Inactive manager cannot be assigned ❌
    def test_inactive_manager_cannot_be_assigned(self,):
        manager = self.create_employee(
            username="pankaj",
            role=UserRole.MANAGER,
            department=self.engineering,
            is_active=False
        )

        with self.assertRaises(ValueError):
            DepartmentService.assign_manager(
                department=self.engineering,
                manager=manager,
            )

    # Employee sees own department
    def test_employee_sees_own_department(self,):
        employee = self.create_employee(
            username="rahul",
            role=UserRole.EMPLOYEE,
            department=self.engineering,
        )

        departments = DepartmentService.get_visible_departments(
            user=employee.user
        )

        self.assertEqual(departments.count(), 1)
        self.assertEqual(
            departments.first(),
            self.engineering,
        )

    # Manager sees own department
    def test_manager_sees_own_department(self):
        manager = self.create_employee(
            username="pankaj",
            role=UserRole.MANAGER,
            department=self.engineering,
        )

        departments = DepartmentService.get_visible_departments(
            user=manager.user
        )

        self.assertEqual(departments.count(), 1)
        self.assertEqual(
            departments.first(),
            self.engineering,
        )

    # HR sees all
    def test_hr_sees_all_departments(self):
        hr = self.create_employee(
            username="hr",
            role=UserRole.HR,
            department=self.hr,
        )

        departments = DepartmentService.get_visible_departments(
            user=hr.user
        )

        self.assertEqual(
            departments.count(),
            Department.objects.count(),
        )

    # Admin sees all
    def test_admin_sees_all_departments(self):
        User = get_user_model()

        admin = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@example.com",
        )

        departments = DepartmentService.get_visible_departments(
            user=admin
        )

        self.assertEqual(
            departments.count(),
            Department.objects.count(),
        )