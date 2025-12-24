import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_all_tests():
    """Запускает ВСЕ тесты из всех папок"""
    args = [
        '-v',           # подробный вывод
        '--tb=short',   # короткие ошибки
        'tests/',       # все тесты из папки tests/
    ]
    return pytest.main(args)

def run_part1():
    """Часть 1: test_core/"""
    return pytest.main(['-v', 'tests/test_core/'])

def run_part2():
    """Часть 2: test_employees/"""
    return pytest.main(['-v', 'tests/test_employees/'])

def run_patterns():
    """Часть 5: test_patterns/"""
    return pytest.main(['-v', 'tests/test_patterns/'])

if __name__ == "__main__":
    print("🎓 ЛАБОРАТОРНАЯ РАБОТА №8 — ВЫБЕРИ:")
    print("1. Все тесты")
    print("2. Часть 1 (Employee)")
    print("3. Часть 2 (Employees)")
    print("4. Паттерны")
    
    choice = input("Выбери (1-4): ").strip()
    
    if choice == '1':
        print("🚀 Запуск ВСЕХ тестов...")
        result = run_all_tests()
    elif choice == '2':
        print("📁 Часть 1: Инкапсуляция...")
        result = run_part1()
    elif choice == '3':
        print("👥 Часть 2: Наследование...")
        result = run_part2()
    elif choice == '4':
        print("🎨 Часть 5: Паттерны...")
        result = run_patterns()
    else:
        print("Запуск ВСЕХ тестов по умолчанию...")
        result = run_all_tests()
    
    print(f"\n🎉 Результат: {result}")
