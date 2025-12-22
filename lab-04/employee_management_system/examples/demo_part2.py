"""
    Демонстрация. Часть 2: Наследование и абстракция.
"""

import sys
import os

# Добавляем корень проекта в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.employee import Employee                             
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson
from src.factories.employee_factory import EmployeeFactory                 


def main():
    print("=" * 60)
    print(f"{'Демонстрация. Части 2: Наследование и абстракция':^60}")
    print("=" * 60)
    
    # Создание сотрудников разных типов
    print(f'\n{' Создание сотрудников и вывод их основной информации ':-^60}\n')
    employee = Employee(1, "Евгений", "ADMIN", 30000.0)
    manager = Manager(2, "Максим", "MANAGEMENT", 60000.0,
                        10000.0)
    developer = Developer(3, "Даниил", "DEV", 80000.0, 
                        ["JS", "GO", "C"], "senior")
    salesperson = Salesperson(4, "Павел", "SALES", 30000.0,
                        0.2, 200000.0)
    
    # Получение основной информации о сотрудниках
    print(f"  {employee.get_info()}")
    print(f"  {manager.get_info()}")
    print(f"  {developer.get_info()}")
    print(f"  {salesperson.get_info()}")
    
    # Демонстрация расчета зарплат
    print(f'\n{' Расчет итоговых зарплат до изменений ':-^60}\n')
    print(f"  Обычный сотрудник: {employee.calculate_salary()}")
    print(f"  Менеджер: {manager.calculate_salary()}")
    print(f"  Разработчик (senior): {developer.calculate_salary()}")
    print(f"  Продавец: {salesperson.calculate_salary()}")
    
    # Демонстрация работы с Manager
    print(f'\n{' Работа с менеджером ':-^60}\n')
    print(f'  Бонус: {manager.bonus}')
    manager.bonus = 5000.0
    print(f'  После изменения: {manager.bonus}')

    # Демонстрация работы с Developer
    print(f'\n{' Работа с разработчиком ':-^60}\n')
    print(f"  Уровень Seniority: {developer.seniority_level}")
    developer.seniority_level = 'middle'
    print(f"  После изменения: {developer.seniority_level}\n")
    print(f"  Стек технологий: {developer.tech_stack}")
    developer.add_skill("Python")
    print(f"  После изменения: {developer.tech_stack}")
    print(f"  Итерация по стеку технологий:")
    for tech in developer:
        print(f'   {tech}')
    
    # Демонстрация работы с Salesperson
    print(f'\n{' Работа с продавцом ':-^60}\n')
    print(f"  Объем продаж: {salesperson.sales_volume}")
    salesperson.update_sales(50000.0)
    print(f"  После изменения: {salesperson.sales_volume}\n")
    print(f"  Процент комиссии: {salesperson.commission_rate}")
    salesperson.commission_rate = 0.15
    print(f"  После изменения: {salesperson.commission_rate}")
    
    # Демонстрация фабрики
    print(f'\n{' Демонстрация фабрики сотрудников ':-^60}\n')
    dev = EmployeeFactory.create_employee(
        "developer",
        id=11,
        name="Олег",
        department="DEV",
        base_salary=70000.0,
        tech_stack=["Python", "JavaScript"],
        seniority_level="middle"
    )
    print(f"  {dev.get_info()}")
    
    # Демонстрация полиморфного поведения
    print(f'\n{' Демонстрация полиморфного поведения ':-^60}\n')
    employees_list = [employee, manager, developer, salesperson, dev]
    for emp in employees_list:
        print(f"      {emp.get_info()}")
    
    # Демонстрация расчета зарплат
    print(f'\n{' Расчет итоговых зарплат после изменений ':-^60}\n')
    print(f"  Обычный сотрудник: {employee.calculate_salary()}")
    print(f"  Менеджер: {manager.calculate_salary()}")
    print(f"  Разработчик (senior): {developer.calculate_salary()}")
    print(f"  Продавец: {salesperson.calculate_salary()}")

    print("\n" + "=" * 60)
    print(f"{'Демонстрация завершена!':^60}")
    print("=" * 60)


if __name__ == "__main__":
    main()