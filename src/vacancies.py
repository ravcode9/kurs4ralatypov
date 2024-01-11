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