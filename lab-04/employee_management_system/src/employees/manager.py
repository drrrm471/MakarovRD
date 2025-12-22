from src.core.employee import Employee

class Manager(Employee):
    """Менеджер с бонусом."""

    def __init__(self, id: int, name: str, department: str, base_salary: float, bonus: float):
        """
        Инициализация базовых атрибутов менеджера.
        
        :param id: Уникальный идентификатор менеджера.
        :param name: Имя менеджера.
        :param department: Название отдела.
        :param base_salary: Базовая зарплата менеджера.
        :param bonus: Дополнительная плата, бонус менеджера.
        """
        super().__init__(id, name, department, base_salary)
        self.__bonus = bonus
    

    @property
    def bonus(self):
        """Возвращает бонус менеджера."""
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        """Устанавливает бонус с проверкой."""
        if not isinstance(value, (int, float)):
            raise ValueError("Бонус должен быть числом!")
        if value <= 0:
            raise ValueError("Бонус должен быть положительным числом!")
        self.__bonus = value

    @classmethod
    def from_dict(cls, data: dict) -> 'Manager':
        """Создаёт объект Manager из словаря."""
        if not data['type'] == cls.__name__:
            raise ValueError('Неподходящий тип данных!')
        del data['type']
        required_fields = ['id', 'name', 'department', 'base_salary', 'bonus']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Для создания {cls.__name__} отсутствует поле: '{field}'")
        return cls(**data)

    def __str__(self):
        """Возвращает строковое представление менеджера."""
        return f"Менеджер [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}, бонус: {self.bonus}]"

    def calculate_salary(self):
        """Возвращает сумму базовой зарплаты и бонуса."""
        return float(self.base_salary + self.__bonus)
