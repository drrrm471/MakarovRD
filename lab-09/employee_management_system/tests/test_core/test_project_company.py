import pytest

from src.core.employee import Employee
from src.core.department import Department
from src.core.project import Project
from src.core.company import Company
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson
from src.utils.exceptions import DuplicateIdError, InvalidStatusError


class TestProject:
    def test_project_team_management(self):
        project = Project(
            1, "AI Platform", "Разработка AI системы", "2024-12-31", "planning"
        )
        dev = Developer(1, "John", "DEV", 5000.0, ["Python"], "senior")

        project.add_team_member(dev)
        assert len(project.get_team()) == 1
        assert project.get_team_size() == 1

        project.remove_team_member(1)
        assert len(project.get_team()) == 0

    def test_project_total_salary(self):
        project = Project(
            1, "AI Platform", "Разработка AI системы", "2024-12-31", "planning"
        )
        manager = Manager(1, "Alice", "DEV", 7000.0, 2000.0)
        developer = Developer(2, "Bob", "DEV", 5000.0, ["Python"], "senior")

        project.add_team_member(manager)
        project.add_team_member(developer)

        total = project.calculate_total_salary()
        expected = manager.calculate_salary() + developer.calculate_salary()

        assert total == expected

    @pytest.mark.parametrize("invalid_status", ["invalid", "done", "in_progress"])
    def test_project_invalid_status_raises_error(self, invalid_status):
        with pytest.raises(InvalidStatusError):
            Project(1, "Test", "Test", "2024-12-31", invalid_status)


class TestCompanyDepartmentsProjects:
    def test_company_department_management(self):
        company = Company("TechCorp")
        dept = Department("Development")

        company.add_department(dept)
        assert len(company.get_departments()) == 1

        company.remove_department("Development")
        assert len(company.get_departments()) == 0

    def test_cannot_delete_department_with_employees(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000.0)

        dept.add_employee(emp)
        company.add_department(dept)

        with pytest.raises(ValueError):
            company.remove_department("Development")

    def test_company_find_employee(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000.0)

        dept.add_employee(emp)
        company.add_department(dept)

        found = company.find_employee_by_id(1)

        assert found is not None
        assert found.name == "John"

    def test_company_total_monthly_cost(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp1 = Employee(1, "John", "DEV", 5000.0)
        emp2 = Employee(2, "Jane", "DEV", 6000.0)

        dept.add_employee(emp1)
        dept.add_employee(emp2)
        company.add_department(dept)

        total = company.calculate_total_monthly_cost()
        assert total == emp1.calculate_salary() + emp2.calculate_salary()


class TestCustomExceptions:
    def test_duplicate_project_id_raises_error(self):
        company = Company("TechCorp")
        p1 = Project(1, "P1", "Desc", "2024-12-31", "planning")
        p2 = Project(1, "P2", "Desc2", "2024-12-31", "planning")

        company.add_project(p1)

        with pytest.raises(DuplicateIdError):
            company.add_project(p2)


class TestComplexCompanyStructure:
    def test_complex_company_structure(self):
        company = Company("TechInnovations")

        dev_department = Department("Development")
        sales_department = Department("Sales")

        manager = Manager(1, "Alice Johnson", "DEV", 7000.0, 2000.0)
        developer = Developer(
            2, "Bob Smith", "DEV", 5000.0, ["Python", "SQL"], "senior"
        )
        salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000.0, 0.15, 50000.0)

        dev_department.add_employee(manager)
        dev_department.add_employee(developer)
        sales_department.add_employee(salesperson)

        company.add_department(dev_department)
        company.add_department(sales_department)

        ai_project = Project(
            101, "AI Platform", "Разработка AI системы", "2024-12-31", "active"
        )
        web_project = Project(
            102, "Web Portal", "Создание веб-портала", "2024-09-30", "planning"
        )

        company.add_project(ai_project)
        company.add_project(web_project)

        ai_project.add_team_member(developer)
        ai_project.add_team_member(manager)
        web_project.add_team_member(developer)

        assert company.calculate_total_monthly_cost() > 0
        assert len(company.get_all_employees()) == 3
        assert ai_project.get_team_size() == 2
        assert web_project.get_team_size() == 1
