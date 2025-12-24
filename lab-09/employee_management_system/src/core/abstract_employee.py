"""Абстрактный базовый класс для сотрудников."""

from abc import ABC, abstractmethod


class AbstractEmployee(ABC):
    """
    Абстрактный класс, описывающий общие свойства и методы всех сотрудников компании.
    """


class ISalaryCalculable(ABC):
    """Абстрактный класс для вычисления итоговой зарплаты сотрудника."""

    @abstractmethod
    def calculate_salary(self) -> float:
        """Вычисляет итоговую зарплату сотрудника."""
        pass


class IInfoProvidable(ABC):
    """Абстрактный класс. Возвращает строковую информацию о сотруднике."""

    @abstractmethod
    def get_info(self) -> str:
        """Возвращает строковую информацию о сотруднике."""
        pass


class IToDict(ABC):
    """Абстрактный класс. Преобразует объект в словарь."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        pass


class IFromDict(ABC):
    """Абстрактный класс. Создаёт объект сотрудника из словаря."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "AbstractEmployee":
        """Создаёт объект сотрудника из словаря."""
        pass
