from src.hhAPI import HeadHunterAPI
from src.sjAPI import SuperJobAPI
from vacancies import Vacancy
from jsonSaver import JSONSaver
from typing import List


def get_user_keywords() -> List[str]:
    """
    Получает от пользователя ключевые слова для фильтрации вакансий.
    """
    user_keywords_input = input("Введите ключевые слова для фильтрации вакансий (через запятую): ")
    return user_keywords_input.split(",") if user_keywords_input else []


def user_interaction():
    """
    Осуществляет взаимодействие с пользователем, позволяя выбрать API для поиска вакансий,
    вводить поисковый запрос, применять фильтры и выводить результаты.
    Выводит топ N вакансий, предоставленных выбранным API, и сохраняет их в JSON-файл.
    """
    api_choice = input("Выберите API (вбейте 'hh' для hh.ru или 'sj' для superjob.ru): ").lower()

    if api_choice == 'hh':
        job_api = HeadHunterAPI()
    elif api_choice == 'sj':
        job_api = SuperJobAPI()
    else:
        print("Неверный выбор API.")
        return

    json_saver = JSONSaver()
    search_query = input("Введите поисковый запрос: ")
    vacancies = job_api.get_vacancies(search_query)

    if not vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    all_vacancies = [Vacancy(**v) for v in vacancies]

    filter_words = get_user_keywords()
    filtered_vacancies = json_saver.filter_vacancies(all_vacancies, filter_words=filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = json_saver.sort_vacancies(filtered_vacancies)
    top_vacancies = json_saver.get_top_vacancies(sorted_vacancies, top_n=int(input("Введите количество вакансий для вывода: ")))
    json_saver.print_vacancies(top_vacancies)

    # Сохранение вакансий в JSON-файл
    for vacancy in top_vacancies:
        json_saver.add_vacancy(vacancy)

    print("Вакансии успешно сохранены в JSON-файл.")


if __name__ == "__main__":
    user_interaction()
