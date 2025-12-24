"""Класс Department (Отдел) для управления сотрудниками."""

from typing import Optional
import json
import os

from .abstract_employee import AbstractEmployee
from .employee import Employee
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson
from src.utils.validators import DepartmentValidator


class Department:
    """Класс для управления отделом и его сотрудниками."""

    def __init__(self, name: str):
        """
        :param name: Название отдела.
        """
        validator = DepartmentValidator
        validator.validate_name(name)

        self.__name = name
        self.__employees: list[AbstractEmployee] = []

    @property
    def name(self):
        """Вернуть название отдела."""
        return self.__name

    @name.setter
    def name(self, value):
        """Установить название отдела."""
        DepartmentValidator.validate_name(value)
        self.__name = value

    @property
    def employees(self):
        """Вернуть список сотрудников."""
        return self.__employees

    def add_employee(self, employee: AbstractEmployee) -> None:
        """Добавляет нового сотрудника в отдел."""
        if not isinstance(employee, AbstractEmployee):
            raise ValueError(
                "Добавляемый сотрудник должен быть из класса AbstractEmployee!"
            )
        if employee in self.employees:
            raise ValueError("Добавляемый сотрудник уже находится в отделе!")
        self.employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        """Удаляет сотрудника по его ID."""
        employee = self.find_employee_by_id(employee_id)
        if not employee:
            raise ValueError("id сотрудника нет в списке!")
        self.employees.remove(employee)

    def get_employees(self) -> list[AbstractEmployee]:
        """Возвращает список сотрудников отдела."""
        return self.__employees

    def calculate_total_salary(self) -> float:
        """Возвращает суммарную зарплату всех сотрудников отдела."""
        return sum(emp.calculate_salary() for emp in self.employees)

    def get_employee_count(self) -> dict[str, int]:
        """Возвращает количество сотрудников по типам."""
        counter: dict[str, int] = {}
        for emp in self.employees:
            name = emp.__class__.__name__
            counter[name] = counter.get(name, 0) + 1
        return counter

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Ищет сотрудника по ID."""
        return next((e for e in self.employees if e.id == employee_id), None)

    @staticmethod
    def validate_path_json(filename: str, path: str):
        """Вспомогательная функция, для проверки и/или создания пути до .json файлов"""
        full_path = os.path.abspath(path)
        if not filename.endswith(".json"):
            raise ValueError("Файл должен быть в формате .json!")
        filepath = os.path.join(full_path, filename)

        os.makedirs(path, exist_ok=True)
        return filepath

    def to_dict(self) -> dict:
        """Преобразует объект в словарь без приватных префиксов."""
        data_department = {"name": self.name}
        data_department["employees"] = [e.to_dict() for e in self.employees]
        return data_department

    def save_to_file(self, filename: str) -> None:
        """Сохраняет данные отдела и сотрудников в JSON-файл."""
        filepath = self.validate_path_json(filename, "data/json")
        data = {
            "name": self.name,
            "employees": [emp.to_dict() for emp in self.employees],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "Department":
        """
        Создание экземпляра Department из словаря.
        """
        department = cls(data["name"])
        for emp_data in data["employees"]:
            if "bonus" in emp_data:
                department.add_employee(Manager.from_dict(emp_data))
            elif "tech_stack" in emp_data:
                department.add_employee(Developer.from_dict(emp_data))
            elif "commission_rate" in emp_data:
                department.add_employee(Salesperson.from_dict(emp_data))
            else:
                department.add_employee(Employee.from_dict(emp_data))
        return department

    @classmethod
    def load_from_file(cls, filename: str) -> "Department":
        """Загружает отдел из JSON-файла."""
        try:
            filepath = cls.validate_path_json(filename, "data/json")
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            raise ValueError(f"Ошибка при чтении файла {filename}!")
        return Department.from_dict(data)

    def __len__(self) -> int:
        """Возвращает количество сотрудников."""
        return len(self.employees)

    def __getitem__(self, key) -> AbstractEmployee:
        """Позволяет обращаться к сотруднику по индексу."""
        return self.employees[key]

    def __contains__(self, employee: AbstractEmployee) -> bool:
        """Проверяет, находится ли сотрудник в отделе."""
        return employee in self.employees

    def __iter__(self):
        """Позволяет итерироваться по сотрудникам отдела."""
        return iter(self.employees)
