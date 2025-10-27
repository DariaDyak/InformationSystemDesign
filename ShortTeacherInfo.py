from Teacher import Teacher


class ShortTeacherInfo:
    def __init__(self, teacher: Teacher, inn: str, ogrn: str):
        self.last_name = teacher.get_last_name()
        self.initial = f"{teacher.get_first_name()[0]}."
        self.inn = inn
        self.ogrn = ogrn

    def __str__(self) -> str:
        return (
            f"Преподаватель: {self.last_name} {self.initial} " f"ИНН: {self.inn}, ОГРН: {self.ogrn}"
        )

    def __repr__(self) -> str:
        return f"Преподаватель: {self.last_name} {self.initial}"
