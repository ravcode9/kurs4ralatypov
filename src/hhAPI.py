from abc import ABC, abstractmethod
import requests
from typing import List


class AbstractJobAPI(ABC):
    """
    Абстрактный класс AbstractJobAPI определяет интерфейс для работы с API вакансий.
    """
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[dict]:
        """
        Получает список вакансий по запросу.
        """
        pass


class HeadHunterAPI(AbstractJobAPI):
    """
    Класс HeadHunterAPI реализует интерфейс AbstractJobAPI для взаимодействия с API HeadHunter.
    """
    API_BASE_URL = "https://api.hh.ru/"

    def get_vacancies(self, search_query: str) -> List[dict]:
        """
        Получает список вакансий по запросу.
        """
        endpoint = "vacancies"
        params = {"text": search_query}

        try:
            response = requests.get(f"{self.API_BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            vacancies = response.json().get("items", [])
            return vacancies
        except requests.exceptions.RequestException as e:
            print(f"Error accessing HeadHunter API: {e}")
            return []