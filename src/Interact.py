from src.JSONsaver import SaveJSON
from src.JojSites import SuperJob, HeadHunter

sj = SuperJob()
hh = HeadHunter()
js = SaveJSON("vacancies.json")


class InteractWithUser:

    def choice_1(self):
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

    def choice_2(self):
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

    def choice_3(self):
        vacancies = js.load_vacancies()

        filtered_vacancies = [vac for vac in vacancies if vac.salary != "не указан "]
        sorted_vacancies = sorted(filtered_vacancies, key=lambda x: js.extract_salary(x.salary), reverse=True)
        for vacancy in sorted_vacancies:
            print(vacancy)

        vacancies_dicts = [vacancy.to_dict() for vacancy in sorted_vacancies]
        js.save_vacancies(vacancies_dicts)

    def choice_4(self):
        js.delete_vacancies()
        print("Вакансии удаленны из файла")
