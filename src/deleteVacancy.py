from jsonSaver import JSONSaver

if __name__ == "__main__":
    # Пример использования
    json_saver = JSONSaver()

    # Загрузка существующих вакансий из JSON-файла
    all_vacancies = json_saver.vacancies

    # Определение вакансии, которую нужно удалить на основе её названия и ссылки
    vacancy_to_delete_title = "вставь название вакансии"
    vacancy_to_delete_link = "вставь ссылку вакансии"

    # Поиск вакансии в списке всех вакансий
    vacancy_to_delete = next((v for v in all_vacancies if v.get("title") == vacancy_to_delete_title and v.get("link") == vacancy_to_delete_link), None)

    if vacancy_to_delete:
        # Удаление вакансии
        json_saver.delete_vacancy(vacancy_to_delete)

        # Сохранение обновлённого списка вакансий в JSON-файл
        json_saver.save_to_file()
    else:
        print("Вакансия не найдена.")