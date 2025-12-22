import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print('aaaa', project_root)

from src.patterns.singleton import DatabaseConnection

class TestSingletonDatabaseConnection:
    def test_singleton_instance_is_same(self):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()

        assert db1 is db2
        assert id(db1) == id(db2)

    def test_get_connection_returns_same_object(self):
        db = DatabaseConnection()
        conn1 = db.get_connection()
        conn2 = db.get_connection()

        assert conn1 is conn2
