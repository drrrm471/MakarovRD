import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


from src.core.company import Company
from src.factories.company_factory import TechCompanyFactory, SalesCompanyFactory

class TestCompanyFactories:
    def test_tech_company_factory_creates_company_with_departments_and_projects(self):
        factory = TechCompanyFactory()

        company = factory.create_company("TechCorp")

        assert isinstance(company, Company)
        deps = company.get_departments()
        projs = company.get_projects()

        assert any(d.name == "Development" for d in deps)
        assert any(d.name == "QA" for d in deps)
        assert any(p.name == "AI Platform" for p in projs)
        assert any(p.name == "Web Portal" for p in projs)

    def test_sales_company_factory_creates_company_with_departments_and_projects(self):
        factory = SalesCompanyFactory()

        company = factory.create_company("SalesCorp")

        deps = company.get_departments()
        projs = company.get_projects()

        assert any(d.name == "Sales" for d in deps)
        assert any(d.name == "Marketing" for d in deps)
        assert any(p.name == "Vending" for p in projs)
        assert any("Маркетплейс" in p.name for p in projs)
