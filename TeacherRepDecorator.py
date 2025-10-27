from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from BaseTeacherRepository import BaseTeacherRepository


class TeacherFilter(ABC):
    """Базовый класс для фильтров преподавателей"""

    @abstractmethod
    def apply(self, teachers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Применить фильтр к списку преподавателей"""
        pass


class ExperienceFilter(TeacherFilter):
    """Фильтр по опыту работы"""

    def __init__(
        self, min_experience: Optional[int] = None, max_experience: Optional[int] = None
    ) -> None:
        self.min_experience = min_experience
        self.max_experience = max_experience

    def apply(self, teachers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = teachers
        if self.min_experience is not None:
            result = [t for t in result if t.get("experience_years", 0) >= self.min_experience]
        if self.max_experience is not None:
            result = [t for t in result if t.get("experience_years", 0) <= self.max_experience]
        return result


class AcademicDegreeFilter(TeacherFilter):
    """Фильтр по ученой степени"""

    def __init__(self, degree: str) -> None:
        self.degree = degree

    def apply(self, teachers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [t for t in teachers if t.get("academic_degree") == self.degree]


class SurnameFilter(TeacherFilter):
    """Фильтр по фамилии"""

    def __init__(self, starts_with: str) -> None:
        self.starts_with = starts_with.upper()

    def apply(self, teachers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [t for t in teachers if t.get("last_name", "").upper().startswith(self.starts_with)]


class CompositeFilter(TeacherFilter):
    """Композитный фильтр для объединения нескольких условий"""

    def __init__(self) -> None:
        self.filters: List[TeacherFilter] = []

    def add_filter(self, filter_obj: TeacherFilter) -> None:
        """Добавить фильтр в композит"""
        self.filters.append(filter_obj)

    def apply(self, teachers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = teachers
        for filter_obj in self.filters:
            result = filter_obj.apply(result)
        return result


class TeacherSorter:
    """Класс для сортировки преподавателей"""

    @staticmethod
    def by_surname(reverse: bool = False) -> Callable[[Dict[str, Any]], tuple[str, bool]]:
        """Сортировка по фамилии"""
        return lambda t: (t.get("last_name", ""), reverse)

    @staticmethod
    def by_experience(reverse: bool = False) -> Callable[[Dict[str, Any]], tuple[int, bool]]:
        """Сортировка по опыту работы"""
        return lambda t: (t.get("experience_years", 0), reverse)

    @staticmethod
    def by_academic_degree(reverse: bool = False) -> Callable[[Dict[str, Any]], tuple[str, bool]]:
        """Сортировка по ученой степени"""
        return lambda t: (t.get("academic_degree", ""), reverse)

    @staticmethod
    def by_position(reverse: bool = False) -> Callable[[Dict[str, Any]], tuple[str, bool]]:
        """Сортировка по административной должности"""
        return lambda t: (t.get("administrative_position", ""), reverse)

    @staticmethod
    def by_email(reverse: bool = False) -> Callable[[Dict[str, Any]], tuple[str, bool]]:
        """Сортировка по email"""
        return lambda t: (t.get("email", ""), reverse)

    @staticmethod
    def by_id(reverse: bool = False) -> Callable[[Dict[str, Any]], tuple[int, bool]]:
        """Сортировка по ID"""
        return lambda t: (t.get("id_teacher", 0), reverse)


class TeacherRepDecorator(BaseTeacherRepository):
    """
    Паттерн Декоратор (Decorator) для добавления функциональности фильтрации и сортировки.
    Декорирует любой репозиторий из иерархии BaseTeacherRepository.
    """

    def __init__(self, repository: BaseTeacherRepository) -> None:
        """
        Инициализация декоратора
        """
        self._repository = repository
        self.file_path = getattr(repository, "file_path", "")  # Безопасное получение file_path
        self._filters: List[TeacherFilter] = []
        self._sorter: Optional[Callable] = None
        if hasattr(self._repository, "_ensure_file_exists"):
            self._repository._ensure_file_exists()

    def add_filter(self, filter_obj: TeacherFilter) -> None:
        """Добавить фильтр"""
        self._filters.append(filter_obj)

    def set_sorter(self, sorter: Callable) -> None:
        """Установить способ сортировки"""
        self._sorter = sorter

    def clear_filters(self) -> None:
        """Очистить фильтры"""
        self._filters = []

    def clear_sorter(self) -> None:
        """Очистить сортировку"""
        self._sorter = None

    def _apply_filters_and_sorting(self, teachers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Применить фильтры и сортировку к списку преподавателей"""
        result = teachers

        for filter_obj in self._filters:
            result = filter_obj.apply(result)

        if self._sorter:
            try:
                key_func = self._sorter
                if callable(key_func):
                    sample_result = key_func({}) if teachers else (None, False)
                    reverse = (
                        sample_result[1]
                        if isinstance(sample_result, tuple) and len(sample_result) > 1
                        else False
                    )

                    result = sorted(result, key=lambda t: key_func(t)[0], reverse=reverse)
            except (TypeError, IndexError) as e:
                print(f"Ошибка сортировки: {e}")

        return result

    def _ensure_file_exists(self) -> None:
        """Делегирование создания файла декорируемому объекту"""
        self._repository._ensure_file_exists()

    def read_all(self) -> List[Dict[str, Any]]:
        """Чтение всех преподавателей с применением фильтров и сортировки"""
        teachers = self._repository.read_all()
        return self._apply_filters_and_sorting(teachers)

    def write_all(self, data: List[Dict[str, Any]]) -> str:
        """Делегирование записи декорируемому объекту"""
        return self._repository.write_all(data)

    def get_by_id(self, id_teacher: int) -> Optional[Dict[str, Any]]:
        """Делегирование получения по ID"""
        return self._repository.get_by_id(id_teacher)

    def get_k_n_short_list(self, k: int, n: int) -> List[Dict[str, Any]]:
        """
        Получить список с пагинацией с учетом фильтров и сортировки

        Args:
            k: Количество элементов на странице
            n: Номер страницы

        Returns:
            Список преподавателей в коротком формате
        """
        all_teachers = self._repository.read_all()

        # Применяем фильтры и сортировку
        filtered_teachers = self._apply_filters_and_sorting(all_teachers)

        # Применяем пагинацию
        start_index = (n - 1) * k
        end_index = start_index + k

        if start_index >= len(filtered_teachers):
            return []

        return filtered_teachers[start_index:end_index]

    def sort_by_field(self, field: str) -> str:
        """Делегирование сортировки декорируемому объекту"""
        return self._repository.sort_by_field(field)

    def add_teacher(
        self,
        first_name: str,
        last_name: str,
        email: str,
        academic_degree: str,
        administrative_position: str,
        experience_years: int,
    ) -> int:
        """Делегирование добавления"""
        return self._repository.add_teacher(
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
        """Делегирование обновления"""
        return self._repository.update_teacher(
            id_teacher,
            first_name,
            last_name,
            email,
            academic_degree,
            administrative_position,
            experience_years,
        )

    def delete_teacher(self, id_teacher: int) -> str:
        """Делегирование удаления"""
        return self._repository.delete_teacher(id_teacher)

    def get_count(self) -> int:
        """
        Получить количество элементов с учетом фильтров

        Returns:
            Количество преподавателей после применения фильтров
        """
        all_teachers = self._repository.read_all()
        filtered_teachers = self._apply_filters_and_sorting(all_teachers)
        return len(filtered_teachers)
