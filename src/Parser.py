from abc import ABC, abstractmethod
import re
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("SJ_KEY")


class JobSites(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def parse_vacancies(self):
        pass

    def formatting_vacancies(self, vacancies):
        """Форматирование под единый вид"""

        formatted_list = []
        for index, vacancy in enumerate(vacancies, start=1):
            if not vacancy["client"]:
                client = 'Не указан'
            else:
                client = vacancy["client"]
            if not vacancy["salary_from"] and not vacancy["salary_to"]:
                salary = 'не указан'
                vacancy["currency"] = ''
            else:
                salary_from, salary_to = "", ""
                if vacancy["salary_from"]:
                    salary_from = f'От {vacancy["salary_from"]}'
                if vacancy["salary_to"]:
                    salary_to = f' до {vacancy["salary_to"]}'
                salary = "".join([salary_from, salary_to]).strip()

            formatted_dict = {
                'index': index,
                'title': vacancy["title"],
                'client': client,
                'salary': f'{salary} {vacancy["currency"]}',
                'type_of_work': vacancy["type_of_work"],
                'experience': vacancy["experience"],
                'link': vacancy["link"]
            }

            formatted_list.append(formatted_dict)

        return formatted_list


class HeadHunter(JobSites):

    def get_vacancies(self, search_query, quantity, city):
        """Получение списка вакансий"""

        url = 'https://api.hh.ru/vacancies'

        params = {
            'text': search_query,
            'area': city,
            'per_page': quantity
        }

        try:
            response = requests.get(url, params)
            data = response.json()
            if "items" not in data:
                print("Error: No vacancies found.")
                return []
            vacancies = data["items"]
        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            return []

        return vacancies

    def parse_vacancies(self, vacancies):
        """Выборка нужных параметров"""
        parsed_vacancies = []
        for vacancy in vacancies:
            parsed_vacancy = {
                "title": vacancy['name'],
                "client": vacancy['employer']['name'],
                "salary_from": vacancy['salary']['from'] if "salary" in vacancy and vacancy["salary"] and "from" in
                                                            vacancy['salary'] else None,
                "salary_to": vacancy['salary']['to'] if "salary" in vacancy and vacancy["salary"] and "to" in
                                                        vacancy['salary'] else None,
                "currency": vacancy['salary']['currency'] if "salary" in vacancy and vacancy["salary"] and "currency" in
                                                             vacancy["salary"] else None,
                "type_of_work": vacancy['employment']['name'],
                "experience": vacancy['experience']['name'],
                "link": vacancy['alternate_url'],
            }
            parsed_vacancies.append(parsed_vacancy)

        return parsed_vacancies


class SuperJob(JobSites):

    def get_vacancies(self, search_query, quantity, city):
        """Получение списка вакансий"""

        url = "https://api.superjob.ru/2.0/vacancies"
        headers = {
            'X-Api-App-Id': key
        }
        params = {
            "town": city,  # Укажите город
            "count": quantity,  # Установите количество вакансий для загрузки
            "keyword": search_query
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            data = json.loads(response.text)
            if "objects" not in data:
                print("Error: No vacancies found.")
                return []
            vacancies = data["objects"]
        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            return []

        return vacancies

    def parse_vacancies(self, vacancies):
        """Выборка нужных параметров"""
        parsed_vacancies = []
        for vacancy in vacancies:
            parsed_vacancy = {
                "title": vacancy["profession"],
                "client": vacancy["client"]["title"] if "client" in vacancy and "title" in vacancy["client"] and
                                                        vacancy["client"]["title"] and vacancy["client"][
                                                            "title"] != 0 else None,
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy[
                    "payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None,
                "currency": vacancy["currency"],
                "type_of_work": vacancy["type_of_work"]["title"],
                "experience": vacancy["experience"]["title"],
                "link": vacancy["link"],

            }
            parsed_vacancies.append(parsed_vacancy)

        return parsed_vacancies


class Vacancy:
    def __init__(self, index, title, client, salary, type_of_work, experience, link):
        self.index = index
        self.title = title
        self.client = client
        self.salary = salary
        self.type_of_work = type_of_work
        self.experience = experience
        self.link = link

    def __str__(self):
        return f"""
        'index': {self.index},
        'title': {self.title},
        'client': {self.client},
        'salary': {self.salary}',
        'type_of_work': {self.type_of_work},
        'experience': {self.experience},
        'link': {self.link}
"""

    def __lt__(self, other):
        """Сравнение вакансий по зарплате"""
        return self.salary < other.salary

    def __eq__(self, other):
        """Сравнение вакансий по зарплате"""
        return self.salary == other.salary

    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'index': self.index,
            'title': self.title,
            'client': self.client,
            'salary': self.salary,
            'type_of_work': self.type_of_work,
            'experience': self.experience,
            'link': self.link
        }


class JSONsaver(ABC):
    @abstractmethod
    def save_vacancies(self):
        pass

    @abstractmethod
    def read_vacancies(self):
        pass

    @abstractmethod
    def delete_vacancies(self):
        pass


class SaveJSON(JSONsaver):

    def __init__(self, file_path):
        self.file_path = file_path

    def save_vacancies(self, vacancy):
        """Сохранение в файл"""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancy, file, indent=4, ensure_ascii=False)

    def read_vacancies(self):
        """Чтение файла"""
        with open(self.file_path, "r", encoding="utf-8") as file:
            reading_file = json.load(file, )
            print(json.dumps(reading_file, indent=4, ensure_ascii=False))

    def load_vacancies(self):
        """Создание обьектов класса на основе словарей файла"""
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            vacancies = []
            for item in data:
                vacancy = Vacancy(**item)
                vacancies.append(vacancy)
            return vacancies

    def extract_salary(self, salary):
        """Отделение числовых значений"""
        values = re.findall(r'\d+', salary)
        if len(values) == 1:
            return int(values[0])
        elif len(values) == 2:
            return (int(values[0]) + int(values[1])) / 2
        else:
            return float('')

    def delete_vacancies(self):
        """Удаление вакансий по индексу"""
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        keys_to_delete = input("Введите индексы вакансий, которые нужно удалить (через пробел): ")
        indices = map(int, keys_to_delete.split())

        for index in indices:
            data = [d for d in data if d.get("index") != index]

        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def interact_with_user():
    """Функция работы с пользователем"""
    sj = SuperJob()
    hh = HeadHunter()
    js = SaveJSON("vacancies.json")

    while True:
        print("1. Получить вакансии с HeadHunter")
        print("2. Получить вакансии с SuperJob")
        print("3. Вывести отсортированные по зарплате вакансии")
        print("4. Удалить вакансии")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "0":
            break

        elif choice == "1":
            search_query = input("Введите поисковый запрос: ")
            quantity = input("Введите количество вакансий: ")
            print("1. Москва")
            print("2. Хабаровск")
            value = input("Выберите город поиска: ")
            if value == "1":
                city = 1
            elif value == "2":
                city = 1975
            else:
                print("Не понимаю тебя")
            get_vac = hh.get_vacancies(search_query, quantity, city)
            parsed_vac = hh.parse_vacancies(get_vac)
            formatted_vac = hh.formatting_vacancies(parsed_vac)
            js.save_vacancies(formatted_vac)
            js.read_vacancies()
            if len(formatted_vac) == 0:
                print("Ничего не удалось найти")

        elif choice == "2":
            search_query = input("Введите поисковый запрос: ")
            quantity = input("Введите количество вакансий: ")
            print("1. Москва")
            print("2. Хабаровск")
            value = input("Выберите город поиска: ")
            if value == "1":
                city = "Москва"
            elif value == "2":
                city = "Хабаровск"
            else:
                print("Не понимаю тебя")
            get_vac = sj.get_vacancies(search_query, quantity, city)
            parsed_vac = sj.parse_vacancies(get_vac)
            formatted_vac = sj.formatting_vacancies(parsed_vac)
            js.save_vacancies(formatted_vac)
            js.read_vacancies()
            if len(formatted_vac) == 0:
                print("Ничего не удалось найти")

        elif choice == "3":
            vacancies = js.load_vacancies()

            filtered_vacancies = [vac for vac in vacancies if vac.salary != "не указан "]
            sorted_vacancies = sorted(filtered_vacancies, key=lambda x: js.extract_salary(x.salary), reverse=True)
            for vacancy in sorted_vacancies:
                print(vacancy)

            vacancies_dicts = [vacancy.to_dict() for vacancy in sorted_vacancies]
            js.save_vacancies(vacancies_dicts)


        elif choice == "4":
            js.delete_vacancies()
            print("Вакансии удаленны из файла")


interact_with_user()
