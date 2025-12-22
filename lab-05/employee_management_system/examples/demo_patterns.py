"""
    Демонстрация работы.
"""

import sys
import os


# Добавляем корень проекта в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.database.connection import DatabaseConnection
from src.core.employee import Employee                             
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson
from src.factories.employee_factory import ManagerFactory, DeveloperFactory, SalespersonFactory
from src.factories.company_factory import TechCompanyFactory, SalesCompanyFactory
from src.patterns.builder import EmployeeBuilder

def main():
    print("=" * 60)
    print(f"{'Демонстрация':^60}")
    print("=" * 60)
    
    # Демонстрация Singleton 
    print(f'\n{' Singleton ':-^60}\n')
    db1 = DatabaseConnection("test.db")
    db2 = DatabaseConnection("test.db")

    print(f"db1 id: {id(db1)}")
    print(f"db2 id: {id(db2)}")
    print(db1 is db2) # True

    # Получаем подключение
    conn1 = db1.get_connection() # Создано подключение к: test.db
    print("Подключение к БД создано успешно")

    # Демонстрация фабрики
    print(f'\n{' Демонстрация фабрики сотрудников ':-^60}\n')

    # Создаем менеджера
    man = ManagerFactory.create_employee(
        id=11,
        name="Фабричный Менеджер",
        department="SAL",
        base_salary=45000.0,
        bonus = 5000
    )
    # Создаем разработчика
    dev = DeveloperFactory.create_employee(
        id=12,
        name="Фабричный Разработчик",
        department="DEV",
        base_salary=60000.0,
        tech_stack=['JS', 'GO'],
        seniority_level='middle' 
    )
    # Создаем продавца
    sal = SalespersonFactory.create_employee(
        id=13,
        name="Фабричный Продавец",
        department="SAL",
        base_salary=30000.0,
        commission_rate=0.2,
        sales_volume=200000.0
    )

    print(man, dev, sal, sep='\n')

    print(f'\n{' Демонстрация фабрики компаний ':-^60}\n')
    
    # Создаем техническую компанию
    tech_factory = TechCompanyFactory()
    tech_company = tech_factory.create_company("TechCompany")
    print(f"Создана IT-компания: {tech_company.name}  ({tech_company.__class__.__name__})")
    print(f"Отделы: {[d.name for d in tech_company.get_departments()]}")
    print(f"Проекты: {[p.name for p in tech_company.get_projects()]}\n")

    # Создаем торговую компанию
    sal_factory = SalesCompanyFactory()
    sal_company = sal_factory.create_company("SalCompany")
    print(f"Создана торговая компания: {sal_company.name}  ({sal_company.__class__.__name__})")
    print(f"Отделы: {[d.name for d in sal_company.get_departments()]}")
    print(f"Проекты: {[p.name for p in sal_company.get_projects()]}")



    # Демонстрация Builder
    print(f'\n{' Демонстрация Builder ':-^60}\n')

    # Создаем разработчика через Builder
    developer = (EmployeeBuilder()
                .set_id(1)
                .set_name("Bob Smith")
                .set_department("DEV")
                .set_base_salary(5000)
                .set_type("developer")
                .set_tech_stack(["Python", "SQL"])
                .set_seniority_level("senior")
                .build())
    print(f"Разработчик через Builder: {developer.get_info()}")

    # Создаем менеджера через Builder
    manager = (EmployeeBuilder()
              .set_id(2)
              .set_name("Alice Johnson")
              .set_department("MANAGEMENT")
              .set_base_salary(7000)
              .set_type("manager")
              .set_bonus(2000)
              .build())
    print(f"Менеджер через Builder: {manager.get_info()}")


    print("\n" + "=" * 60)
    print(f"{'Демонстрация завершена!':^60}")
    print("=" * 60)


if __name__ == "__main__":
    main()