from abc import ABC, abstractmethod


class AbstractEmployee(ABC):
    """
    Абстрактный класс, описывающий общие свойства и методы всех сотрудников компании.
    """

    def __init__(self, id: int, name: str, department: str, base_salary: float):
        """
        Инициализация базовых атрибутов сотрудника.
        
        :param id: Уникальный идентификатор сотрудника.
        :param name: Имя сотрудника.
        :param department: Название отдела.
        :param base_salary: Базовая зарплата сотрудника.
        """
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

        self._validate_id(id)
        self._validate_name(name)
        self._validate_department(department)
        self._validate_base_salary(base_salary)


    def _validate_id(self, value: int) -> None:
        """Валидация ID."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"ID должен быть целым положительным числом!")
    
    def _validate_name(self, value: str) -> None:
        """Валидация имени."""
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой!")
        if not value.strip():
            raise ValueError("Имя не может быть пустой строкой!")
    
    def _validate_department(self, value: str) -> None:
        """Валидация отдела"""
        if not isinstance(value, str):
            raise ValueError("Отдел должен быть строкой!")
        if not value.strip():
            raise ValueError("Отдел не может быть пустой строкой!")


    def _validate_base_salary(self, value: float) -> None:
        """Валидация базовой зарплаты."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Базовая зарплата должна быть неотрицательным числом!")
        
    @property
    def id(self) -> int:
        """Возвращает ID сотрудника."""
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        """Устанавливает ID сотрудника с валидацией."""
        self._validate_id(value)
        self.__id = value

    @property
    def name(self) -> str:
        """Возвращает имя сотрудника."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает имя сотрудника с валидацией."""
        self._validate_name(value)
        self.__name = value

    @property
    def department(self) -> str:
        """Возвращает отдел сотрудника."""
        return self.__department

    @department.setter
    def department(self, value: str) -> None:
        """Устанавливает отдел сотрудника с валидацией."""
        self._validate_department(value)
        self.__department = value

    @property
    def base_salary(self) -> float:
        """Возвращает базовую зарплату сотрудника."""
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value: float) -> None:
        """Устанавливает базовую зарплату с проверкой."""
        self._validate_base_salary(value)
        self.__base_salary = value

    
    def __str__(self):
        """Возвращает строковое представление объекта сотрудника."""
        return f"Сотрудник [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}]"

    def __eq__(self, other) -> bool:
        """
        Сравнение сотрудников по id.
        
        :param other: Другой объект для сравнения.
        :return: True, если id совпадает, иначе False.
        """
        if isinstance(other, AbstractEmployee):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        raise ValueError('Необходимо использовать аргументы из классов AbstractEmployee или int!')

    def __lt__(self, other) -> bool:
        """
        Сравнение сотрудников по зарплате.
        """
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() < other.calculate_salary()
        elif isinstance(other, (int, float)):
            return self.calculate_salary() < other
        raise ValueError('Необходимо использовать аргументы из классов AbstractEmployee, int или float!')

    def __add__(self, other) -> float:
        """
        Сложение зарплат двух сотрудников или сотрудника с числом.
        """
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() + other.calculate_salary()
        elif isinstance(other, (int, float)):
            return self.calculate_salary() + other
        raise ValueError('Необходимо использовать аргументы из классов AbstractEmployee, int или float!')

    def __radd__(self, other) -> float:
        """Поддержка обратного сложения."""
        return self + other

    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'AbstractEmployee':
        """Создаёт объект сотрудника из словаря."""
        pass

    @abstractmethod
    def calculate_salary(self) -> float:
        """Вычисляет итоговую зарплату сотрудника."""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Возвращает строковую информацию о сотруднике."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        pass
