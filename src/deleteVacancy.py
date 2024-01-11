from jsonSaver import JSONSaver

if __name__ == "__main__":
    # Пример использования
    json_saver = JSONSaver()

    # Загрузка существующих вакансий из JSON-файла
    json_saver.load_from_file()
    all_vacancies = json_saver.vacancies

    # Определение вакансии, которую нужно удалить на основе её названия и ссылки
    vacancy_to_delete_title = "Программист-разработчик Python"
    vacancy_to_delete_link = "https://www.superjob.ru/vakansii/programmist-razrabotchik-python-42601580.html"

    # Поиск вакансии в списке всех вакансий
    vacancy_to_delete = next((v for v in all_vacancies if v.get("title") == vacancy_to_delete_title and v.get("link") == vacancy_to_delete_link), None)

    if vacancy_to_delete:
        # Удаление вакансии
        json_saver.delete_vacancy(vacancy_to_delete)

        # Сохранение обновлённого списка вакансий в JSON-файл
        json_saver.save_to_file()
        print(f"Вакансия '{vacancy_to_delete_title}' по ссылке {vacancy_to_delete_link} удалена.")
    else:
        print(f"Вакансия '{vacancy_to_delete_title}' по ссылке {vacancy_to_delete_link} не найдена.")
