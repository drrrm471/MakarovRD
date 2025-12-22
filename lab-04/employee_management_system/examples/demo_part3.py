"""
    Демонстрация. Часть 3: Полиморфизм и Магические методы.
"""

import sys
import os
from functools import cmp_to_key

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.employee import Employee
from src.core.department import Department
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.utils.comparators import cmp_name, cmp_salary, cmp_department_and_name


def main():
    print("=" * 60)
    print(f"{'Демонстрация. Часть 3: Полиморфизм и магические методы':^60}")
    print("=" * 60)
    
    # Создание сотрудников разных типов
    employee = Employee(1, "Евгений", "ADMIN", 30000.0)
    manager = Manager(2, "Максим", "MANAGEMENT", 60000.0,
                        10000.0)
    developer = Developer(3, "Даниил", "DEV", 80000.0, 
                        ["JS", "GO", "C"], "senior")
    salesperson = Salesperson(4, "Павел", "SALES", 30000.0,
                        0.2, 200000.0)
    
    # Создание отдела
    print(f'\n{' Создание отдела':-^60}\n')
    department = Department("IT")
    department.add_employee(employee)
    department.add_employee(manager)
    department.add_employee(developer)
    department.add_employee(salesperson)
    print(f"  Отдел: {department.name}")
    print(f"  Добавленные сотрудники:")
    for emp in department:
        print(f"   - {emp.name} ({emp.__class__.__name__})")
    
    # Вызов `calculate_total_salary()` для отдела.
    print(f'\n{' Вызов `calculate_total_salary()` для отдела.':-^60}\n')
    total = department.calculate_total_salary()
    print(f"   Общая зарплата отдела: {total}")
    
    # Суммирование через sum()
    print(f'\n{' Суммирование зарплат через sum() ':-^60}\n')    
    employees = [employee, manager, developer, salesperson]
    total_salary = sum(employees)
    print(f"  Сумма зарплат через sum(): {total_salary}")
    
    # Использование перегруженных операторов
    print(f'\n{' Использование перегруженных операторов ':-^60}\n')    
    print(f"  employee == manager: {employee == manager}")
    print(f"  employee == employee: {employee == employee}")
    print(f"  employee < manager (по зарплате): {employee < manager}")
    print(f"  employee + manager (сумма зарплат): {employee + manager}")
    
    # Магические методы для отдела
    print(f'\n{' Магические методы для отдела ':-^60}\n')    
    print(f"  Количество сотрудников (len): {len(department)}")
    print(f"  Первый сотрудник (department[0]): {department[0].name}")
    print(f"  employee in department: {employee in department}")
    print(f"  employee not in department: {employee not in department}")
    
    # Итерация по отделу
    print(f'\n{' Итерация по отделу ':-^60}\n')    
    print("   Сотрудники в отделе:")
    for emp in department:
        print(f"   - {emp.name} ({emp.__class__.__name__})")
    
    # Итерация по стеку технологий разработчика
    print(f'\n{' Итерация по стеку технологий разработчика ':-^60}\n')    
    print(f"   Технологии {developer.name}:")
    for tech in developer:
        print(f"   - {tech}")
    
    # Сериализация и десериализация
    print(f'\n{' Сохранение и загрузка отдела из файла. ':-^60}\n')    

    # Сохранение отдела в файл .json
    department.save_to_file('department.json') 

    # Загрузка отдела из файла .json
    test_department = Department.load_from_file('department_load.json')

    print(f'Имя сохраненного отдела:  {department.name}')
    print(f'Имя загруженного отдела:  {test_department.name}')
    
    # Демонстрация работы компараторов
    employees = [employee, manager, developer, salesperson] # создадим список сотрудников для наглядности
    print(f'\n{' Использование компараторов ':-^60}\n')    
    print("  Демонстрация sorted() с key=")

    # 1. Сортировка по имени (возрастание)
    sorted_by_name = sorted(employees, key=lambda emp: emp.name)
    print("\n1. По имени (возрастание, key=lambda emp: emp.name):")
    for emp in sorted_by_name:
        print(f"  {emp.name:10} | {emp.department:15} | {emp.calculate_salary():8.2f}")

    # 2. Сортировка по зарплате (по убыванию)
    sorted_by_salary_desc = sorted(employees, key=lambda emp: emp.calculate_salary(), reverse=True)
    print("\n2. По зарплате (убывание, key=lambda emp: emp.calculate_salary(), reverse=True):")
    for emp in sorted_by_salary_desc:
        print(f"  {emp.name:10} | {emp.calculate_salary():8.2f} | {emp.__class__.__name__}")

    # 3. Сортировка по отделу и зарплате
    sorted_by_department_salary = sorted(employees, key=lambda emp: (emp.department, emp.calculate_salary()))
    print("\n3. По отделу и зарплате (key=lambda emp: (emp.department, emp.calculate_salary())):")
    for emp in sorted_by_department_salary:
        print(f"  {emp.department:15} | {emp.calculate_salary():8.2f} | {emp.name}")


    print("\n  Демонстрация key= vs cmp_to_key")

    # 1. Сортировка по имени с компаратором
    sorted_cmp_name = sorted(employees, key=cmp_to_key(cmp_name))
    print("\n1. По имени (cmp_to_key(cmp_name)):")
    for emp in sorted_cmp_name:
        print(f"  {emp.name:10}")

    # 2. Сортировка по зарплате с компаратором
    sorted_cmp_salary = sorted(employees, key=cmp_to_key(cmp_salary))
    print("\n2. По зарплате, убывание (cmp_to_key(cmp_salary)):")
    for emp in sorted_cmp_salary:
        print(f"  {emp.name:10} | {emp.calculate_salary():8.2f}")

    # 3. Сортировка по отделу и зарплате с компаратором
    sorted_cmp_department_salary = sorted(employees, key=cmp_to_key(cmp_department_and_name))
    print("\n3. По отделу и зарплате (cmp_to_key(compare_by_department_then_salary_cmp)):")
    for emp in sorted_cmp_department_salary:
        print(f"  {emp.department:15} | {emp.calculate_salary():8.2f} | {emp.name}")
    
    # Поиск сотрудника
    print(f'\n{' Поиск сотрудника по ID ':-^60}\n')    
    found = department.find_employee_by_id(3)
    if found:
        print(f"  {found.get_info()}")
    
    print("\n" + "=" * 60)
    print(f"{'Демонстрация завершена!':^60}")
    print("=" * 60)


if __name__ == "__main__":
    main()