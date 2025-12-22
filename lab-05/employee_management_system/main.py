import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from examples.demo_patterns import main

if __name__ == "__main__":
    main()