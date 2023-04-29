from abc import ABC, abstractmethod
import requests

VACANCY_COUNT = 100
PAGE_COUNT = 10
YOUR_KEY = "Введите ваш код доступа к API Superjob"


class API(ABC):
    @abstractmethod
    def get_request(self, keyword, page):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HHVacancy(API):
    """Класс для взаимодействия с HHunterAPI"""
    def get_request(self, keyword, search_count) -> dict:

        url = "https://api.hh.ru/vacancies"

        params = {
            "text": keyword,
            "page": search_count,
            "per_page": VACANCY_COUNT

        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            vacancies = response.json()["items"]
            return vacancies
        else:
            print("Error:", response.status_code)

    def get_vacancies(self, keyword):
        response = []
        for page in range(PAGE_COUNT):
            values = self.get_request(keyword, page)
            response.extend(values)
        return response


class SuperJobVacancy(API):
    """Класс для взаимодействия с SuperJobAPI"""

    def get_request(self, key_word, page):
        auth_data = {'X-Api-App-Id': YOUR_KEY}
        params = {
            "keyword": key_word,
            "page": page,
            "count": VACANCY_COUNT,
        }
        try:
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=auth_data, params=params).json()[
                "objects"]
        except requests.exceptions.ConnectionError as e:
            print(e)
            print("Ошибка при запросе. Ошибка соединения")

        return response

    def get_vacancies(self, keyword):
        response = []
        for page in range(PAGE_COUNT):
            values = self.get_request(keyword, page)
            response.extend(values)
        return response
