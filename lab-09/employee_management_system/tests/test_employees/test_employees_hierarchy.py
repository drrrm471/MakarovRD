import pytest

from src.core.abstract_employee import AbstractEmployee
from src.core.employee import Employee
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson
from src.factories.employee_factory import (
    ManagerFactory,
    DeveloperFactory,
    SalespersonFactory,
)


class TestAbstractEmployee:
    def test_cannot_instantiate_abstract_employee(self):
        with pytest.raises(TypeError):
            AbstractEmployee(1, "John", "IT", 5000.0)

    def test_subclasses_are_subtypes_of_abstract_employee(self):
        assert issubclass(Employee, AbstractEmployee)
        assert issubclass(Manager, AbstractEmployee)
        assert issubclass(Developer, AbstractEmployee)
        assert issubclass(Salesperson, AbstractEmployee)


class TestManager:
    def test_manager_salary_calculation(self):
        manager = Manager(1, "John", "Management", 5000.0, 1000.0)

        salary = manager.calculate_salary()

        assert salary == 6000.0

    def test_manager_bonus_validation(self):
        manager = Manager(1, "John", "Management", 5000.0, 1000.0)

        with pytest.raises(ValueError):
            manager.bonus = -1

        with pytest.raises(ValueError):
            manager.bonus = 0

    def test_manager_str_contains_bonus(self):
        manager = Manager(1, "John", "Management", 5000.0, 1000.0)

        text = str(manager)

        assert "бонус" in text.lower()
        assert "1000.0" in text


class TestDeveloper:
    @pytest.mark.parametrize(
        "level, coef",
        [
            ("junior", 1.0),
            ("middle", 1.5),
            ("senior", 2.0),
        ],
    )
    def test_developer_salary_by_level(self, level, coef):
        base_salary = 5000.0
        dev = Developer(1, "Alice", "DEV", base_salary, ["Python"], level)

        assert dev.calculate_salary() == base_salary * coef

    def test_add_skill_appends_to_tech_stack(self):
        dev = Developer(1, "Alice", "DEV", 5000.0, ["Python"], "senior")

        dev.add_skill("SQL")

        assert "SQL" in dev.tech_stack
        assert dev.tech_stack == ["Python", "SQL"]

    def test_tech_stack_validation(self):
        dev = Developer(1, "Alice", "DEV", 5000.0, ["Python"], "senior")

        with pytest.raises(ValueError):
            dev.tech_stack = "not_a_list"  # не список

        with pytest.raises(ValueError):
            dev.tech_stack = ["Python", ""]  # пустая строка

    def test_developer_iterates_over_skills(self):
        dev = Developer(1, "Alice", "DEV", 5000.0, ["Python", "SQL"], "senior")

        skills = [s for s in dev]

        assert skills == ["Python", "SQL"]


class TestSalesperson:
    def test_salesperson_salary_with_commission(self):
        sp = Salesperson(1, "Bob", "Sales", 3000.0, 0.2, 200000.0)

        salary = sp.calculate_salary()

        assert salary == 3000.0 + 0.2 * 200000.0

    def test_update_sales_increases_volume(self):
        sp = Salesperson(1, "Bob", "Sales", 3000.0, 0.1, 10000.0)

        sp.update_sales(5000.0)

        assert sp.sales_volume == 15000.0

    def test_commission_and_sales_validation(self):
        with pytest.raises(ValueError):
            Salesperson(1, "Bob", "Sales", 3000.0, -0.1, 10000.0)

        sp = Salesperson(1, "Bob", "Sales", 3000.0, 0.1, 10000.0)

        with pytest.raises(ValueError):
            sp.commission_rate = 0

        with pytest.raises(ValueError):
            sp.sales_volume = 0


class TestEmployeeFactories:
    def test_manager_factory_creates_manager(self):
        mgr = ManagerFactory.create_employee(
            id=1,
            name="John",
            department="MAN",
            base_salary=5000.0,
            bonus=1000.0,
        )

        assert isinstance(mgr, Manager)
        assert mgr.calculate_salary() == 6000.0

    def test_developer_factory_creates_developer(self):
        dev = DeveloperFactory.create_employee(
            id=1,
            name="Alice",
            department="DEV",
            base_salary=5000.0,
            tech_stack=["Python"],
            seniority_level="middle",
        )

        assert isinstance(dev, Developer)
        assert dev.calculate_salary() == 5000.0 * 1.5

    def test_salesperson_factory_creates_salesperson(self):
        sp = SalespersonFactory.create_employee(
            id=1,
            name="Bob",
            department="SAL",
            base_salary=3000.0,
            commission_rate=0.2,
            sales_volume=100000.0,
        )

        assert isinstance(sp, Salesperson)
        assert sp.calculate_salary() == 3000.0 + 0.2 * 100000.0


class TestPolymorphicEmployees:
    def test_polymorphic_calculate_salary(self):
        employees = [
            Employee(1, "Base", "IT", 4000.0),
            Manager(2, "Manager", "MAN", 5000.0, 1000.0),
            Developer(3, "Dev", "DEV", 5000.0, ["Python"], "senior"),
            Salesperson(4, "Sales", "SAL", 3000.0, 0.1, 50000.0),
        ]

        salaries = [e.calculate_salary() for e in employees]

        assert salaries[0] == 4000.0
        assert salaries[1] == 6000.0
        assert salaries[2] == 10000.0
        assert salaries[3] == 3000.0 + 0.1 * 50000.0
