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
