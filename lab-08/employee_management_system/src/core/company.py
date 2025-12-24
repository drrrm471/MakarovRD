import os
import json
import csv
from typing import Optional

from .abstract_employee import AbstractEmployee
from .department import Department
from .project import Project
from src.utils.exceptions import (
    DepartmentNotFoundError,
    ProjectNotFoundError,
    DuplicateIdError,
    EmployeeNotFoundError,
)


class Company:
    """Класс, для управления компанией и её атрибутами"""

    def __init__(self, name: str):
        """
        Инициализация основных атрибутов компании

        :param name: Название компании
        """

        self.name = name
        self.__departments: list[Department] = []
        self.__projects: list[Project] = []

    def _validate_id(self, value: int) -> None:
        """Проверка ID в пределах всей компании"""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Идентификатор должен быть целым положительным числом!")

    def _validate_unique_employee_id(self, value: int) -> None:
        """Проверка уникальности ID сотрудника"""
        self._validate_id(value)
        if value in [e.id for e in self.get_all_employees()]:
            raise DuplicateIdError(f"Уже cуществует сотрудник с ID: {value}!")

    def _validate_unique_project_id(self, value: int) -> None:
        """Проверка уникальности ID проекта"""
        self._validate_id(value)
        if value in [p.project_id for p in self.projects]:
            raise DuplicateIdError(f"Уже существует проект с ID: {value}")

    @property
    def name(self):
        """Возвращает название компании"""
        return self._name

    @name.setter
    def name(self, value: str):
        """Устанавливает название компании с проверкой."""
        if not isinstance(value, str):
            raise ValueError("Название компании должно быть строкой!")
        if not value.strip():
            raise ValueError("Название компании не может быть пустой строкой!")
        self._name = value

    @property
    def departments(self):
        """Возвращает список отделов компании"""
        return self.__departments

    def add_department(self, value: Department) -> None:
        """Добавляет отдел в компанию"""
        if not isinstance(value, Department):
            raise DepartmentNotFoundError()
        self.departments.append(value)

    def _find_department(self, value: str) -> Optional[Department]:
        """Поиск отдела по имени в списке отделов компании"""
        for dep in self.__departments:
            if dep.name == value:
                return dep
        return None

    def remove_department(self, value: str) -> None:
        """Удаление отдела по имени в списке отделов компании"""
        department = self._find_department(value)
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{value}' не найден")
        if len(department) > 0:
            raise ValueError(f"Нельзя удалить отдел '{value}', в нем есть сотрудники")
        self.__departments.remove(department)

    def get_departments(self) -> list[Department]:
        """Возвращает список отделов компании"""
        return self.__departments

    @property
    def projects(self):
        """Возвращает список проектов компании"""
        return self.__projects

    def add_project(self, value: Project) -> None:
        """Добавляет проект в компанию"""
        self._validate_unique_project_id(value.project_id)
        if not isinstance(value, Project):
            raise ProjectNotFoundError()
        self.projects.append(value)

    def _find_project(self, project_id: int) -> Optional[Project]:
        """Поиск проекта по ID"""
        self._validate_id(project_id)
        return next((p for p in self.projects if p.project_id == project_id), None)

    def get_projects(self) -> list[Project]:
        """Возвращает список проектов компании"""
        return self.projects

    def remove_project(self, project_id: int) -> None:
        """Удаление проекта по ID"""
        proj = self._find_project(project_id)
        if proj == None:
            raise ProjectNotFoundError()
        if proj.team:
            raise ValueError("Нельзя удалить проект, если над ним работает команда!")
        self.projects.remove(proj)

    def get_all_employees(self) -> list[AbstractEmployee]:
        """Возвращает список всех сотрудников компании"""
        emp_list = []
        for dep in self.departments:
            for emp in dep:
                if emp not in emp_list:
                    emp_list.append(emp)
        return emp_list

    def transfer_employee(
        self,
        employee: AbstractEmployee,
        from_department: Department,
        to_department: Department,
    ) -> None:
        """
        Перенос сотрудника в другой отдел

        Args:
            employee(AbstractEmployee): Сотрудник, которого необходимо переместить
            from_department(Department): Отдел, из которого переносим сотрудника
            to_department(Department): Отдел, в который переносим сотрудника
        """
        departments = [from_department, to_department]
        if not isinstance(employee, AbstractEmployee):
            raise ValueError("Сотрудник должен быть из класса AbstractEmployee")
        if not all(isinstance(d, Department) for d in departments):
            raise ValueError("Отдел должен быть из класса Department")

        if all(d not in self.departments for d in departments):
            raise DepartmentNotFoundError()
        if employee not in from_department:
            raise EmployeeNotFoundError()

        for d in self.departments:
            if d == to_department:
                d.add_employee(employee)
            if d == from_department:
                d.remove_employee(employee.id)

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Поиск сотрудника по ID"""
        self._validate_id(employee_id)
        return next((e for e in self.get_all_employees() if e.id == employee_id), None)

    def calculate_total_monthly_cost(self) -> float:
        """Расчет общих месячных зарплат на затраты"""
        total_salary = 0.0
        for salary in self.get_all_employees():
            s = salary.calculate_salary()
            total_salary += s
        return total_salary

    def get_projects_by_status(self, status: str) -> list[Project]:
        """Сортирует проекты по статусу"""
        valide_projects: list[Project] = []
        for proj in self.projects:
            proj.validate_status(proj.status)
            if proj.status == status:
                valide_projects.append(proj)
        return valide_projects

    @staticmethod
    def _validate_path(filename: str, path: str):
        """Вспомогательная функция, для проверки и/или создания пути"""
        full_path = os.path.abspath(path)
        if not filename.endswith(".json") and filename == "data/json":
            raise ValueError("Файл должен быть в формате .json!")
        if not filename.endswith(".csv") and filename == "data/csv":
            raise ValueError("Файл должен быть в формате .csv!")
        filepath = os.path.join(full_path, filename)

        os.makedirs(path, exist_ok=True)
        return filepath

    def save_to_file(self, filename: str) -> None:
        """Сохраняет данные отдела и сотрудников в JSON-файл."""
        filepath = self._validate_path(filename, "data/json")
        data = {
            "name": self.name,
            "departments": [d.to_dict() for d in self.departments],
            "projects": [p.to_dict() for p in self.projects],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_file(cls, filename: str) -> "Company":
        """Загружает компанию из JSON-файла."""
        try:
            filepath = cls._validate_path(filename, "data/json")
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            raise ValueError(f"Ошибка при чтении файла {filename}!")

        company = cls(data["name"])
        for d in data["departments"]:
            department = Department.from_dict(d)
            company.add_department(department)
        for p in data["projects"]:
            project = Project.from_dict(p)
            company.add_project(project)
        return company

    def get_department_stats(self) -> dict:
        """Возвращает статистику по отделам."""
        state = dict()
        for d in self.departments:
            state[d.name] = {
                "employee_count": len(d),
                "employee_types": d.get_employee_count(),
                "total_salary": d.calculate_total_salary(),
            }
        return state

    def get_project_budget_analysis(self) -> dict:
        """Возвращает анализ бюджетов проектов."""
        analysis = {"total_budget": 0.0, "total_projects": len(self.projects)}
        for proj in self.projects:
            budget = proj.calculate_total_salary()
            analysis["total_budget"] += budget
        return analysis

    def find_overloaded_employees(self) -> list[AbstractEmployee]:
        """
        Возвращает список перегруженных сотрудников, которые участвуют в нескольких проектах
        """
        overloaded_employees = []
        for emp in self.get_all_employees():
            c = 0
            for proj in self.projects:
                if emp in proj.team:
                    c += 1
                if c >= 2:
                    overloaded_employees.append(emp)
                    break
        return overloaded_employees

    def _find_project_by_id(self, value: int):
        self._validate_id(value)
        return next((p for p in self.get_projects() if p.project_id == value), None)

    def assign_employee_to_project(self, employee_id: int, project_id: int) -> bool:
        """Назначение сотрудника на проект."""
        employee = self.find_employee_by_id(employee_id)
        project = self._find_project_by_id(project_id)
        project.add_team_member(employee)
        return True

    def check_employee_availability(self, employee_id: int) -> bool:
        """Проверить доступность сотрудника (не перегружен ли)."""
        return self.find_employee_by_id(employee_id) in self.find_overloaded_employees()

    def export_employees_csv(self, filename: str) -> None:
        """Экспорт отчета по сотрудникам в CSV."""
        if not ".csv" in filename:
            raise ValueError("Файл должен быть формата .csv!")
        filepath = self._validate_path(filename, "data/csv")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["ID", "Имя", "Отдел", "Тип", "Базовая зарплата", "Итоговая зарплата"]
            )
            for emp in self.get_all_employees():
                writer.writerow(
                    [
                        emp.id,
                        emp.name,
                        emp.department,
                        emp.__class__.__name__,
                        emp.base_salary,
                        emp.calculate_salary(),
                    ]
                )

    def export_projects_csv(self, filename: str) -> None:
        """Экспорт отчета по проектам в CSV."""
        if not ".csv" in filename:
            raise ValueError("Файл должен быть формата .csv!")
        filepath = self._validate_path(filename, "data/csv")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "ID проекта",
                    "Название",
                    "Статус",
                    "Срок",
                    "Размер команды",
                    "Бюджет команды",
                ]
            )
            for proj in self.__projects:
                writer.writerow(
                    [
                        proj.project_id,
                        proj.name,
                        proj.status,
                        proj.deadline,
                        proj.get_team_size(),
                        proj.calculate_total_salary(),
                    ]
                )
