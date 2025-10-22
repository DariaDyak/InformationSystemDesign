import json
import os

class TeacherRepJson:

    def __init__(self, json_file="teachers.json"):
        self.json_file = json_file
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    # a. Чтение всех значений из файла
    def read_all(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    # b. Запись всех значений в файл
    def write_all(self, data):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return "ок"

    # c. Получить объект по ID
    def get_by_id(self, id_teacher):
        data = self.read_all()
        for entity in data:
            if entity['id_teacher'] == id_teacher:
                return entity
        return None

    # d. Получить список k по счету n объектов класса
    def get_k_n_short_list(self, k, n):
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
    def sort_by_field(self, field):
        data = self.read_all()
        data.sort(key=lambda x: x[field])
        self.write_all(data)
        return "ок"

    # f. Добавить объект в список (при добавлении сформировать новый ID)
    def add_teacher(self, first_name, last_name, email, academic_degree, administrative_position, experience_years):
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
    def update_teacher(self, id_teacher, first_name=None, last_name=None, email=None, academic_degree=None,
                       administrative_position=None, experience_years=None):
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
    def delete_teacher(self, id_teacher):
        data = self.read_all()
        entity = self.get_by_id(id_teacher)
        if entity:
            data.remove(entity)
            self.write_all(data)
            return "ок"
        return "не найден"

    # i. Получить количество элементов
    def get_count(self):
        data = self.read_all()
        return len(data)