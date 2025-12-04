from typing import Any, Dict, Optional

from BaseTeacherRepository import BaseTeacherRepository
from TeacherDBAdapter import TeacherDBAdapter


class TeacherController:
    """
    Контроллер для операций чтения над сущностью преподавателя.
    Вся прикладная логика вынесена сюда и использует репозиторий как модель.
    """

    def __init__(self, repository: Optional[BaseTeacherRepository] = None) -> None:
        # По умолчанию работаем с БД через адаптер
        self.repository: BaseTeacherRepository = repository or TeacherDBAdapter()

    def get_short_teachers(
        self, page_size: Optional[int] = None, page: int = 1
    ) -> Dict[str, Any]:
        """
        Вернуть сокращенный список преподавателей для главной таблицы.
        Возвращает метаданные пагинации, чтобы фронтенд мог строить страницы.
        """
        page = max(page, 1)
        total = self.repository.get_count()

        if page_size is None or page_size <= 0:
            # Без явной пагинации возвращаем полный список
            data_slice = self.repository.read_all()
            page_size = total if total > 0 else 1
        else:
            # Используем пагинацию репозитория если есть
            if hasattr(self.repository, "get_k_n_short_list"):
                data_slice = self.repository.get_k_n_short_list(page_size, page)
            else:
                all_data = self.repository.read_all()
                start = (page - 1) * page_size
                end = start + page_size
                data_slice = all_data[start:end]

        short_list = []
        for teacher in data_slice:
            first_name_value = teacher.get("first_name", "")
            # Репозитории с коротким списком уже возвращают инициалы, поэтому проверяем хвост
            first_initial = (
                first_name_value
                if first_name_value.endswith(".")
                else f"{first_name_value[:1]}."
            )
            short_list.append(
                {
                    "id": teacher.get("id_teacher"),
                    "last_name": teacher.get("last_name"),
                    "first_initial": first_initial,
                    "email": teacher.get("email"),
                    "academic_degree": teacher.get("academic_degree"),
                    "administrative_position": teacher.get("administrative_position"),
                    "experience_years": teacher.get("experience_years"),
                }
            )

        return {
            "items": short_list,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def get_teacher(self, teacher_id: int) -> Optional[Dict[str, Any]]:
        """Получить полные данные преподавателя по id."""
        return self.repository.get_by_id(teacher_id)
