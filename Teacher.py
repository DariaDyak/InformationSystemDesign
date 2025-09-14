class Teacher:
    def __init__(self, first_name, last_name, email, academic_degree, administrative_position, experience_years):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__academic_degree = academic_degree
        self.__administrative_position = administrative_position
        self.__experience_years = experience_years

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

    # setters (изменение значений)
    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_academic_degree(self, degree):
        self.__academic_degree = degree

    def set_administrative_position(self, position):
        self.__administrative_position = position

    def set_experience_years(self, years):
        self.__experience_years = years

    def __str__(self):
        return (f"Преподаватель: {self.__first_name} {self.__last_name}, "
                f"Email: {self.__email}, Степень: {self.__academic_degree}, "
                f"Должность: {self.__administrative_position}, Стаж: {self.__experience_years} лет")