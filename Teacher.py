import re

class Teacher:
    def __init__(self, first_name, last_name, email, academic_degree, administrative_position, experience_years):
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_email(email)
        self.set_academic_degree(academic_degree)
        self.set_administrative_position(administrative_position)
        self.set_experience_years(experience_years)

    @classmethod
    def from_string(cls, data_str: str):
        parts = [p.strip() for p in data_str.split(',')]
        if len(parts) != 6:
            raise ValueError("Строка должна содержать 6 значений")
        first_name, last_name, email, academic_degree, administrative_position, experience_years = parts
        return cls(first_name, last_name, email, academic_degree, administrative_position, int(experience_years))

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(
            json_data['first_name'],
            json_data['last_name'],
            json_data['email'],
            json_data['academic_degree'],
            json_data['administrative_position'],
            json_data['experience_years']
        )

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

    def __str__(self):
        return (f"Преподаватель: {self.get_first_name()} {self.get_last_name()}, "
                f"Email: {self.get_email()}, Степень: {self.get_academic_degree()}, "
                f"Должность: {self.get_administrative_position()}, Стаж: {self.get_experience_years()} лет")

    def __repr__(self):
        return f"Преподаватель('{self.get_first_name()}', '{self.get_last_name()}', '{self.get_email()}')"

    def __eq__(self, other):
        if not isinstance(other, Teacher):
            return NotImplemented
        return (self.get_first_name() == other.get_first_name() and
                self.get_last_name() == other.get_last_name() and
                self.get_email() == other.get_email() and
                self.get_academic_degree() == other.get_academic_degree() and
                self.get_administrative_position() == other.get_administrative_position() and
                self.get_experience_years() == other.get_experience_years())

class ShortTeacherInfo(Teacher):
    def __init__(self, first_name, last_name, email, academic_degree, administrative_position, experience_years, inn, ogrn):
        super().__init__(first_name, last_name, email, academic_degree, administrative_position, experience_years)
        self.inn = inn
        self.ogrn = ogrn

    def __str__(self):
        return (f"Преподаватель: {self.get_last_name()} {self.get_first_name()[0]}. "
                f"ИНН: {self.inn}, ОГРН: {self.ogrn}")

    def __repr__(self):
        return (f"Краткая информация: {self.get_last_name()} {self.get_first_name()[0]}, ИНН={self.inn}, ОГРН={self.ogrn}")