"""Базовый класс Employee с инкапсуляцией данных."""

from src.core.abstract_employee import AbstractEmployee
from src.utils.validators import EmployeeValidator


class Employee(AbstractEmployee):
    """Обычный сотрудник без дополнительных параметров."""

    def __init__(self, id: int, name: str, department: str, base_salary: float):
        """
        Инициализация базовых атрибутов сотрудника.

        :param id: Уникальный идентификатор сотрудника.
        :param name: Имя сотрудника.
        :param department: Название отдела.
        :param base_salary: Базовая зарплата сотрудника.
        """
        validator = EmployeeValidator()
        validator.validate_id(id)
        validator.validate_name(name)
        validator.validate_department(department)
        validator.validate_base_salary(base_salary)

        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    @property
    def id(self) -> int:
        """Получить ID сотрудника."""
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        """Установить ID сотрудника."""
        EmployeeValidator.validate_id(value)
        self.__id = value

    @property
    def name(self) -> str:
        """Получить имя сотрудника."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Установить имя сотрудника."""
        EmployeeValidator.validate_name(value)
        self.__name = value

    @property
    def department(self) -> str:
        """Получить отдел сотрудника."""
        return self.__department

    @department.setter
    def department(self, value: str) -> None:
        """Установить отдел сотрудника."""
        EmployeeValidator.validate_department(value)
        self.__department = value

    @property
    def base_salary(self) -> float:
        """Получить базовую зарплату сотрудника."""
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        """Установить базовую зарплату сотрудника."""
        EmployeeValidator.validate_base_salary(value)
        self.__base_salary = float(value)

    def __str__(self):
        """Возвращает строковое представление объекта сотрудника."""
        return f"Сотрудник [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}]"

    def __eq__(self, other) -> bool:
        """
        Сравнение сотрудников по id.

        :param other: Другой объект для сравнения.
        :return: True, если id совпадает, иначе False.
        """
        if isinstance(other, Employee):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        raise ValueError(
            "Необходимо использовать аргументы из классов AbstractEmployee или int!"
        )

    def __lt__(self, other) -> bool:
        """
        Сравнение сотрудников по зарплате.
        """
        if isinstance(other, Employee):
            return self.calculate_salary() < other.calculate_salary()
        raise ValueError(
            "Необходимо использовать аргументы из классов AbstractEmployee!"
        )

    def __add__(self, other) -> float:
        """
        Сложение зарплат двух сотрудников или сотрудника с числом.
        """
        if isinstance(other, Employee):
            return self.calculate_salary() + other.calculate_salary()
        raise ValueError(
            "Необходимо использовать аргументы из классов AbstractEmployee"
        )

    def __radd__(self, other) -> float:
        """Поддержка обратного сложения."""
        return self + other

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        """
        Создание экземпляра Employee из словаря.
        """
        if not data["type"] == cls.__name__:
            raise ValueError("Неподходящий тип данных!")
        del data["type"]

        required_fields = ["id", "name", "department", "base_salary"]
        for field in required_fields:
            if field not in data:
                raise ValueError(
                    f"Для создания {cls.__name__} отсутствует поле: '{field}'"
                )
        return cls(**data)

    def calculate_salary(self):
        """Возвращает базовую зарплату."""
        return float(self.base_salary)

    def get_info(self):
        """Возвращает текстовую информацию о сотруднике."""
        return f"Основная информация: {str(self)}\nИтоговая зарплата: {self.calculate_salary()}"

    def to_dict(self):
        """Преобразует объект в словарь без приватных префиксов."""
        data = self.__dict__
        data_employee = {"type": self.__class__.__name__}
        for i in data:
            data_employee[i.split("__")[-1]] = data[i]
        return data_employee
