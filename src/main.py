from src.Interact import InteractWithUser

if __name__ == "__main__":
    user = InteractWithUser()

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
            user.choice_1()
        elif choice == "2":
            user.choice_2()
        elif choice == "3":
            user.choice_3()
        elif choice == "4":
            user.choice_4()
