"""Класс Salesperson (Продавец)."""

from src.core.employee import Employee
from src.utils.validators import EmployeeValidator


class Salesperson(Employee):
    """Продавец с комиссией и объемом продаж."""

    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        commission_rate: float,
        sales_volume: float,
    ):
        """
        Инициализация базовых атрибутов продавца.

        :param id: Уникальный идентификатор продавца.
        :param name: Имя продавца.
        :param department: Название отдела.
        :param base_salary: Базовая зарплата продавца.
        :param commission_rate: Процент комиссии.
        :param sales_volume: Объем продаж.
        """
        validator = EmployeeValidator()
        validator.validate_commission_rate(commission_rate)
        validator.validate_sales_volume(sales_volume)

        super().__init__(id, name, department, base_salary)
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume

    @property
    def commission_rate(self) -> float:
        """Получить процент комиссии."""
        return self.__commission_rate

    @commission_rate.setter
    def commission_rate(self, value: float) -> None:
        """Установить процент комиссии."""
        EmployeeValidator.validate_commission_rate(value)
        self.__commission_rate = float(value)

    @property
    def sales_volume(self) -> float:
        """Получить объем продаж."""
        return self.__sales_volume

    @sales_volume.setter
    def sales_volume(self, value: float) -> None:
        """Установить объем продаж."""
        EmployeeValidator.validate_sales_volume(value)
        self.__sales_volume = float(value)

    def __str__(self):
        """Возвращает строковое представление продавца."""
        return f"Продавец [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}, процент комиссии: {self.commission_rate}, объем продаж: {self.sales_volume}]"

    @classmethod
    def from_dict(cls, data: dict) -> Employee:
        """Создаёт объект Salesperson из словаря."""
        if not data["type"] == cls.__name__:
            raise ValueError("Неподходящий тип данных!")
        del data["type"]
        required_fields = [
            "id",
            "name",
            "department",
            "base_salary",
            "commission_rate",
            "sales_volume",
        ]
        for field in required_fields:
            if field not in data:
                raise ValueError(
                    f"Для создания {cls.__name__} отсутствует поле: '{field}'"
                )
        return cls(**data)

    def calculate_salary(self):
        """Вычисляет итоговую зарплату продавца."""
        return self.base_salary + (self.sales_volume * self.commission_rate)

    def update_sales(self, new_sales: float) -> None:
        """Увеличивает объем продаж."""
        if not isinstance(new_sales, (int, float)):
            raise ValueError("Добавляемый объем продаж должен быть числом!")
        self.sales_volume += new_sales
