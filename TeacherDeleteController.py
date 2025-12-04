from typing import Dict, Optional

from BaseTeacherRepository import BaseTeacherRepository
from TeacherDBAdapter import TeacherDBAdapter


class TeacherDeleteController:
    """
    Контроллер для удаления преподавателя.
    Выполняет базовую проверку ID и делегирует удаление репозиторию.
    """

    def __init__(self, repository: Optional[BaseTeacherRepository] = None) -> None:
        self.repository: BaseTeacherRepository = repository or TeacherDBAdapter()

    def delete_teacher(self, teacher_id: int) -> Dict[str, object]:
        if not isinstance(teacher_id, int) or teacher_id <= 0:
            return {"success": False, "message": "Некорректный идентификатор"}

        existing = self.repository.get_by_id(teacher_id)
        if not existing:
            return {"success": False, "message": "Преподаватель не найден"}

        result = self.repository.delete_teacher(teacher_id)
        if result != "ок":
            return {"success": False, "message": "Не удалось удалить запись"}

        return {"success": True, "message": "Преподаватель удален"}
