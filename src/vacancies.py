from bs4 import BeautifulSoup
from io import StringIO


class Vacancy:
    """
    Класс Vacancy представляет вакансию и содержит методы для обработки данных о вакансии.
    """
    def __init__(self, **kwargs):
        """
        Инициализация объекта Vacancy.
        """
        self.id = kwargs.get("id")
        self.title = kwargs.get("name") or kwargs.get("profession", "")
        self.link = kwargs.get("alternate_url") or kwargs.get("link", "")

        # Проверяем наличие ключа "salary" и его значения
        salary_data = kwargs.get("salary")
        self.salary = {
            "from": salary_data.get("from") if salary_data and isinstance(salary_data, dict) else None,
            "to": salary_data.get("to") if salary_data and isinstance(salary_data, dict) else None,
        }

        self.requirements = kwargs.get("snippet", {}).get("requirement", "") or kwargs.get("work", "")
        self.extra_data = kwargs  # Сохраняем дополнительные данные

    def extract_salary(self) -> str:
        """
        Извлекает информацию о заработной плате в формате строки.
        """
        salary_from = self.salary.get("from")
        salary_to = self.salary.get("to")

        if salary_from is not None and salary_to is not None:
            if salary_from == salary_to:
                return f"от {salary_from}"
            else:
                return f"от {salary_from} до {salary_to}"
        elif salary_from is not None:
            return f"от {salary_from}"
        elif salary_to is not None:
            return f"до {salary_to}"
        else:
            # В случае SuperJob используем поле "payment_from"
            salary_from_sj = self.extra_data.get("payment_from", None)
            if salary_from_sj is not None:
                return f"от {salary_from_sj}"
            else:
                return "зарплата не указана"

    def get_requirements(self) -> str:
        """Возвращает требования к кандидату в формате строки."""
        try:
            snippet_requirements = self.extra_data.get('snippet', {}).get('requirement', '')
            work_requirements = self.extra_data.get('work', '')
            requirements = snippet_requirements or work_requirements

            if requirements:
                # Используем StringIO для создания объекта файлового потока
                with StringIO(requirements) as file_stream:
                    soup = BeautifulSoup(file_stream, 'html.parser')
                    return soup.get_text()
            else:
                return "данные отсутствуют, проверьте информацию о требованиях в вакансии по ссылке"
        except Exception as e:
            print(f"Ошибка при обработке HTML: {e}")
            return "данные отсутствуют, проверьте информацию о требованиях в вакансии по ссылке"

    def get_city(self) -> str:
        """Возвращает город вакансии."""
        area_data = self.extra_data.get('area', {}) if 'area' in self.extra_data else {}
        town_data = self.extra_data.get('town', {}) if 'town' in self.extra_data else {}
        return area_data.get('name', town_data.get('title', 'Не указан'))

    def get_currency(self) -> str:
        """
        Возвращает валюту вакансии.
        """
        if self.extra_data:
            salary_data = self.extra_data.get("salary")
            if salary_data and "currency" in salary_data:
                return salary_data["currency"]
            elif "currency" in self.extra_data:
                return self.extra_data["currency"]
            else:
                return "Не указана"
        else:
            return "Не указана"