from typing import Any, Dict, Optional

from BaseTeacherRepository import BaseTeacherRepository
from TeacherDBAdapter import TeacherDBAdapter
from TeacherRepDecorator import (
    AcademicDegreeFilter,
    ExperienceFilter,
    SurnameFilter,
    TeacherRepDecorator,
    TeacherSorter,
)


class TeacherController:
    """
    Контроллер для операций чтения над сущностью преподавателя.
    Вся прикладная логика вынесена сюда и использует репозиторий как модель.
    """

    def __init__(self, repository: Optional[BaseTeacherRepository] = None) -> None:
        # По умолчанию работаем с БД через адаптер
        self.repository: BaseTeacherRepository = repository or TeacherDBAdapter()

    def _apply_filters(self, filters: Dict[str, Any], sort_by: Optional[str]) -> BaseTeacherRepository:
        """
        Оборачивает репозиторий декоратором и применяет фильтры/сортировку,
        если они указаны.
        """
        need_decorator = bool(filters) or sort_by is not None
        if not need_decorator:
            return self.repository

        decorated = TeacherRepDecorator(self.repository)

        # Фильтры
        if filters:
            degree = filters.get("degree")
            if degree:
                decorated.add_filter(AcademicDegreeFilter(degree))

            min_exp = filters.get("min_experience")
            max_exp = filters.get("max_experience")
            if min_exp is not None or max_exp is not None:
                decorated.add_filter(
                    ExperienceFilter(min_experience=min_exp, max_experience=max_exp)
                )

            surname_prefix = filters.get("surname_prefix")
            if surname_prefix:
                decorated.add_filter(SurnameFilter(surname_prefix))

        # Сортировка
        if sort_by:
            sorters = {
                "last_name": TeacherSorter.by_surname(),
                "experience_years": TeacherSorter.by_experience(),
                "academic_degree": TeacherSorter.by_academic_degree(),
                "administrative_position": TeacherSorter.by_position(),
                "email": TeacherSorter.by_email(),
                "id_teacher": TeacherSorter.by_id(),
            }
            sorter = sorters.get(sort_by)
            if sorter:
                decorated.set_sorter(sorter)

        return decorated

    def get_short_teachers(
        self,
        page_size: Optional[int] = None,
        page: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Вернуть сокращенный список преподавателей для главной таблицы.
        Возвращает метаданные пагинации, чтобы фронтенд мог строить страницы.
        """
        page = max(page, 1)
        filters = filters or {}

        repo_to_use = self._apply_filters(filters, sort_by)

        total = repo_to_use.get_count()

        if page_size is None or page_size <= 0:
            # Без явной пагинации возвращаем полный список
            data_slice = repo_to_use.read_all()
            page_size = total if total > 0 else 1
        else:
            # Используем пагинацию репозитория если есть
            if hasattr(repo_to_use, "get_k_n_short_list"):
                data_slice = repo_to_use.get_k_n_short_list(page_size, page)
            else:
                all_data = repo_to_use.read_all()
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
