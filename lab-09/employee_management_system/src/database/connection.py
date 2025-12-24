"""Реализация Singleton"""

import sqlite3


class DatabaseConnection:
    """
    Простая реализация Singleton без потокобезопасности.
    Подходит для однопоточных приложений.
    """

    _instance = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="database.db"):
        if not hasattr(self, "_initialized"):
            self.db_name = db_name
            self._initialized = True

    def get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_name)
            print(f"Создано подключение к: {self.db_name}")
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Подключение закрыто")
