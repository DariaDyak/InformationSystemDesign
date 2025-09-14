import Teacher

class ShortTeacherInfo:
    def __init__(self, teacher: Teacher, inn: str, ogrn: str):
        self.last_name = teacher.set_last_name()
        self.initial = f"{teacher.set_first_name()[0]}"
        self.inn = inn
        self.ogrn = ogrn

    def __str__(self):
        return (f"Преподаватель: {self.last_name} {self.initial}, "
                f"INN: {self.inn}, OGRN: {self.ogrn}")

    def __repr__(self):
        return (f"Преподаватель: {self.last_name} {self.initial}")