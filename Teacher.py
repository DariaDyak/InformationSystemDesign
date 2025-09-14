import re

class Teacher:
    def __init__(self, first_name: str, last_name: str, email: str, academic_degree: str, administrative_position: str, experience_years: int):

        if not self.validate_non_empty_string(first_name):
            raise ValueError("Некорректное имя")
        if not self.validate_non_empty_string(last_name):
            raise ValueError("Некорректная фамилия")
        if not self.validate_email(email):
            raise ValueError("Некорректный email")
        if not self.validate_non_empty_string(academic_degree):
            raise ValueError("Некорректная ученая степень")
        if not self.validate_non_empty_string(administrative_position):
            raise ValueError("Некорректная должность")
        if not self.validate_experience_years(experience_years):
            raise ValueError("Некорректный стаж работы")

        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__academic_degree = academic_degree
        self.__administrative_position = administrative_position
        self.__experience_years = experience_years

    # Статические методы валидации
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return isinstance(email, str) and re.match(pattern, email) is not None

    @staticmethod
    def validate_non_empty_string(value: str) -> bool:
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def validate_experience_years(years: int) -> bool:
        return isinstance(years, int) and years >= 0

    # getters (чтение значений)
    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_academic_degree(self):
        return self.__academic_degree

    def get_administrative_position(self):
        return self.__administrative_position

    def get_experience_years(self):
        return self.__experience_years

    # setters с валидацией
    def set_first_name(self, first_name):
        if not self.validate_non_empty_string(first_name):
            raise ValueError("Некорректное имя")
        self.__first_name = first_name

    def set_last_name(self, last_name):
        if not self.validate_non_empty_string(last_name):
            raise ValueError("Некорректная фамилия")
        self.__last_name = last_name

    def set_email(self, email):
        if not self.validate_email(email):
            raise ValueError("Некорректный email")
        self.__email = email

    def set_academic_degree(self, degree):
        if not self.validate_non_empty_string(degree):
            raise ValueError("Некорректная ученая степень")
        self.__academic_degree = degree

    def set_administrative_position(self, position):
        if not self.validate_non_empty_string(position):
            raise ValueError("Некорректная должность")
        self.__administrative_position = position

    def set_experience_years(self, years):
        if not self.validate_experience_years(years):
            raise ValueError("Некорректный стаж работы")
        self.__experience_years = years

    def __str__(self):
        return (f"Преподаватель: {self.__first_name} {self.__last_name}, "
                f"Email: {self.__email}, Степень: {self.__academic_degree}, "
                f"Должность: {self.__administrative_position}, Стаж: {self.__experience_years} лет")