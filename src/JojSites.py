from abc import ABC, abstractmethod
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
