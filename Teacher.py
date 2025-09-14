import re

class Teacher:
    def __init__(self, first_name: str, last_name: str, email: str, academic_degree: str, administrative_position: str, experience_years: int):
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

    # Универсальный метод для валидации
    def __validate_and_set(self, attr_name: str, value, validator, error_message: str):
        if not validator(value):
            raise ValueError(error_message)
        setattr(self, attr_name, value)

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

    # setters с универсальным методом
    def set_first_name(self, first_name):
        self.__validate_and_set('_Teacher__first_name', first_name, self.validate_non_empty_string, "Некорректное имя")

    def set_last_name(self, last_name):
        self.__validate_and_set('_Teacher__last_name', last_name, self.validate_non_empty_string, "Некорректная фамилия")

    def set_email(self, email):
        self.__validate_and_set('_Teacher__email', email, self.validate_email, "Некорректный email")

    def set_academic_degree(self, degree):
        self.__validate_and_set('_Teacher__academic_degree', degree, self.validate_non_empty_string, "Некорректная ученая степень")

    def set_administrative_position(self, position):
        self.__validate_and_set('_Teacher__administrative_position', position, self.validate_non_empty_string, "Некорректная должность")

    def set_experience_years(self, years):
        self.__validate_and_set('_Teacher__experience_years', years, self.validate_experience_years, "Некорректный стаж работы")

    def __str__(self):
        return (f"Преподаватель: {self.__first_name} {self.__last_name}, "
                f"Email: {self.__email}, Степень: {self.__academic_degree}, "
                f"Должность: {self.__administrative_position}, Стаж: {self.__experience_years} лет")