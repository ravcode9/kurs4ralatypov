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