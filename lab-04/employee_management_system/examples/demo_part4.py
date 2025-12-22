"""
    Демонстрация работы.
    Часть 4: Композиция, Агрегация и Работа со сложными структурами.
"""

import sys
import os

# Добавляем корень проекта в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.department import Department
from src.core.project import Project
from src.core.company import Company
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.utils.exceptions import InvalidStatusError, DuplicateIdError


def main():
    print("=" * 60)
    print(f"{'Демонстрация. Часть 4: Композиция и агрегация':^60}")
    print("=" * 60)


    # Создание компании
    print(f'\n{' Создание компании ':-^60}\n')
    company = Company("TechInnovations")
    print(f"  Название компании: {company.name}")
    
    # Создание отделов
    print(f'\n{' Создание и добавление отделов в компанию ':-^60}\n')
    dev_department = Department("Development")
    sales_department = Department("Sales")

    # Добавление отделов в компанию
    company.add_department(dev_department)
    company.add_department(sales_department)

    print(f"  Добавленные отделы:")
    for dep in company.departments:
        print(f"   - {dep.name}")

    
    # Создание сотрудников разных типов
    print(f'\n{' Создание и добавление сотрудников в отделы ':-^60}\n')
    manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
    developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
    salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)
    
    # Добавление сотрудников в отделы
    dev_department.add_employee(manager)
    dev_department.add_employee(developer)
    sales_department.add_employee(salesperson)
    
    print(f"  Добавленные отделы и сотрудники:")
    for dep in company.departments:
        print(f"   - {dep.name}")
        for emp in dep:
            print(f"     - {emp.name}")


    # Создание проектов
    print(f'\n{' Создание и добавление проектов в компанию ':-^60}\n')
    ai_project = Project(101, "AI Platform", "Разработка AI системы", "2024-12-31", "active")
    web_project = Project(102, "Web Portal", "Создание веб-портала", "2024-09-30", "planning")
    
    # Добавление проектов в компанию
    company.add_project(ai_project)
    company.add_project(web_project)

    print(f"  Добавленные проекты:")
    for proj in company.projects:
        print(f"   - {proj.name}")
    
    # Формирование команд проектов
    print(f'\n{' Формирование команд проектов ':-^60}\n')
    ai_project.add_team_member(developer)
    ai_project.add_team_member(manager)
    web_project.add_team_member(developer)

    print(f"  Добавленные проекты и команды:")
    for proj in company.projects:
        print(f"   - {proj.name}")
        for emp in proj.team:
            print(f"     - {emp.name}")

    # Валидация и обработка ошибок
    print(f'\n{' Демонстрация валидации и обработки ошибок ':-^60}\n')
    
    try:
        project = Project(101, "Test", "Test", "2024-12-31", "invalid_status")
    except InvalidStatusError as e:
        print(f"    Ошибка при создании проекта с невалидным статусом: {e}")

    try:
        company.add_project(Project(101, "Duplicate", "Test", "2024-12-31", "planning"))
    except DuplicateIdError as e:
        print(f"    Ошибка при добавлении проекта с дублирующимся ID: {e}")

    try:
        company.remove_department("Development")
    except ValueError as e:
        print(f"    Ошибка при удалении отдела с сотрудниками: {e}")


    # Статистика по отделам
    print(f'\n{' Статистика по отделам ':-^60}\n')
    stats = company.get_department_stats()
    for dept_name, dept_stats in stats.items():
        print(f"   {dept_name}:")
        print(f"      Сотрудников: {dept_stats['employee_count']}")
        print(f"      Общая зарплата: {dept_stats['total_salary']}")
        print(f"      Типы сотрудников: {dept_stats['employee_types']}")

    # Финансовые показатели
    print(f'\n{' Финансовые показатели компании ':-^60}\n')
    total_cost = company.calculate_total_monthly_cost()
    print(f"   Общие месячные затраты на зарплаты: {total_cost}")

    # Анализ бюджетов проектов
    print(f'\n{' Анализ бюджетов проектов ':-^60}\n')
    budget_analysis = company.get_project_budget_analysis()
    print(f"   Всего проектов: {budget_analysis['total_projects']}")
    print(f"   Общий бюджет: {budget_analysis['total_budget']}")

    # Поиск перегруженных сотрудников
    print(f'\n{' Поиск перегруженных сотрудников ':-^60}\n')
    overloaded = company.find_overloaded_employees()
    if overloaded:
        for emp in overloaded:
            print(f"    {emp.name} участвует в нескольких проектах")
    else:
        print("    Перегруженных сотрудников не найдено")

    # Проверка доступности сотрудника
    print(f'\n{' Проверка доступности сотрудников ':-^60}\n')
    for emp_id in [1, 2, 3]:
        available = company.check_employee_availability(emp_id)
        emp = company.find_employee_by_id(emp_id)
        print(f"    {emp.name if emp else 'Не найден'}: {'Доступен' if available else 'Перегружен'}")
    
    # Перенос сотрудника между отделами
    print(f'\n{' Перенос сотрудника между отделами ':-^60}\n')
    try:
        company.transfer_employee(developer, dev_department, sales_department)
        print(f"    Сотрудник {developer.name} перенесен из Development в Sales")
        print(f"    Сотрудников в Development: {len(dev_department)}")
        print(f"    Сотрудников в Sales: {len(sales_department)}")
    except Exception as e:
        print(f"    Ошибка при переносе: {e}")

     # Назначение сотрудника на проект
    print(f'\n{' Назначение сотрудника на проект ':-^60}\n')

    # Создание нового проекта
    fin_analysis_project = Project(103, "Finance Analysis", "Финансовый анализ", 
                               "2024-11-30", "planning")
    company.add_project(fin_analysis_project)

    company.assign_employee_to_project(3, 103)  # назначим продавца по id = 3 на созданный только что проект по id = 103
    print(f"    Продавец назначен на проект Finance Analysis")
    print(f"    Команда проекта Finance Analysis: {fin_analysis_project.get_team_size()} человек")
    print(f"     - {fin_analysis_project.team[0].name}")

    # Сериализация компании
    print(f'\n{' Сохранение и загрузка компании в .json ':-^60}\n')
    
    # Сохранение компании в company.json
    company.save_to_file('company.json')
    
    # Загрузка компании из company_load.json
    test_company = Company.load_from_file('company_load.json')

    print(f"  Имя сохраненного отдела: {company.name}")
    print(f"  Имя загруженного отдела: {test_company.name}")    
    
    # Экспорт отчетов
    print(f'\n{' Экспорт отчетов ':-^60}\n')

    # Экспорт отчета по сотрудникам
    company.export_employees_csv('employees.csv')
    print(f"    Отчет по сотрудникам сохранен в employees.csv")

    # Экспорт отчета по проектам
    company.export_projects_csv('projects.csv')
    print(f"    Отчет по сотрудникам сохранен в projects.csv")

    print("\n" + "=" * 60)
    print(f"{'Демонстрация завершена!':^60}")
    print("=" * 60)
    
if __name__ == "__main__":
    main()