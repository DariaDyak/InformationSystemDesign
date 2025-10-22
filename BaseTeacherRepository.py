from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseTeacherRepository(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    @abstractmethod
    def _ensure_file_exists(self):
        """Создать файл если он не существует"""
        pass

    @abstractmethod
    def read_all(self) -> List[Dict[str, Any]]:
        """Чтение всех значений из файла"""
        pass

    @abstractmethod
    def write_all(self, data: List[Dict[str, Any]]) -> str:
        """Запись всех значений в файл"""
        pass

    # c. Получить объект по ID
    def get_by_id(self, id_teacher: int) -> Optional[Dict[str, Any]]:
        data = self.read_all()
        for entity in data:
            if entity['id_teacher'] == id_teacher:
                return entity
        return None

    # d. Получить список k по счету n объектов класса
    def get_k_n_short_list(self, k: int, n: int) -> List[Dict[str, Any]]:
        data = self.read_all()
        start = (n - 1) * k
        end = start + k

        short_list = []
        for entity in data[start:end]:
            short_entity = {
                'id_teacher': entity['id_teacher'],
                'last_name': entity['last_name'],
                'first_name': entity['first_name'][0] + '.',
                'email': entity['email'],
                'academic_degree': entity['academic_degree'],
                'administrative_position': entity['administrative_position'],
                'experience_years': entity['experience_years'],
            }
            short_list.append(short_entity)

        return short_list

    # e. Сортировать элементы по выбранному полю
    def sort_by_field(self, field: str) -> str:
        data = self.read_all()
        data.sort(key=lambda x: x[field])
        self.write_all(data)
        return "ок"

    # f. Добавить объект в список (при добавлении сформировать новый ID)
    def add_teacher(self, first_name: str, last_name: str, email: str,
                   academic_degree: str, administrative_position: str,
                   experience_years: int) -> int:
        data = self.read_all()

        new_id = 1
        if data:
            new_id = max(entity['id_teacher'] for entity in data) + 1

        new_entity = {
            'id_teacher': new_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'academic_degree': academic_degree,
            'administrative_position': administrative_position,
            'experience_years': experience_years
        }

        data.append(new_entity)
        self.write_all(data)
        return new_id

    # g. Заменить элемент списка по ID
    def update_teacher(self, id_teacher: int, first_name: str = None,
                      last_name: str = None, email: str = None,
                      academic_degree: str = None, administrative_position: str = None,
                      experience_years: int = None) -> Optional[Dict[str, Any]]:
        data = self.read_all()
        entity = self.get_by_id(id_teacher)

        if entity is None:
            return None

        for i, item in enumerate(data):
            if item['id_teacher'] == id_teacher:
                if first_name:
                    data[i]['first_name'] = first_name
                if last_name:
                    data[i]['last_name'] = last_name
                if email:
                    data[i]['email'] = email
                if academic_degree:
                    data[i]['academic_degree'] = academic_degree
                if administrative_position:
                    data[i]['administrative_position'] = administrative_position
                if experience_years is not None:
                    data[i]['experience_years'] = experience_years
                self.write_all(data)
                return data[i]
        return None

    # h. Удалить элемент списка по ID
    def delete_teacher(self, id_teacher: int) -> str:
        data = self.read_all()
        entity = self.get_by_id(id_teacher)
        if entity:
            data.remove(entity)
            self.write_all(data)
            return "ок"
        return "не найден"

    # i. Получить количество элементов
    def get_count(self) -> int:
        data = self.read_all()
        return len(data)