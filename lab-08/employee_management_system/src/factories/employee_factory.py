from abc import ABC, abstractmethod

from src.core.abstract_employee import AbstractEmployee
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson


class EmployeeFactory(ABC):
    """Абстрактная фабрика для создания объектов сотрудников разных типов."""

    @classmethod
    @abstractmethod
    def create_employee(cls, **kwargs) -> AbstractEmployee:
        """Создание сотрудника."""
        pass

    @classmethod
    @abstractmethod
    def _check_params(cls, req_params: list, params: dict) -> None:
        default = ["id", "name", "department", "base_salary"]
        default.extend(req_params)
        missing = [p for p in default if p not in params]
        if missing:
            raise ValueError(
                f"Отсутствуют обязательные параметры: {', '.join(missing)}"
            )


class ManagerFactory(EmployeeFactory):
    """Фабрика для создания менеджеров."""

    @classmethod
    def create_employee(cls, **kwargs) -> Manager:
        cls._check_params(["bonus"], kwargs)

        return Manager(
            id=kwargs["id"],
            name=kwargs["name"],
            department=kwargs["department"],
            base_salary=kwargs["base_salary"],
            bonus=kwargs["bonus"],
        )


class DeveloperFactory(EmployeeFactory):
    """Фабрика для создания менеджеров."""

    @classmethod
    def create_employee(cls, **kwargs) -> Developer:
        cls._check_params(["tech_stack", "seniority_level"], kwargs)

        return Developer(
            id=kwargs["id"],
            name=kwargs["name"],
            department=kwargs["department"],
            base_salary=kwargs["base_salary"],
            tech_stack=kwargs["tech_stack"],
            seniority_level=kwargs["seniority_level"],
        )


class SalespersonFactory(EmployeeFactory):
    """Фабрика для создания менеджеров."""

    @classmethod
    def create_employee(cls, **kwargs) -> Salesperson:
        cls._check_params(["commission_rate", "sales_volume"], kwargs)

        return Salesperson(
            id=kwargs["id"],
            name=kwargs["name"],
            department=kwargs["department"],
            base_salary=kwargs["base_salary"],
            commission_rate=kwargs["commission_rate"],
            sales_volume=kwargs["sales_volume"],
        )
