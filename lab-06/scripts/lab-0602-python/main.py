from functions_as_objects import *
from lambda_closures import *
from higher_order import *
from comprehensions_generators import *
from decorators import *

# Импорты для практических заданий
from functools import reduce

def analyze_students(students):
    """Задание 1"""
    total_grade = reduce(lambda x, y: x + y['grade'], students, 0)
    avg_grade = total_grade / len(students)
    excellent_students = list(filter(lambda s: s['grade'] >= 90, students))
    return {
        'average_grade': round(avg_grade, 2),
        'excellent_students': [s['name'] for s in excellent_students],
        'total_students': len(students)
    }

def logger(func):
    """Задание 2"""
    from functools import wraps
    import datetime
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] Результат: {result}")
        return result
    return wrapper

def prime_generator():
    """Задание 3"""
    yield 2
    candidate = 3
    primes = [2]
    while True:
        is_prime = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
            yield candidate
        candidate += 2

def main():
    print("=== Лабораторная работа 6. Функциональное программирование ===\n")
    
    # Тест Задания 1
    print("1. Анализ студентов:")
    students_data = [
        {'name': 'Alice', 'grade': 85, 'age': 20},
        {'name': 'Bob', 'grade': 92, 'age': 22},
        {'name': 'Charlie', 'grade': 78, 'age': 19},
        {'name': 'Diana', 'grade': 95, 'age': 21},
        {'name': 'Eve', 'grade': 88, 'age': 20}
    ]
    analysis = analyze_students(students_data)
    print(f"   Средний балл: {analysis['average_grade']}")
    print(f"   Отличники: {analysis['excellent_students']}")
    print(f"   Всего студентов: {analysis['total_students']}\n")
    
    # Тест Задания 2
    print("2. Декоратор logger:")
    @logger
    def test_func(x, y):
        return x + y
    test_func(10, 20)
    
    # Тест Задания 3
    print("\n3. Генератор простых чисел:")
    primes = [next(prime_generator()) for _ in range(10)]
    print(f"   Первые 10 простых чисел: {primes}")

if __name__ == "__main__":
    main()
