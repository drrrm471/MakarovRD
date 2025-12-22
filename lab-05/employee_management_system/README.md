# **Лабораторная работа 5**  
**Тема:** Организация рабочего окружения и работа с Git. Стратегии ветвления и автоматизация контроля качества.  

## Сведения о студенте
**Дата:** 2025-12-20
**Семестр:** 3
**Группа:** ПИН-б-о-24-1
**Дисциплина:** Технологии программирования
**Студент:** Макаров Роман Дмитриевич

### Структура проекта по системе учета сотрудников

```
employee_management_system/
├── src/                          # Исходный код системы
│   ├── core/                     # Основные классы системы
│   │   ├── __init__.py
│   │   ├── abstract_employee.py  # Абстрактный класс AbstractEmployee
│   │   ├── employee.py           # Базовый класс Employee
│   │   ├── department.py         # Класс Department
│   │   ├── company.py            # Класс Company
│   │   └── project.py            # Класс Project
│   │
│   ├── employees/                # Классы сотрудников
│   │   ├── __init__.py
│   │   ├── manager.py            # Класс Manager
│   │   ├── developer.py          # Класс Developer
│   │   └── salesperson.py        # Класс Salesperson
│   │
│   ├── factories/                # Фабрики и порождающие паттерны
│   │   ├── __init__.py
│   │   ├── employee_factory.py   # EmployeeFactory
│   │   └── company_factory.py    # AbstractFactory для компаний
│   │
│   ├── patterns/                 # Реализации паттернов проектирования
│   │   ├── __init__.py
│   │   ├── singleton.py          # Singleton для DatabaseConnection
│   │   └── builder.py            # EmployeeBuilder
│   │
│   ├── utils/                    # Вспомогательные модули
│   │   ├── __init__.py
│   │   ├── comparators.py        # Компараторы
│   │   └── exceptions.py         # Кастомные исключения
│   │
│   └── database/                 # Работа с базой данных
│       ├── __init__.py
│       └── connection.py         # Singleton для подключения к БД
│
├── data/                         # Данные для тестирования
│   ├── json/                     # JSON файлы для сериализации
│   └── csv/                      # CSV отчеты
│
├── examples/                     # Примеры использования
│   └── demo_part5.py             # Демо Part 5: Паттерны
│
├── README.md                    # Описание проекта
└── main.py                      # Основной скрипт для запуска
```