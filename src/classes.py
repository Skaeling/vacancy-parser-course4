import json
from abc import ABC, abstractmethod


class ParentJSONSaver(ABC):
    """Родительский класс для классов, работающих с данными о вакансиях """

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def select(self):
        pass


class Vacancy:
    """Класс для работы с вакансиями"""
    def __init__(self, name, salary_min, salary_max, currency, employer, url):
        self.name = name
        self.url = url
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.employer = employer
        self.currency = currency

        if currency and currency.capitalize() == "EUR":
            self.salary_min = self.salary_min * 89 if self.salary_min else None
            self.salary_max = self.salary_max * 89 if self.salary_max else None
            self.currency = "RUR"
        elif currency and currency.capitalize() == "USD":
            self.salary_min = self.salary_min * 81 if self.salary_min else None
            self.salary_max = self.salary_max * 81 if self.salary_max else None
            self.currency = "RUR"
        else:
            self.currency = "RUR"

    def __str__(self):
        if self.currency:
            self.currency = f"Зарплата({self.currency}) "
        else:
            self.currency = "Зарплата не указана"
        if self.salary_min:
            self.salary_min = f" от {self.salary_min}"
        else:
            self.salary_min = ""
        if self.salary_max:
            self.salary_max = f" до {self.salary_max}"
        else:
            self.salary_to = ""

        msg = f"{self.employer}:  {self.name}\n" \
              f"URL вакансии: {self.url} \n" \
              f"{self.currency}{self.salary_min} {self.salary_max}\n"
        return msg

    def __gt__(self, other):
        """Метод сравнения по зарплате"""
        if not other.salary_min:
            return True
        if not self.salary_min:
            return False
        return self.salary_min >= other.salary_min


class JSONSaver:
    """Класс для сохранения информации о вакансиях в JSON-файл"""
    def __init__(self, keyword, platform):
        self.__filename = f'{keyword.title()}_{platform.lower()}.json'

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.__filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        vacancies = []
        salary_min, salary_max, currency = None, None, None
        if "hh" in self.filename:
            for row in data:
                if row['salary']:
                    salary_min, salary_max, currency = row['salary']['from'], row['salary']['to'], row['salary'][
                        'currency']  # добавить условие про рубли и перевод
                vacancies.append(Vacancy(row['name'], salary_min, salary_max, currency, row['employer']['name'],
                                         row['alternate_url']))
            return vacancies

        if "sj" in self.filename:
            for row in data:
                if row['currency']:
                    salary_min, salary_max, currency = row['payment_from'], row['payment_to'], row[
                        'currency']  # добавить условие про рубли и перевод
                vacancies.append(
                    Vacancy(row['profession'], salary_min, salary_max, currency, row['firm_name'], row['link']))
            return vacancies
