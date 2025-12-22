from src.core.employee import Employee

class Developer(Employee):
    """Разработчик с уровнем seniority и стеком технологий."""

    def __init__(self, id: int, name: str, department: str, base_salary: float, tech_stack: list[str], seniority_level: str):
        """
        Инициализация базовых атрибутов разработчика.
        
        :param id: Уникальный идентификатор разработчика.
        :param name: Имя разработчика.
        :param department: Название отдела.
        :param base_salary: Базовая зарплата разработчика.
        :param tech_stack: Стек технологий разработчика.
        :param seniority_level: Уровень seniority разработчика (junior, middle, senior)
        """
        super().__init__(id, name, department, base_salary)
        self.__tech_stack = tech_stack
        self.__seniority_level = seniority_level

    @property
    def seniority_level(self):
        """Возвращает уровень seniority."""
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value):
        """Устанавливает уровень seniority с валидацией."""
        levels = ["junior", "middle", "senior"]
        if not isinstance(value, str):
            raise ValueError("Уровень Seniority должен быть строкой!")
        if not value.strip():
            raise ValueError("Уровень Seniority не может быть пустой строкой!")
        if value not in levels:
            raise ValueError(f"Уровень Seniority дожен быть в списке: {levels}!")
        self.__seniority_level = value

    @property
    def tech_stack(self):
        """Возвращает стек технологий разработчика."""
        return self.__tech_stack

    @tech_stack.setter
    def tech_stack(self, list_value):
        """Устанавливает стек технологий с проверкой."""
        if not isinstance(list_value, list):
            raise ValueError("Стек технологий должен быть списком (list[str])!")
        if not all(isinstance(item, str) for item in list_value):
            raise ValueError("Содержимое из списка со стеком технологий должно быть строкой!")
        if any(item.strip() == "" for item in list_value):
            raise ValueError("Содержимое из списка со стеком технологий не может быть пустой строкой!")
        self.__tech_stack = list_value

    def __str__(self):
        """Возвращает строковое представление разработчика."""
        return f"Разработчик [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}, стек технологий: {self.tech_stack}, уровень Seniority: {self.seniority_level}]"

    def __iter__(self):
        """Позволяет итерироваться по стеку технологий."""
        return iter(self.tech_stack)

    @classmethod
    def from_dict(cls, data: dict) -> Employee:
        """Создаёт объект Developer из словаря."""
        if not data['type'] == cls.__name__:
            raise ValueError('Неподходящий тип данных!')
        del data['type']
        required_fields = ['id', 'name', 'department', 'base_salary', 'tech_stack', 'seniority_level']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Для создания {cls.__name__} отсутствует поле: '{field}'")
        return cls(**data)

    def calculate_salary(self):
        """Вычисляет зарплату в зависимости от уровня seniority."""
        coef = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return self.base_salary * coef.get(self.__seniority_level)

    def add_skill(self, new_skill: str) -> None:
        """Добавляет новую технологию в стек."""
        if not isinstance(new_skill, str):
            raise ValueError("Технология стека должна быть строкой!")
        if not new_skill.strip():
            raise ValueError("Технология стека не может быть пустой строкой!")
        self.tech_stack.append(new_skill)

