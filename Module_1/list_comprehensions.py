def filter_list(list_student):
    new_list = [
        student for student in list_student if student["avg_grade"] > 4
    ]
    return new_list


if __name__ == "__main__":
    list_student = [
        {
            "name": "Вася",
            "avg_grade": 5,
        },
        {
            "name": "Петя",
            "avg_grade": 1.5,
        },
        {
            "name": "Тася",
            "avg_grade": 2.2,
        },
        {
            "name": "Нина",
            "avg_grade": 8,
        },
        {
            "name": "Маша",
            "avg_grade": 9,
        },
    ]
    print(f"Список студентов {filter_list(list_student)}")
