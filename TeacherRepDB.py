from typing import List, Dict, Any, Optional
from DBConnection import DBConnection

class TeacherRepDB:
    def __init__(self, db_connection: DBConnection):
        self.db = db_connection
        self._ensure_table_exists()
        self._fill_initial_data()

    def _ensure_table_exists(self):
        """Создать таблицу teachers (пересоздает если существует)"""
        # Всегда удаляем и создаем заново для чистого старта
        drop_query = "DROP TABLE IF EXISTS teachers CASCADE"
        self.db.execute_query(drop_query)

        create_table_query = """
        CREATE TABLE teachers (
            id_teacher SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            academic_degree VARCHAR(50),
            administrative_position VARCHAR(50),
            experience_years INTEGER
        )
        """
        self.db.execute_query(create_table_query)

    def _fill_initial_data(self):
        """Заполнить таблицу начальными данными если она пустая"""
        if self.get_count() == 0:
            teachers_data = [
                ("Ирина", "Валерьева", "irina@example.com", "Доктор наук", "Зав кафедрой", 10),
                ("Мария", "Алегрова", "alegrova_m@yandex.ru", "Кандидат наук", "Доцент", 16),
                ("Александр", "Смирнов", "smirnov@university.edu", "Доктор наук", "Декан", 22),
                ("Мария", "Кузнецова", "kuznetsova@university.edu", "Кандидат наук", "Доцент", 14),
                ("Дмитрий", "Попов", "popov@university.edu", "Доктор наук", "Зав кафедрой", 18),
                ("Елена", "Васильева", "vasilieva@university.edu", "Кандидат наук", "Старший преподаватель", 9),
                ("Сергей", "Петров", "petrov@university.edu", "Доктор наук", "Профессор", 25),
                ("Ольга", "Соколова", "sokolova@university.edu", "Кандидат наук", "Доцент", 12),
                ("Андрей", "Михайлов", "mikhailov@university.edu", "Доктор наук", "Зав кафедрой", 20),
                ("Наталья", "Новикова", "novikova@university.edu", "Кандидат наук", "Старший преподаватель", 8)
            ]

            added_count = 0
            for teacher_data in teachers_data:
                new_id = self.add_teacher(*teacher_data)
                if new_id != -1:
                    added_count += 1
                else:
                    print(f"Ошибка при добавлении: {teacher_data[1]} {teacher_data[0]}")

            print(f"Добавлено {added_count} преподавателей")
        else:
            current_count = self.get_count()

    def read_all(self) -> List[Dict[str, Any]]:
        """Чтение всех значений из базы данных"""
        query = """
        SELECT id_teacher, first_name, last_name, email, academic_degree, 
               administrative_position, experience_years 
        FROM teachers 
        ORDER BY id_teacher
        """
        result = self.db.execute_query(query)

        teachers = []
        if result:
            for row in result:
                teachers.append({
                    'id_teacher': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'academic_degree': row[4],
                    'administrative_position': row[5],
                    'experience_years': row[6]
                })
        return teachers

    def write_all(self, data: List[Dict[str, Any]]) -> str:
        """Запись всех значений в базу данных (перезаписывает все данные)"""
        # Очищаем таблицу И сбрасываем последовательность
        self.db.execute_query("TRUNCATE TABLE teachers RESTART IDENTITY")

        for teacher in data:
            query = """
            INSERT INTO teachers (id_teacher, first_name, last_name, email, 
                                academic_degree, administrative_position, experience_years) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (
                teacher['id_teacher'],
                teacher['first_name'],
                teacher['last_name'],
                teacher['email'],
                teacher['academic_degree'],
                teacher['administrative_position'],
                teacher['experience_years']
            ))

        return "ок"

    def clear_table_completely(self):
        """Полностью очистить таблицу и сбросить последовательность ID"""
        try:
            query = "TRUNCATE TABLE teachers RESTART IDENTITY CASCADE"
            result = self.db.execute_query(query)
            print("Таблица полностью очищена, последовательность ID сброшена")
            return True
        except Exception as e:
            print(f"Ошибка при очистке таблицы: {e}")
            return False

    # a. Получить объект по ID
    def get_by_id(self, id_teacher: int) -> Optional[Dict[str, Any]]:
        query = """
        SELECT id_teacher, first_name, last_name, email, academic_degree, 
               administrative_position, experience_years 
        FROM teachers 
        WHERE id_teacher = %s
        """
        result = self.db.execute_query(query, (id_teacher,))

        if result and len(result) > 0:
            row = result[0]
            return {
                'id_teacher': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'academic_degree': row[4],
                'administrative_position': row[5],
                'experience_years': row[6]
            }
        return None

    # b. Получить список k по счету n объектов класса short
    def get_k_n_short_list(self, k: int, n: int) -> List[Dict[str, Any]]:
        offset = (n - 1) * k
        query = """
        SELECT id_teacher, first_name, last_name, email, academic_degree, 
               administrative_position, experience_years 
        FROM teachers 
        ORDER BY id_teacher 
        LIMIT %s OFFSET %s
        """
        result = self.db.execute_query(query, (k, offset))

        short_list = []
        if result:
            for row in result:
                short_entity = {
                    'id_teacher': row[0],
                    'last_name': row[2],
                    'first_name': row[1][0] + '.',
                    'email': row[3],
                    'academic_degree': row[4],
                    'administrative_position': row[5],
                    'experience_years': row[6],
                }
                short_list.append(short_entity)

        return short_list

    # c. Сортировать элементы по выбранному полю
    def sort_by_field(self, field: str) -> str:
        return "ок"

    # d. Добавить объект в список (при добавлении сформировать новый ID)
    def add_teacher(self, first_name: str, last_name: str, email: str,
                    academic_degree: str, administrative_position: str,
                    experience_years: int) -> int:
        try:
            query = """
            INSERT INTO teachers (first_name, last_name, email, academic_degree, 
                                administrative_position, experience_years) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING id_teacher
            """
            result = self.db.execute_query(query, (
                first_name, last_name, email, academic_degree,
                administrative_position, experience_years
            ))

            if result and len(result) > 0 and result[0]:
                new_id = result[0][0]
                print(f"Преподаватель добавлен с ID {new_id}: {last_name} {first_name}")
                return new_id
            else:
                print(f"Не удалось добавить преподавателя {last_name} {first_name}")
                return -1

        except Exception as e:
            print(f"Ошибка при добавлении преподавателя {first_name} {last_name}: {e}")
            return -1

    # e. Заменить элемент списка по ID
    def update_teacher(self, id_teacher: int, first_name: str = None,
                       last_name: str = None, email: str = None,
                       academic_degree: str = None, administrative_position: str = None,
                       experience_years: int = None) -> Optional[Dict[str, Any]]:

        current_teacher = self.get_by_id(id_teacher)
        if not current_teacher:
            return None

        update_data = {
            'first_name': first_name if first_name else current_teacher['first_name'],
            'last_name': last_name if last_name else current_teacher['last_name'],
            'email': email if email else current_teacher['email'],
            'academic_degree': academic_degree if academic_degree else current_teacher['academic_degree'],
            'administrative_position': administrative_position if administrative_position else current_teacher['administrative_position'],
            'experience_years': experience_years if experience_years is not None else current_teacher['experience_years']
        }

        query = """
        UPDATE teachers 
        SET first_name = %s, last_name = %s, email = %s, academic_degree = %s, 
            administrative_position = %s, experience_years = %s
        WHERE id_teacher = %s
        """
        result = self.db.execute_query(query, (
            update_data['first_name'],
            update_data['last_name'],
            update_data['email'],
            update_data['academic_degree'],
            update_data['administrative_position'],
            update_data['experience_years'],
            id_teacher
        ))

        if result == 1:
            return self.get_by_id(id_teacher)
        return None

    # f. Удалить элемент списка по ID
    def delete_teacher(self, id_teacher: int) -> str:
        query = "DELETE FROM teachers WHERE id_teacher = %s"
        result = self.db.execute_query(query, (id_teacher,))
        return "ок" if result == 1 else "не найден"

    # g. Получить количество элементов
    def get_count(self) -> int:
        query = "SELECT COUNT(*) FROM teachers"
        result = self.db.execute_query(query)
        return result[0][0] if result else 0