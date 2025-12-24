from abc import ABC


class BaseCompanyException(Exception, ABC):
    """Абстрактный класс кастомных исключений для компании"""

    def __init__(self, *args):
        message = args[0] if args else self.default_message
        super().__init__(message)


class EmployeeNotFoundError(BaseCompanyException):
    """Исключение: Сотрудник не найден в отделе"""

    default_message = "Ошибка: Сотрудник не найден!"


class DepartmentNotFoundError(BaseCompanyException):
    """Исключение: Отдел не найден"""

    default_message = "Ошибка: Отдел не найден!"


class ProjectNotFoundError(BaseCompanyException):
    """Исключение: Проект не найден"""

    default_message = "Ошибка: Проект не найден!"


class InvalidStatusError(BaseCompanyException):
    """Исключение: Неверный формат статуса проекта"""

    default_message = "Ошибка: Неверный формат статуса проекта!"


class DuplicateIdError(BaseCompanyException):
    """Исключение: Идентификатор уже существует"""

    default_message = "Ошибка: Идентификатор уже существует!"
