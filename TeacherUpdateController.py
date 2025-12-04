from typing import Any, Dict, Optional

from BaseTeacherRepository import BaseTeacherRepository
from Teacher import Teacher
from TeacherDBAdapter import TeacherDBAdapter


class TeacherUpdateController:
    """
    Контроллер для редактирования записи (используется отдельным окном/вкладкой).
    Делает валидацию входных данных и делегирует обновление репозиторию.
    """

    def __init__(self, repository: Optional[BaseTeacherRepository] = None) -> None:
        self.repository: BaseTeacherRepository = repository or TeacherDBAdapter()

    def update_teacher(self, teacher_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(teacher_id, int) or teacher_id <= 0:
            return {"success": False, "message": "Некорректный идентификатор", "data": None}

        existing = self.repository.get_by_id(teacher_id)
        if not existing:
            return {"success": False, "message": "Преподаватель не найден", "data": None}

        required_fields = [
            "first_name",
            "last_name",
            "email",
            "academic_degree",
            "administrative_position",
            "experience_years",
        ]

        missing = [f for f in required_fields if f not in payload or payload[f] in (None, "")]
        if missing:
            return {
                "success": False,
                "message": f"Отсутствуют обязательные поля: {', '.join(missing)}",
                "data": None,
            }

        try:
            experience = int(payload.get("experience_years"))
        except (TypeError, ValueError):
            return {"success": False, "message": "Стаж должен быть целым числом", "data": None}

        try:
            Teacher(
                first_name=str(payload.get("first_name")),
                last_name=str(payload.get("last_name")),
                email=str(payload.get("email")),
                academic_degree=str(payload.get("academic_degree")),
                administrative_position=str(payload.get("administrative_position")),
                experience_years=experience,
            )
        except Exception as exc:
            return {"success": False, "message": str(exc), "data": None}

        updated = self.repository.update_teacher(
            teacher_id,
            first_name=payload.get("first_name"),
            last_name=payload.get("last_name"),
            email=payload.get("email"),
            academic_degree=payload.get("academic_degree"),
            administrative_position=payload.get("administrative_position"),
            experience_years=experience,
        )

        if not updated:
            return {"success": False, "message": "Не удалось обновить запись", "data": None}

        return {"success": True, "message": "Данные обновлены", "data": updated}
