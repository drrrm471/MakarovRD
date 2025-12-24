"""Класс Developer (Разработчик)."""

from src.core.employee import Employee
from src.utils.validators import EmployeeValidator


class Developer(Employee):
    """Разработчик с уровнем seniority и стеком технологий."""

    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        tech_stack: list[str],
        seniority_level: str,
    ):
        """
        Инициализация базовых атрибутов разработчика.

        :param id: Уникальный идентификатор разработчика.
        :param name: Имя разработчика.
        :param department: Название отдела.
        :param base_salary: Базовая зарплата разработчика.
        :param tech_stack: Стек технологий разработчика.
        :param seniority_level: Уровень seniority разработчика (junior, middle, senior)
        """
        validator = EmployeeValidator()
        validator.validate_tech_stack(tech_stack)
        validator.validate_seniority_level(seniority_level)

        super().__init__(id, name, department, base_salary)
        self.__tech_stack = tech_stack
        self.__seniority_level = seniority_level

    @property
    def tech_stack(self) -> list[str]:
        """Получить стек технологий."""
        return self.__tech_stack.copy()

    @property
    def seniority_level(self) -> str:
        """Получить уровень seniority."""
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value: str) -> None:
        """Установить уровень seniority."""
        EmployeeValidator.validate_seniority_level(value)
        self.__seniority_level = value

    def __str__(self):
        """Возвращает строковое представление разработчика."""
        return f"Разработчик [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}, стек технологий: {self.tech_stack}, уровень Seniority: {self.seniority_level}]"

    def __iter__(self):
        """Позволяет итерироваться по стеку технологий."""
        return iter(self.tech_stack)

    @classmethod
    def from_dict(cls, data: dict) -> Employee:
        """Создаёт объект Developer из словаря."""
        if not data["type"] == cls.__name__:
            raise ValueError("Неподходящий тип данных!")
        del data["type"]
        required_fields = [
            "id",
            "name",
            "department",
            "base_salary",
            "tech_stack",
            "seniority_level",
        ]
        for field in required_fields:
            if field not in data:
                raise ValueError(
                    f"Для создания {cls.__name__} отсутствует поле: '{field}'"
                )
        return cls(**data)

    def calculate_salary(self):
        """Вычисляет зарплату в зависимости от уровня seniority."""
        coef = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return self.base_salary * coef.get(self.__seniority_level)

    def add_skill(self, new_skill: str) -> None:
        """Добавляет новую технологию в стек."""
        if not isinstance(new_skill, str):
            raise ValueError("Технология стека должна быть строкой!")
        if not new_skill.strip():
            raise ValueError("Технология стека не может быть пустой строкой!")
        self.tech_stack.append(new_skill)
