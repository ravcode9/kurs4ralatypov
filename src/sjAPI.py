from abc import ABC, abstractmethod
import os
from typing import List, Optional
import requests


class AbstractJobAPI(ABC):
    """
    Абстрактный класс AbstractJobAPI определяет интерфейс для работы с API вакансий.
    """
    @abstractmethod
    def get_vacancies(self, search_query: str, **params) -> List[dict]:
        """
        Получает список вакансий по запросу.
        """
        pass


class SuperJobAPI(AbstractJobAPI):
    """
    Класс SuperJobAPI реализует интерфейс AbstractJobAPI для взаимодействия с API SuperJob.
    """
    API_BASE_URL = "https://api.superjob.ru/2.0/"

    def __init__(self):
        superjob_token = os.getenv("API_SUPERJOB")
        if not superjob_token:
            raise ValueError("API_SUPERJOB token is missing in environment variables.")
        self.api_key = superjob_token

    def get_vacancies(
        self,
        search_query: str,
        order_field: str = "payment",
        order_direction: str = "asc",
        payment_from: Optional[int] = None,
        payment_to: Optional[int] = None,
        **kwargs
    ) -> List[dict]:
        """
        Получает список вакансий по запросу.
        """
        endpoint = "vacancies/"
        headers = {
            "X-Api-App-Id": self.api_key,
        }
        params = {
            "keyword": search_query,
            "order_field": order_field,
            "order_direction": order_direction,
            "payment_from": payment_from,
            "payment_to": payment_to,
            **kwargs,
        }

        try:
            response = requests.get(f"{self.API_BASE_URL}{endpoint}", headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            vacancies = data.get("objects", [])
            return vacancies
        except requests.exceptions.RequestException as e:
            print(f"Error accessing SuperJob API: {e}")
            return []
