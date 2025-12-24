import pytest

from src.core.employee import Employee
from src.core.department import Department
from src.employees.developer import Developer
from src.employees.manager import Manager


class TestDepartmentBasic:
    def test_add_and_get_employees(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000.0)

        dept.add_employee(emp)

        assert dept.get_employees() == [emp]

    def test_add_duplicate_employee_raises(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000.0)
        dept.add_employee(emp)

        with pytest.raises(ValueError):
            dept.add_employee(emp)

    def test_remove_employee_by_id(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000.0)
        dept.add_employee(emp)

        dept.remove_employee(1)

        assert len(dept) == 0

    def test_remove_non_existing_employee_raises(self):
        dept = Department("IT")

        with pytest.raises(ValueError):
            dept.remove_employee(999)

    def test_find_employee_by_id(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000.0)
        dept.add_employee(emp)

        found = dept.find_employee_by_id(1)

        assert found is emp
        assert dept.find_employee_by_id(999) is None


class TestDepartmentPolymorphism:
    def test_calculate_total_salary(self):
        dept = Department("IT")
        emp = Employee(1, "Base", "IT", 4000.0)
        mgr = Manager(2, "Manager", "IT", 5000.0, 1000.0)
        dev = Developer(3, "Dev", "IT", 5000.0, ["Python"], "middle")

        dept.add_employee(emp)
        dept.add_employee(mgr)
        dept.add_employee(dev)

        total = dept.calculate_total_salary()
        expected = (
            emp.calculate_salary() + mgr.calculate_salary() + dev.calculate_salary()
        )

        assert total == expected

    def test_get_employee_count_by_type(self):
        dept = Department("IT")
        dept.add_employee(Employee(1, "Base", "IT", 4000.0))
        dept.add_employee(Manager(2, "Manager", "IT", 5000.0, 1000.0))
        dept.add_employee(Developer(3, "Dev", "IT", 5000.0, ["Python"], "middle"))

        counts = dept.get_employee_count()

        assert counts["Employee"] == 1
        assert counts["Manager"] == 1
        assert counts["Developer"] == 1


class TestEmployeeMagicMethods:
    def test_employee_equality_by_id(self):
        emp1 = Employee(1, "John", "IT", 5000.0)
        emp2 = Employee(1, "Jane", "HR", 4000.0)
        emp3 = Employee(2, "Bob", "IT", 5000.0)

        assert emp1 == emp2  # одинаковый id
        assert emp1 != emp3

    def test_employee_salary_comparison(self):
        emp1 = Employee(1, "John", "IT", 5000.0)
        emp2 = Employee(2, "Jane", "HR", 6000.0)

        assert emp1 < emp2
        assert emp2 > emp1

    def test_employee_addition_with_employee_and_number(self):
        emp1 = Employee(1, "John", "IT", 5000.0)
        emp2 = Employee(2, "Jane", "HR", 6000.0)

        assert emp1 + emp2 == 11000.0
        assert emp1 + 1000 == 6000.0
        assert 1000 + emp1 == 6000.0


class TestDepartmentMagicMethods:
    def test_len_getitem_contains_iter(self):
        dept = Department("IT")
        employees = [Employee(i, f"Emp{i}", "IT", 5000.0) for i in range(3)]

        for emp in employees:
            dept.add_employee(emp)

        assert len(dept) == 3
        assert dept[0] is employees[0]
        assert employees[1] in dept

        names = [e.name for e in dept]
        assert names == ["Emp0", "Emp1", "Emp2"]


class TestSerialization:
    def test_employee_to_from_dict(self):
        emp = Employee(1, "John", "IT", 5000.0)

        data = emp.to_dict()
        new_emp = Employee.from_dict(data)

        assert new_emp.id == emp.id
        assert new_emp.name == emp.name
        assert new_emp.department == emp.department
        assert new_emp.base_salary == emp.base_salary


class TestSorting:
    def test_sorting_by_name_and_salary(self):
        employees = [
            Employee(3, "Charlie", "IT", 7000.0),
            Employee(1, "Alice", "HR", 5000.0),
            Employee(2, "Bob", "IT", 6000.0),
        ]

        sorted_by_name = sorted(employees, key=lambda e: e.name)
        assert [e.name for e in sorted_by_name] == ["Alice", "Bob", "Charlie"]

        sorted_by_salary = sorted(employees, key=lambda e: e.calculate_salary())
        assert sorted_by_salary[0].calculate_salary() == 5000.0
