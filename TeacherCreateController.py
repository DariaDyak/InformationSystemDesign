from typing import Any, Dict, Optional

from BaseTeacherRepository import BaseTeacherRepository
from Teacher import Teacher
from TeacherDBAdapter import TeacherDBAdapter


class TeacherCreateController:
    """
    Контроллер для операций создания (используется отдельным окном/вкладкой).
    Выполняет валидацию входных данных перед делегированием в репозиторий.
    """

    def __init__(self, repository: Optional[BaseTeacherRepository] = None) -> None:
        self.repository: BaseTeacherRepository = repository or TeacherDBAdapter()

    def create_teacher(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидирует входные данные и создает запись.
        Возвращает словарь с ключами: success (bool), message (str), id (int | None).
        """
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
                "id": None,
            }

        # Приведение типов и базовая валидация
        try:
            experience = int(payload.get("experience_years"))
        except (TypeError, ValueError):
            return {"success": False, "message": "Стаж должен быть целым числом", "id": None}

        try:
            # Используем доменную модель для проверки корректности полей
            Teacher(
                first_name=str(payload.get("first_name")),
                last_name=str(payload.get("last_name")),
                email=str(payload.get("email")),
                academic_degree=str(payload.get("academic_degree")),
                administrative_position=str(payload.get("administrative_position")),
                experience_years=experience,
            )
        except Exception as exc:
            return {"success": False, "message": str(exc), "id": None}

        # Делегируем создание в репозиторий
        new_id = self.repository.add_teacher(
            payload.get("first_name"),
            payload.get("last_name"),
            payload.get("email"),
            payload.get("academic_degree"),
            payload.get("administrative_position"),
            experience,
        )

        if new_id == -1:
            return {"success": False, "message": "Не удалось добавить преподавателя", "id": None}

        return {"success": True, "message": "Преподаватель добавлен", "id": new_id}
