from typing import Any, Dict, List, Optional

from BaseTeacherRepository import BaseTeacherRepository
from TeacherRepDB import TeacherRepDB


class TeacherDBAdapter(BaseTeacherRepository):
    """
    Адаптер для интеграции TeacherRepDB (PostgreSQL)
    в иерархию BaseTeacherRepository
    """

    def __init__(self, file_path: str = "") -> None:
        # file_path игнорируется для БД, но требуется конструктором базового класса
        super().__init__(file_path)
        self.teacher_rep_db = TeacherRepDB()

    def _ensure_file_exists(self) -> None:
        """
        Для БД этот метод обеспечивает существование таблицы.
        В базовом классе это создание файла, здесь - создание таблицы.
        """
        pass

    def read_all(self) -> List[Dict[str, Any]]:
        """Чтение всех преподавателей из БД"""
        return self.teacher_rep_db.read_all()

    def write_all(self, data: List[Dict[str, Any]]) -> str:
        """Запись всех преподавателей в БД (полная перезапись)"""
        return self.teacher_rep_db.write_all(data)

    def get_by_id(self, id_teacher: int) -> Optional[Dict[str, Any]]:
        """Получение преподавателя по ID (оптимизированная версия для БД)"""
        return self.teacher_rep_db.get_by_id(id_teacher)

    def get_k_n_short_list(self, k: int, n: int) -> List[Dict[str, Any]]:
        """Получение короткого списка преподавателей (пагинация на уровне БД)"""
        return self.teacher_rep_db.get_k_n_short_list(k, n)

    def sort_by_field(self, field: str) -> str:
        """
        Сортировка по полю.
        В базовой реализации сортировка в памяти, здесь просто возвращаем 'ок'
        так как в БД сортировка обычно выполняется при запросе
        """
        return self.teacher_rep_db.sort_by_field(field)

    def add_teacher(
        self,
        first_name: str,
        last_name: str,
        email: str,
        academic_degree: str,
        administrative_position: str,
        experience_years: int,
    ) -> int:
        """Добавление нового преподавателя в БД"""
        return self.teacher_rep_db.add_teacher(
            first_name, last_name, email, academic_degree, administrative_position, experience_years
        )

    def update_teacher(
        self,
        id_teacher: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        academic_degree: Optional[str] = None,
        administrative_position: Optional[str] = None,
        experience_years: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """Обновление данных преподавателя в БД"""
        return self.teacher_rep_db.update_teacher(
            id_teacher,
            first_name,
            last_name,
            email,
            academic_degree,
            administrative_position,
            experience_years,
        )

    def delete_teacher(self, id_teacher: int) -> str:
        """Удаление преподавателя по ID из БД"""
        return self.teacher_rep_db.delete_teacher(id_teacher)

    def get_count(self) -> int:
        """Получение общего количества преподавателей из БД"""
        return self.teacher_rep_db.get_count()

    def clear_table_completely(self) -> bool:
        """Очистка таблицы"""
        return self.teacher_rep_db.clear_table_completely()
