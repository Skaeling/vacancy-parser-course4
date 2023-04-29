from src.API_classes import HHVacancy, SuperJobVacancy
from src.classes import JSONSaver
from src.utils import user_console, get_top_vacancies, sort_salary_max, sort_salary_min, sort_keyword


def main():
    vacancy_list = []
    platform, user_vacancy, search_count, top_salary, data_filter = user_console()
    if platform == 'sj':
        vacancy_list = SuperJobVacancy()
        vacancy_choice = "SuperJob"
    elif platform == "hh":
        vacancy_list = HHVacancy()
        vacancy_choice = "HeadHunter"
    else:
        print("Нет такой платформы, пожалуйста, выберете другую")
        main()
    vacancy_info = vacancy_list.get_vacancies(user_vacancy)
    json_saver = JSONSaver(user_vacancy, platform)
    json_saver.add_vacancies(vacancy_info)
    data = json_saver.select()
    top_vacancies = get_top_vacancies(data, search_count)
    if top_salary == "да":
        data = sort_salary_max(top_vacancies)
    else:
        data = sort_salary_min(top_vacancies)
    if vacancy_choice:
        print(f"\nВаша подборка вакансий с {vacancy_choice}:\n")
    if data_filter is not None:
        filtered_vacancy = sort_keyword(data, data_filter)
        if filtered_vacancy:
            [print(vacancy, end="\n\n") for vacancy in filtered_vacancy]
        else:
            new_search = input("Нет вакансий, содержащих такое слово\nНачать поиск заново? ").lower()
            if new_search == "да":
                main()
    else:
        [print(vacancy, end="\n\n") for vacancy in data]


if __name__ == "__main__":
    main()
