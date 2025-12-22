from abc import ABC, abstractmethod
from typing import Union
from src.core.company import Company
from src.core.department import Department
from src.core.project import Project
from src.core.abstract_employee import AbstractEmployee
from src.factories.employee_factory import ManagerFactory, DeveloperFactory, SalespersonFactory
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.employees.salesperson import Salesperson


class CompanyFactory(ABC):
    """Абстрактная фабрика для создания компаний (Abstract Factory паттерн)."""
    
    @abstractmethod
    def create_company(self, name: str) -> Company:
        """Создать компанию."""
        pass
    
    @abstractmethod
    def _create_department(self, name: str) -> Department:
        """Создать отдел."""
        pass
    
    @abstractmethod
    def _create_project(self, project_id: int, name: str, description: str, deadline: str) -> Project:
        """Создать проект."""
        pass
    
    @abstractmethod
    def _create_employee(self, **kwargs) -> AbstractEmployee:
        """Создать сотрудника."""
        pass


class TechCompanyFactory(CompanyFactory):
    """Фабрика для создания технической компании."""
    
    def create_company(self, name: str) -> Company:
        """Создать техническую компанию."""
        company = Company(name)
        
        dev_dept = self._create_department("Development")
        qa_dept = self._create_department("QA")
        company.add_department(dev_dept)
        company.add_department(qa_dept)
        
        ai_project = self._create_project(
            project_id=101,
            name="AI Platform",
            description="Разработка AI системы",
            deadline="2024-12-31"
        )
        web_project = self._create_project(
            project_id=102,
            name="Web Portal",
            description="Создание веб-портала",
            deadline="2024-09-30"
        )
        company.add_project(ai_project)
        company.add_project(web_project)
        
        return company
    
    def _create_department(self, name: str) -> Department:
        """Создать технический отдел."""
        return Department(name)
    
    def _create_project(self, project_id: int, name: str, description: str, 
                      deadline: str) -> Project:
        """Создать технический проект."""
        return Project(project_id, name, description, deadline, status="planning")
    
    def _create_employee(self, **kwargs) -> Developer:
        """Создать разработчика."""
        return DeveloperFactory.create_employee(**kwargs)
        

class SalesCompanyFactory(CompanyFactory):
    """Фабрика для создания торговой компании."""
    
    def create_company(self, name: str) -> Company:
        """Создать торговую компанию."""
        company = Company(name)
        
        sal_dept = self._create_department("Sales")
        market_dept = self._create_department("Marketing")
        company.add_department(sal_dept)
        company.add_department(market_dept)
        
        vending_project = self._create_project(
            project_id=201,
            name="Vending",
            description="Вендинг",
            deadline="2024-12-31"
        )
        marketplace_project = self._create_project(
            project_id=202,
            name="Маркетплейс",
            description="Marketplace",
            deadline="2024-09-30"
        )
        company.add_project(vending_project)
        company.add_project(marketplace_project)
        
        return company
    
    def _create_department(self, name: str) -> Department:
        """Создать отдел продаж."""
        return Department(name)
    
    def _create_project(self, project_id: int, name: str, description: str, 
                      deadline: str) -> Project:
        """Создать торговый проект."""
        return Project(project_id, name, description, deadline, status="planning")
    

    def _create_employee(self, **kwargs) -> Union[Manager, Salesperson]:
        """Создать сотрудника (продавца, менеджера)."""
        if "bonus" in kwargs:
            return ManagerFactory.create_employee(**kwargs)
        elif "commission_rate" in kwargs and "sales_volume" in kwargs:
            return SalespersonFactory.create_employee(**kwargs)
        else:
            raise ValueError('Ошибка при создании сотрудника. Недостаточно значений!')
