from src.core.employee import Employee
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson

class EmployeeFactory:
    """Фабрика для создания объектов сотрудников разных типов."""

    @staticmethod
    def create_employee(emp_type: str, **kwargs):
        """
        Создает объект сотрудника по типу.
        
        :param emp_type: Тип сотрудника ('Employee', 'Manager', 'Developer', 'Salesperson').
        :param kwargs: Аргументы конструктора соответствующего класса.
        """
        emp_type = emp_type.lower()
        if emp_type == "employee":
            return EmployeeFactory._create_employee(**kwargs)
        elif emp_type == "manager":
            return EmployeeFactory._create_manager(**kwargs)
        elif emp_type == "developer":
            return EmployeeFactory._create_developer(**kwargs)
        elif emp_type == "salesperson":
            return EmployeeFactory._create_salesperson(**kwargs)
        else:
            raise ValueError(f'Неизвестный тип сотрудника: {emp_type}.'
                             f'Доступные типы: employee, manager, developer, salesperson')
    

    @staticmethod
    def _create_employee(**kwargs) -> Employee:
        params = ['id', 'name', 'department', 'base_salary']
        EmployeeFactory.check_params(params, kwargs)
        
        return Employee(
            id = kwargs['id'],
            name = kwargs['name'],
            department = kwargs['department'],
            base_salary = kwargs['base_salary']
            )
        
    @staticmethod
    def _create_manager(**kwargs) -> Manager:
        params = ['id', 'name', 'department', 'base_salary', 'bonus']
        EmployeeFactory.check_params(params, kwargs)
        
        return Manager(
            id = kwargs['id'],
            name = kwargs['name'],
            department = kwargs['department'],
            base_salary = kwargs['base_salary'],
            bonus = kwargs['bonus']
        )
        
    @staticmethod
    def _create_developer(**kwargs) -> Developer:
        params = ['id', 'name', 'department', 'base_salary', 'tech_stack', 'seniority_level']
        EmployeeFactory.check_params(params, kwargs)
        
        return Developer(
            id = kwargs['id'],
            name = kwargs['name'],
            department = kwargs['department'],
            base_salary = kwargs['base_salary'],
            tech_stack = kwargs['tech_stack'],
            seniority_level=kwargs['seniority_level']
        )
        
    @staticmethod
    def _create_salesperson(**kwargs) -> Salesperson:
        params = ['id', 'name', 'department', 'base_salary', 'commission_rate', 'sales_volume']
        EmployeeFactory.check_params(params, kwargs)
        
        return Salesperson(
            id = kwargs['id'],
            name = kwargs['name'],
            department = kwargs['department'],
            base_salary = kwargs['base_salary'],
            commission_rate = kwargs['commission_rate'],
            sales_volume = kwargs['sales_volume']
        )
    
    @staticmethod
    def check_params(req_params: list, params: dict):
        missing = [p for p in req_params if p not in params]
        if missing:
            raise ValueError(f"Отсутствуют обязательные параметры: {', '.join(missing)}")