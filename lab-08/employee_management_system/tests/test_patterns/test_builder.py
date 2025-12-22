import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


from src.patterns.builder import EmployeeBuilder

class TestEmployeeBuilder:
    def test_build_developer_with_builder(self):
        dev = (
            EmployeeBuilder()
            .set_type("developer")
            .set_id(101)
            .set_name("John Doe")
            .set_department("DEV")
            .set_base_salary(5000.0)
            .set_tech_stack(["Python", "Java"])
            .set_seniority_level("senior")
            .build()
        )

        assert dev.id == 101
        assert dev.name == "John Doe"
        assert dev.calculate_salary() == 5000.0 * 2.0  # senior
        assert "Python" in dev.tech_stack
