import pytest

from src.core.employee import Employee


class TestEmployeeCreation:
    def test_employee_creation_valid_data(self):
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000.0)

        # Assert
        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000.0

    def test_employee_invalid_id_in_init_raises_error(self):
        # Assert
        with pytest.raises(ValueError):
            Employee(-1, "Alice", "IT", 5000.0)

        with pytest.raises(ValueError):
            Employee(0, "Alice", "IT", 5000.0)

    def test_employee_invalid_base_salary_in_init_raises_error(self):
        # Assert
        with pytest.raises(ValueError):
            Employee(1, "Alice", "IT", -100.0)

    def test_setters_validate_id_and_base_salary(self):
        emp = Employee(1, "Alice", "IT", 5000.0)

        with pytest.raises(ValueError):
            emp.id = -10

        with pytest.raises(ValueError):
            emp.base_salary = -1.0

    def test_setter_name_empty_string_raises_error(self):
        emp = Employee(1, "Alice", "IT", 5000.0)

        with pytest.raises(ValueError):
            emp.name = ""

        with pytest.raises(ValueError):
            emp.name = "   "


class TestEmployeeMethods:
    def test_employee_str_representation(self):
        emp = Employee(1, "Alice", "IT", 5000.0)

        result = str(emp)

        expected = "Сотрудник [id: 1, имя: Alice, отдел: IT, базовая зарплата: 5000.0]"
        assert result == expected

    def test_employee_calculate_salary_returns_base_salary(self):
        emp = Employee(1, "Alice", "IT", 5000.0)

        salary = emp.calculate_salary()

        assert salary == 5000.0
