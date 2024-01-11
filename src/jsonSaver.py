from vacancies import Vacancy
from abc import abstractmethod, ABC
import json
from typing import List, Dict, Union
import os


class AbstractVacancySaver(ABC):
    """
    Абстрактный класс AbstractVacancySaver определяет интерфейс для сохранения вакансий.
    """
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, min_salary: float) -> List[Vacancy]:
        """Возвращает вакансии с зарплатой не ниже указанной."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Union[Dict[str, str], Vacancy]) -> None:
        """Удаляет вакансию из хранилища."""
        pass

    @abstractmethod
    def filter_vacancies(self, *vacancies: List[Dict[str, str]], filter_words: List[str]) -> List[Dict[str, str]]:
        """Фильтрует вакансии по ключевым словам."""
        pass

    @abstractmethod
    def sort_vacancies(self, vacancies: List[Union[Dict[str, str], Vacancy]]) -> List[Union[Dict[str, str], Vacancy]]:
        """Сортирует вакансии по заработной плате."""
        pass

    @abstractmethod
    def get_top_vacancies(self, vacancies: List[Union[Dict[str, str], Vacancy]], top_n: int) -> List[Union[Dict[str, str], Vacancy]]:
        """Возвращает топ N вакансий."""
        pass

    @abstractmethod
    def print_vacancies(self, vacancies: List[Union[Dict[str, str], Vacancy]]) -> None:
        """Выводит информацию о вакансиях."""
        pass