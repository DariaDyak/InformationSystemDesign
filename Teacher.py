import re
from typing import Any, Dict, Optional


class Teacher:
    def __init__(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        academic_degree: Optional[str] = None,
        administrative_position: Optional[str] = None,
        experience_years: Optional[int] = None,
        data_str: Optional[str] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> None:

        # Создаем локальные переменные с правильными типами
        final_first_name: Optional[str] = first_name
        final_last_name: Optional[str] = last_name
        final_email: Optional[str] = email
        final_academic_degree: Optional[str] = academic_degree
        final_administrative_position: Optional[str] = administrative_position
        final_experience_years: Optional[int] = experience_years

        if json_data is not None:
            try:
                final_first_name = json_data["first_name"]
                final_last_name = json_data["last_name"]
                final_email = json_data["email"]
                final_academic_degree = json_data["academic_degree"]
                final_administrative_position = json_data["administrative_position"]
                final_experience_years = json_data["experience_years"]
            except KeyError as e:
                raise ValueError(f"В json_data отсутствует ключ: {e}")

        elif data_str is not None:
            parts = [p.strip() for p in data_str.split(",")]
            if len(parts) != 6:
                raise ValueError("Строка должна содержать 6 значений")

            # Распаковываем в отдельные переменные с правильными типами
            (
                str_first_name,
                str_last_name,
                str_email,
                str_academic_degree,
                str_administrative_position,
                str_experience_years,
            ) = parts

            final_first_name = str_first_name
            final_last_name = str_last_name
            final_email = str_email
            final_academic_degree = str_academic_degree
            final_administrative_position = str_administrative_position

            try:
                final_experience_years = int(str_experience_years)
            except ValueError:
                raise ValueError("Стаж работы должен быть целым числом")

        # Проверяем, что все обязательные параметры заданы
        if (
            not all(
                [
                    final_first_name,
                    final_last_name,
                    final_email,
                    final_academic_degree,
                    final_administrative_position,
                ]
            )
            or final_experience_years is None
        ):
            raise ValueError("Не все обязательные параметры заданы")

        # Приведение типов (теперь безопасно, так как мы проверили выше)
        first_name_str: str = final_first_name  # type: ignore
        last_name_str: str = final_last_name  # type: ignore
        email_str: str = final_email  # type: ignore
        academic_degree_str: str = final_academic_degree  # type: ignore
        administrative_position_str: str = final_administrative_position  # type: ignore
        experience_years_int: int = final_experience_years  # type: ignore

        # Валидация
        if not self.validate_non_empty_string(first_name_str):
            raise ValueError("Некорректное имя")
        if not self.validate_non_empty_string(last_name_str):
            raise ValueError("Некорректная фамилия")
        if not self.validate_email(email_str):
            raise ValueError("Некорректный email")
        if not self.validate_non_empty_string(academic_degree_str):
            raise ValueError("Некорректная ученая степень")
        if not self.validate_non_empty_string(administrative_position_str):
            raise ValueError("Некорректная должность")
        if not self.validate_experience_years(experience_years_int):
            raise ValueError("Некорректный стаж работы")

        # Устанавливаем атрибуты
        self.__first_name: str = first_name_str
        self.__last_name: str = last_name_str
        self.__email: str = email_str
        self.__academic_degree: str = academic_degree_str
        self.__administrative_position: str = administrative_position_str
        self.__experience_years: int = experience_years_int

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return isinstance(email, str) and re.match(pattern, email) is not None

    @staticmethod
    def validate_non_empty_string(value: str) -> bool:
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def validate_experience_years(years: int) -> bool:
        return isinstance(years, int) and years >= 0

    def set_first_name(self, first_name: str) -> None:
        if not self.validate_non_empty_string(first_name):
            raise ValueError("Некорректное имя")
        self.__first_name = first_name

    def set_last_name(self, last_name: str) -> None:
        if not self.validate_non_empty_string(last_name):
            raise ValueError("Некорректная фамилия")
        self.__last_name = last_name

    def set_email(self, email: str) -> None:
        if not self.validate_email(email):
            raise ValueError("Некорректный email")
        self.__email = email

    def set_academic_degree(self, degree: str) -> None:
        if not self.validate_non_empty_string(degree):
            raise ValueError("Некорректная ученая степень")
        self.__academic_degree = degree

    def set_administrative_position(self, position: str) -> None:
        if not self.validate_non_empty_string(position):
            raise ValueError("Некорректная должность")
        self.__administrative_position = position

    def set_experience_years(self, years: int) -> None:
        if not self.validate_experience_years(years):
            raise ValueError("Некорректный стаж работы")
        self.__experience_years = years

    def get_first_name(self) -> str:
        return self.__first_name

    def get_last_name(self) -> str:
        return self.__last_name

    def get_email(self) -> str:
        return self.__email

    def get_academic_degree(self) -> str:
        return self.__academic_degree

    def get_administrative_position(self) -> str:
        return self.__administrative_position

    def get_experience_years(self) -> int:
        return self.__experience_years

    def __str__(self) -> str:
        return (
            f"Преподаватель: {self.get_first_name()} {self.get_last_name()}, "
            f"Email: {self.get_email()}, Степень: {self.get_academic_degree()}, "
            f"Должность: {self.get_administrative_position()}, "
            f"Стаж: {self.get_experience_years()} лет"
        )

    def __repr__(self) -> str:
        return (
            f"Преподаватель('{self.get_first_name()}', "
            f"'{self.get_last_name()}', '{self.get_email()}')"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Teacher):
            return NotImplemented
        return (
            self.get_first_name() == other.get_first_name()
            and self.get_last_name() == other.get_last_name()
            and self.get_email() == other.get_email()
            and self.get_academic_degree() == other.get_academic_degree()
            and self.get_administrative_position() == other.get_administrative_position()
            and self.get_experience_years() == other.get_experience_years()
        )


class ShortTeacherInfo(Teacher):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        academic_degree: str,
        administrative_position: str,
        experience_years: int,
        inn: str,
        ogrn: str,
    ) -> None:
        super().__init__(
            first_name,
            last_name,
            email,
            academic_degree,
            administrative_position,
            experience_years,
        )
        self.inn: str = inn
        self.ogrn: str = ogrn

    def __str__(self) -> str:
        return (
            f"Преподаватель: {self.get_last_name()} {self.get_first_name()[0]}. "
            f"ИНН: {self.inn}, ОГРН: {self.ogrn}"
        )

    def __repr__(self) -> str:
        return (
            f"Краткая информация: {self.get_last_name()} {self.get_first_name()[0]}, "
            f"ИНН={self.inn}, ОГРН={self.ogrn}"
        )


if __name__ == "__main__":
    t1: Teacher = Teacher(
        "Иван",
        "Иванов",
        "ivan@example.com",
        "Кандидат наук",
        "Заведующий кафедрой",
        10,
    )
    t2: Teacher = Teacher(
        data_str=("Иван, Иванов, ivan@example.com, Кандидат наук, " "Заведующий кафедрой, 10")
    )
    t3: Teacher = Teacher(
        json_data={
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "ivan@example.com",
            "academic_degree": "Кандидат наук",
            "administrative_position": "Заведующий кафедрой",
            "experience_years": 10,
        }
    )
