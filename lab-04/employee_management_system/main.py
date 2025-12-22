import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def main():
    """Главная функция для запуска всех демонстраций."""
    print("=" * 60)
    print(f"{'СИСТЕМА УЧЕТА СОТРУДНИКОВ КОМПАНИИ':^60}")
    print(f"{'Лабораторная работа 4: Реализация принципов ООП':^60}")
    print("=" * 60, '\n')

    print("\t  Доступные демонстрации:")
    print("  1.  Часть 1: Инкапсуляция")
    print("  2.  Часть 2: Наследование и абстракция")
    print("  3.  Часть 3: Полиморфизм и магические методы")
    print("  4.  Часть 4: Композиция и агрегация")
    print("  5.  Запуск всех демонстраций")
    print("  0.  Завершение программы")


    while True:
        try:
            choice = input(f'\nВведите команду: ')

            if choice == '1':
                import examples.demo_part1 as demo1
                demo1.main()
                break

            elif choice == '2':
                import examples.demo_part2 as demo2
                demo2.main()
                break

            if choice == '3':
                import examples.demo_part3 as demo3
                demo3.main()
                break

            if choice == '4':
                import examples.demo_part4 as demo4
                demo4.main()
                break

            if choice == '5':
                import examples.demo_part1 as demo1
                demo1.main()

                import examples.demo_part2 as demo2
                demo2.main()

                import examples.demo_part3 as demo3
                demo3.main()

                import examples.demo_part3 as demo3
                demo3.main()
                break

            elif choice == '0':
                print('  Программа завершена!')
                break

            else:
                print('Неверный выбор, попробуйте снова!')
        except:
            print('Ошибка демонстрации.')

if __name__ == "__main__":
    main()