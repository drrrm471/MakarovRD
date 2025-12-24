"""
Валидаторы для системы управления сотрудниками.
SRP: Каждый валидатор отвечает только за валидацию конкретной сущности.
Устраняет дублирование валидационного кода.
"""

from datetime import datetime
from typing import Any


class BaseValidator:
    """Базовый класс для всех валидаторов."""

    @staticmethod
    def validate_not_empty_string(value: Any, field_name: str) -> str:
        """Валидирует, что строка не пустая."""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} должно быть строкой!")
        if not value.strip():
            raise ValueError(f"{field_name} не может быть пустой строкой!")
        return value.strip()

    @staticmethod
    def validate_positive_number(value: Any, field_name: str) -> float:
        """Валидирует положительное число."""
        if not isinstance(value, (int, float)):
            raise ValueError(f"{field_name} должно быть числом!")
        if value <= 0:
            raise ValueError(f"{field_name} должно быть положительным!")
        return float(value)

    @staticmethod
    def validate_non_negative_number(value: Any, field_name: str) -> float:
        """Валидирует неотрицательное число."""
        if not isinstance(value, (int, float)):
            raise ValueError(f"{field_name} должно быть числом!")
        if value < 0:
            raise ValueError(f"{field_name} не может быть отрицательным!")
        return float(value)

    @staticmethod
    def validate_positive_integer(value: Any, field_name: str) -> int:
        """Валидирует положительное целое число."""
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{field_name} должно быть целым числом!")
        if value <= 0:
            raise ValueError(f"{field_name} должно быть положительным!")
        return value


class EmployeeValidator(BaseValidator):
    """Валидатор для сотрудников."""

    @staticmethod
    def validate_id(value: int) -> int:
        """Валидирует ID сотрудника."""
        return EmployeeValidator.validate_positive_integer(value, "ID сотрудника")

    @staticmethod
    def validate_name(value: str) -> str:
        """Валидирует имя сотрудника."""
        return EmployeeValidator.validate_not_empty_string(value, "Имя")

    @staticmethod
    def validate_department(value: str) -> str:
        """Валидирует название отдела."""
        return EmployeeValidator.validate_not_empty_string(value, "Отдел")

    @staticmethod
    def validate_base_salary(value: float) -> float:
        """Валидирует базовую зарплату."""
        return EmployeeValidator.validate_non_negative_number(value, "Базовая зарплата")

    @staticmethod
    def validate_bonus(value: float) -> float:
        """Валидирует бонус."""
        return EmployeeValidator.validate_positive_number(value, "Бонус")

    @staticmethod
    def validate_commission_rate(value: float) -> float:
        """Валидирует процент комиссии."""
        rate = EmployeeValidator.validate_positive_number(value, "Процент комиссии")
        if rate > 1.0:
            raise ValueError("Процент комиссии не может быть больше 100%!")
        return rate

    @staticmethod
    def validate_sales_volume(value: float) -> float:
        """Валидирует объем продаж."""
        return EmployeeValidator.validate_non_negative_number(value, "Объем продаж")

    @staticmethod
    def validate_tech_stack(value: list) -> list:
        """Валидирует список технологий."""
        if not isinstance(value, list):
            raise ValueError("Стек технологий должен быть списком!")
        if not all(isinstance(item, str) for item in value):
            raise ValueError("Все технологии должны быть строками!")
        if any(not tech.strip() for tech in value):
            raise ValueError("Технология не может быть пустой строкой!")
        return [tech.strip() for tech in value]

    @staticmethod
    def validate_seniority_level(value: str) -> str:
        """Валидирует уровень seniority."""
        valid_levels = {"junior", "middle", "senior"}
        normalized = EmployeeValidator.validate_not_empty_string(
            value, "Уровень seniority"
        )
        if normalized not in valid_levels:
            raise ValueError(f"Уровень должен быть одним из: {valid_levels}")
        return normalized


class DepartmentValidator(BaseValidator):
    """Валидатор для отделов."""

    @staticmethod
    def validate_name(value: str) -> str:
        """Валидирует название отдела."""
        return DepartmentValidator.validate_not_empty_string(value, "Название отдела")


class ProjectValidator(BaseValidator):
    """Валидатор для проектов."""

    @staticmethod
    def validate_id(value: int) -> int:
        """Валидирует ID проекта."""
        return ProjectValidator.validate_positive_integer(value, "ID проекта")

    @staticmethod
    def validate_name(value: str) -> str:
        """Валидирует название проекта."""
        return ProjectValidator.validate_not_empty_string(value, "Название проекта")

    @staticmethod
    def validate_description(value: str) -> str:
        """Валидирует описание проекта."""
        return ProjectValidator.validate_not_empty_string(value, "Описание проекта")

    @staticmethod
    def validate_deadline(value: str) -> str:
        """Валидирует срок выполнения в формате YYYY-MM-DD."""
        value = ProjectValidator.validate_not_empty_string(value, "Срок выполнения")
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Срок должен быть в формате YYYY-MM-DD: {e}")
        return value

    @staticmethod
    def validate_status(value: str) -> str:
        """Валидирует статус проекта."""
        valid_statuses = {"planning", "active", "completed", "cancelled"}
        normalized = ProjectValidator.validate_not_empty_string(value, "Статус проекта")
        if normalized not in valid_statuses:
            raise ValueError(f"Статус должен быть одним из: {valid_statuses}")
        return normalized


class CompanyValidator(BaseValidator):
    """Валидатор для компании."""

    @staticmethod
    def validate_name(value: str) -> str:
        """Валидирует название компании."""
        return CompanyValidator.validate_not_empty_string(value, "Название компании")
