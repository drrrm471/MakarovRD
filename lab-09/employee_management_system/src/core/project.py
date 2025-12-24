"""Класс Project (Проект) с композицией сотрудников."""

from typing import Optional

from .employee import Employee
from .department import Department
from .abstract_employee import AbstractEmployee
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson
from src.utils.exceptions import DuplicateIdError
from src.utils.validators import ProjectValidator


class Project(Department):
    """Класс, представляющий проект в компании."""

    def __init__(
        self,
        project_id: int,
        name: str,
        description: str,
        deadline: str,
        status: str = "planning",
    ):
        """
        Инициализация базовых атрибутов проекта

        :param project_id: уникальный идентификатор проекта
        :param name: название проекта
        :param description: описание проекта
        :param deadline: срок выполнения проекта
        :param status: статус проекта ("planning", "active", "completed", "cancelled")
        """
        super().__init__(name)

        validator = ProjectValidator()
        validator.validate_id(project_id)
        validator.validate_name(name)
        validator.validate_description(description)
        validator.validate_deadline(deadline)
        validator.validate_status(status)

        self.__project_id = project_id
        self.__description = description
        self.__deadline = deadline
        self.__status = status
        self.__team: list[Employee] = []

    def _validate_unique_employee_id(self, value: int) -> None:
        """Проверка уникальности ID сотрудника"""
        ProjectValidator.validate_positive_integer(value, "ID сотрудника")
        if value in [e.id for e in self.get_team()]:
            raise DuplicateIdError(f"Уже cуществует сотрудник с ID: {value}!")

    @property
    def project_id(self):
        """Возвращает идентификатор проекта."""
        return self.__project_id

    @project_id.setter
    def project_id(self, value: int):
        """Устанавливает идентификатор проекта с проверкой."""
        ProjectValidator.validate_id(value)
        self.__project_id = value

    @property
    def name(self):
        """Возвращает название проекта."""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Устанавливает название проекта с проверкой."""
        ProjectValidator.validate_name(value)
        self.__name = value

    @property
    def description(self):
        """Возвращает описание проекта."""
        return self.__description

    @description.setter
    def description(self, value: str):
        """Устанавливает описание проекта с проверкой."""
        ProjectValidator.validate_description(value)
        self.__description = value

    @property
    def deadline(self):
        """Возвращает срок выполнения проекта."""
        return self.__deadline

    @deadline.setter
    def deadline(self, value: str):
        ProjectValidator.validate_deadline(value)
        self.__deadline = value

    @property
    def status(self):
        """Возвращает статус проекта."""
        return self.__status

    @status.setter
    def status(self, value: str):
        """Устанавливает статус проекта с проверкой."""
        ProjectValidator.validate_status(value)
        self.__status = value

    @property
    def team(self):
        """Возвращает список сотрудников проекта."""
        return self.__team

    def add_team_member(self, employee: Employee) -> None:
        """Добавляет сотрудника в проект"""
        if not isinstance(employee, Employee):
            raise ValueError(
                "Добавляемый сотрудник должен быть из класса AbstractEmployee!"
            )
        if employee in self.team:
            raise ValueError("Добавляемый сотрудник уже находится в проекте!")
        self._validate_unique_employee_id(employee.id)
        self.team.append(employee)

    def find_team_member(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Ищет сотрудника в проекте по id"""
        ProjectValidator.validate_positive_integer(employee_id, "ID сотрудника")
        return next((e for e in self.team if e.id == employee_id), None)

    def remove_team_member(self, employee_id: int) -> None:
        """Удаляет сотрудника из отдела по id"""
        employee = self.find_team_member(employee_id)
        if not employee:
            raise ValueError("Cотрудника нет в списке!")
        self.team.remove(employee)

    def get_team(self) -> list[Employee]:
        """Возвращает список команды сотрудников"""
        return self.__team

    def get_team_size(self) -> int:
        """Возвращает размер команды сотрудников"""
        return len(self.team)

    def calculate_total_salary(self) -> float:
        """Расчет суммарной зарплаты команды сотрудников"""
        return sum(emp.calculate_salary() for emp in self.team)

    def get_project_info(self) -> str:
        """Возвращает полную информацию о проекте"""
        info = (
            f"Имя проекта: {self.name}\n"
            f"Идентификатор проекта: {self.project_id}\n"
            f"Описание проекта: {self.description}\n"
            f"Срок выполнения проекта: {self.deadline}\n"
            f"Статус проекта: {self.status}\n"
            f"Список сотрудников:\n{'\n'.join([i.get_info() for i in self.team])}"
        )
        return info

    def to_dict(self):
        """Преобразует объект в словарь без приватных префиксов."""
        data = self.__dict__
        data_project = {}
        for i in data:
            value = i[1:].split("__")[-1]
            if value == "deadline":
                data_project[value] = str(data[i])
            elif value == "team":
                data_project[value] = [e.to_dict() for e in data[i]]
            else:
                data_project[value] = data[i]
        return data_project

    def change_status(self, new_status: str) -> None:
        """Изменяет статус проекта"""
        self.status = new_status

    @classmethod
    def from_dict(cls, data: dict):
        """
        Создание экземпляра Project из словаря.
        """
        project = Project(
            data["project_id"],
            data["name"],
            data["description"],
            data["deadline"],
            data["status"],
        )
        for emp_data in data["team"]:
            if "bonus" in emp_data:
                project.add_team_member(Manager.from_dict(emp_data))
            elif "tech_stack" in emp_data:
                project.add_team_member(Developer.from_dict(emp_data))
            elif "commission_rate" in emp_data:
                project.add_team_member(Salesperson.from_dict(emp_data))
            else:
                project.add_team_member(Employee.from_dict(emp_data))
        return project
