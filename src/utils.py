def user_console():
    """Предлагает пользователю выбрать критерии отбора вакансии и фильтры.
    Возвращает все выборы пользователя"""

    platform = input("Приветствуем!\nВыберите платформы для поиска: 'HHunter' или 'Superjob': (hh/sj) ").lower()
    vacancy = input("Введите название интересующей профессии ").lower()
    search_count = int(input("Введите желаемое количество результатов вывода "))
    top_salary = input("Хотите отсортировать вакансии по самой высокой зарплате? (Да/Нет) ").lower()
    choice = input("Использовать дополнительный фильтр? (Да/Нет) ").lower()
    data_filter = None
    if choice == 'да':
        data_filter = input("Показать только вакансии содержащие: ")
        return platform, vacancy, search_count, top_salary, data_filter
    else:
        return platform, vacancy, search_count, top_salary, data_filter


def sort_salary_min(data):
    """Сортирует вакансии по минимальному значению верхней границы зарплаты"""
    data = sorted(data, key=lambda x: (x.salary_max is not None, x.salary_max), reverse=False)
    return data


def sort_salary_max(data):
    """Сортирует вакансии по максимальному значению верхней границы зарплаты"""
    data = sorted(data, key=lambda x: (x.salary_max is not None, x.salary_max), reverse=True)
    return data


def get_top_vacancies(data_list, top=1):
    """Функция принимает отсортированный список вакансий и возвращает n-ое количество первых вакансий из списка
     Если параметр не задан - возвращает один элемент списка"""
    top_list_data = data_list[0:top]
    return top_list_data


def sort_keyword(data, key):
    """Создает и возвращает список отсортированных вакансий
    по ключевому слову в названии вакансии
    Если ключ не найден возвращает None"""
    sort_data_key = []
    for i in data:
        if key in i.name:
            sort_data_key.append(i)
    if not sort_data_key:
        return None
    else:
        return sort_data_key
