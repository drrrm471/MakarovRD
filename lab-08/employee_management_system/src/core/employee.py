from src.core.abstract_employee import AbstractEmployee


class Employee(AbstractEmployee):
    """Обычный сотрудник без дополнительных параметров."""

    def __init__(self, id, name, department, base_salary):
        """
        Инициализация базовых атрибутов сотрудника.

        :param id: Уникальный идентификатор сотрудника.
        :param name: Имя сотрудника.
        :param department: Название отдела.
        :param base_salary: Базовая зарплата сотрудника.
        """
        super().__init__(id, name, department, base_salary)

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
        return f"Основная информация: {self.__str__()}\nИтоговая зарплата: {self.calculate_salary()}"

    def to_dict(self):
        """Преобразует объект в словарь без приватных префиксов."""
        data = self.__dict__
        data_employee = {"type": self.__class__.__name__}
        for i in data:
            data_employee[i.split("__")[-1]] = data[i]
        return data_employee
