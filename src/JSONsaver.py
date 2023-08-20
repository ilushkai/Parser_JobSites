from abc import ABC, abstractmethod
import re
import json
from src.Vacancies import Vacancy

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


