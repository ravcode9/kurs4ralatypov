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

class JSONSaver(AbstractVacancySaver):
    """
    Класс JSONSaver реализует интерфейс AbstractVacancySaver для сохранения вакансий в JSON-файле.

    Методы:
    - add_vacancy(vacancy): Добавляет вакансию в хранилище.
    - get_vacancies_by_salary(min_salary): Возвращает вакансии с зарплатой не ниже указанной.
    - delete_vacancy(vacancy): Удаляет вакансию из хранилища.
    - filter_vacancies(*vacancies, filter_words): Фильтрует вакансии по ключевым словам.
    - sort_vacancies(vacancies): Сортирует вакансии по алфавиту названия.
    - get_top_vacancies(vacancies, top_n): Возвращает топ N вакансий.
    - print_vacancies(vacancies): Выводит информацию о вакансиях.
    """
    def __init__(self, file_path="vacancies.json"):
        self.file_path = file_path
        self.vacancies = []

    def load_from_file(self):
        """Загружает данные из файла в список вакансий."""
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.vacancies = json.load(file)
        else:
            print("Файл с данными пуст или отсутствует.")
            self.vacancies = []

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище."""
        self.load_from_file()
        existing_titles_and_links = [(v.get("title"), v.get("link")) for v in self.vacancies]
        if (vacancy.title, vacancy.link) not in existing_titles_and_links:
            self.vacancies.append({
                "title": vacancy.title,
                "link": vacancy.link,
                "salary": vacancy.extract_salary(),
                "requirements": vacancy.get_requirements(),
                "city": vacancy.get_city(),
                "currency": vacancy.get_currency(),
                "employer": vacancy.get_employer(),
            })
            self.vacancies.sort(key=lambda x: x['title'])  # Сортировка по алфавиту названия
            self.save_to_file()
        else:
            print(f"Вакансия '{vacancy.title}' по ссылке {vacancy.link} уже существует.")

    def get_vacancies_by_salary(self, min_salary: float) -> List[Vacancy]:
        """Возвращает вакансии с зарплатой не ниже указанной."""
        return [Vacancy(**v) for v in self.vacancies if
                float(Vacancy(**v).extract_salary().replace(" ", "")) >= min_salary]

    def delete_vacancy(self, vacancy: Union[Dict[str, str], Vacancy]) -> None:
        """Удаляет вакансию из хранилища."""
        if isinstance(vacancy, dict):
            self.vacancies = [v for v in self.vacancies if
                              v.get("title") != vacancy.get("title") or v.get("link") != vacancy.get("link")]
            self.save_to_file()
        else:
            print("Неверный формат, ожидается словарь.")

    def save_to_file(self):
        """Сохраняет данные в файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=2)

    def filter_vacancies(self, *vacancies: List[Dict[str, str]], filter_words: List[str]) -> List[Dict[str, str]]:
        """Фильтрует вакансии по ключевым словам."""
        filtered_vacancies = []
        for vacancy in vacancies:
            filtered_vacancies.extend([v for v in vacancy if self.word_match(v, filter_words)])
        return filtered_vacancies

    def word_match(self, vacancy: Union[Vacancy, Dict[str, str]], filter_words: List[str]) -> bool:
        """Проверяет, соответствует ли вакансия ключевым словам."""
        if isinstance(vacancy, Vacancy):
            vacancy_data = vacancy.extra_data
        else:
            vacancy_data = vacancy

        return any(word.lower() in str(vacancy_data).lower() for word in filter_words)

    def sort_vacancies(self, vacancies: List[Union[Dict[str, str], Vacancy]]) -> List[Union[Dict[str, str], Vacancy]]:
        """Сортирует вакансии по заработной плате."""
        return sorted(vacancies, key=lambda v: Vacancy(**v).extract_salary() if isinstance(v, dict) else v.extract_salary(), reverse=True)

    def get_top_vacancies(self, vacancies: List[Union[Dict[str, str], Vacancy]], top_n: int) -> List[Union[Dict[str, str], Vacancy]]:
        """Возвращает топ N вакансий."""
        return vacancies[:top_n]

    def print_vacancies(self, vacancies):
        for vacancy in vacancies:
            if isinstance(vacancy, Vacancy):
                print(f"Название: {vacancy.title}")
                print(f"Ссылка: {vacancy.link}")
                print(f"Зарплата: {vacancy.extract_salary()}")
                print(f"Требования: {vacancy.get_requirements()}")
                print(f"Город: {vacancy.get_city()}")
                print(f"Валюта: {vacancy.get_currency()}")
                print(f"Работодатель: {vacancy.get_employer()}")
                print("=" * 50)  # Добавим строку-разделитель
            elif isinstance(vacancy, dict):
                print(f"Название: {vacancy.get('title', 'Не указано')}")
                print(f"Ссылка: {vacancy.get('link', 'Не указана')}")
                print(f"Зарплата: {vacancy.get('salary', 'Не указана')}")
                print(
                    f"Требования: {vacancy.get('requirements', 'данные отсутствуют, проверьте информацию о требованиях в вакансии по ссылке')}")
                print(f"Город: {vacancy.get('city', 'Не указан')}")
                print(f"Валюта: {vacancy.get('currency', 'Не указана')}")
                print(f"Работодатель: {vacancy.get('employer', 'Не указан')}")
                print("=" * 50)  # Добавим строку-разделитель