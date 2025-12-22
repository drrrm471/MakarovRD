from src.core.abstract_employee import AbstractEmployee


def cmp_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Сравнивает сотрудников по имени (алфавитный порядок)."""
    return (emp1.name > emp2.name) - (emp1.name < emp2.name)


def cmp_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Сравнивает сотрудников по зарплате (по убыванию)."""
    return (emp2.calculate_salary() > emp1.calculate_salary()) - (emp2.calculate_salary() < emp1.calculate_salary())


def cmp_department_and_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Сравнивает сотрудников по отделу, а при равенстве — по имени."""
    if emp1.department == emp2.department:
        return cmp_name(emp1, emp2)
    return (emp1.department > emp2.department) - (emp1.department < emp2.department)