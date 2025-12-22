"""
    Демонстрация. Часть 1: Инкапсуляция.
"""

import sys
import os

# Добавляем корень проекта в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.employee import Employee

def main():
    print("=" * 60)
    print(f"{'Демонстрация. Часть 1: Инкапсуляция.':^60}")
    print("=" * 60)
    
    # Создание объекта из класса Employee
    print(f'\n{' Создание сотрудника ':-^60}\n')
    employee = Employee(
    id=111,
    name="виктор",
    department="АДМИНИСТРАЦИЯ",
    base_salary=44444
    )
    print(f'  {employee}')

    # Демонстрация работы геттеров
    print(f'\n{' Работа с свойствами (геттеры) ':-^60}\n')
    print(f"  ID сотрудника: {employee.id}")
    print(f"  Имя сотрудника: {employee.name}")
    print(f"  Отдел сотрудника: {employee.department}")
    print(f"  Базовая зарплата сотрудника: {employee.base_salary}")
    
    # Изменение через сеттеры
    print(f'\n{' Изменение через сеттеры ':-^60}\n')
    employee.id = 1
    employee.name = "Виктор"
    employee.department = "Администрация"
    employee.base_salary = 40000.0
    print(f"  Обновленный сотрудник 1: {employee}")
    
    # Демонстрация обработки ошибок
    print(f'\n{' Демонстрация обработки ошибок ':-^60}\n')

    # Ошибки при создании
    try:
        employee = Employee(-1, 'Виктор', "IT", 40000.0)  # Отрицательный ID
    except ValueError as e:
        print(f"  Ошибка при создании с невалидным ID: {e}")
    
    # Ошибки при установке
    try:
        employee.name = 123  # Невалидное имя
    except ValueError as e:
        print(f"  Ошибка при установке невалидного имени: {e}")
    
    try:
        employee.id = '123'  # Невалидный ID
    except ValueError as e:
        print(f"  Ошибка при установке невалидного ID: {e}")
    
    try:
        employee.department = 123
    except ValueError as e:
        print(f"  Ошибка при установке невалидного отдела: {e}")

    try:
        employee.base_salary = -40000.0  # Отрицательная зарплата
    except ValueError as e:
        print(f"  Ошибка при установке отрицательной зарплаты: {e}")
    
    print("\n" + "=" * 60)
    print(f"{'Демонстрация завершена!':^60}")
    print("=" * 60)


if __name__ == "__main__":
    main()
