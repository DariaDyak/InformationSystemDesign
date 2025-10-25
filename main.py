import BaseTeacherRepository
from TeacherRepJson import TeacherRepJson
from TeacherRepYaml import TeacherRepYaml
from TeacherRepDB import TeacherRepDB
from DatabaseManager import DatabaseManager
from TeacherDBAdapter import TeacherDBAdapter
from TeacherRepDecorator import (TeacherRepDecorator, ExperienceFilter, AcademicDegreeFilter, SurnameFilter,
                                 TeacherSorter, CompositeFilter)

def print_separator(title):
    print(f"\n{title}")

def display_teachers(teachers, title="Список преподавателей"):
    print(f"\n{title}:")
    if not teachers:
        print("  Нет данных")
        return

    for teacher in teachers:
        print(f"  ID {teacher['id_teacher']}: {teacher['last_name']} {teacher['first_name']} "
              f"({teacher['academic_degree']}) - {teacher['email']} - Стаж: {teacher['experience_years']} лет")

def display_short_teachers(short_teachers, title="Короткий список преподавателей"):
    print(f"\n{title}:")
    if not short_teachers:
        print("  Нет данных")
        return

    for teacher in short_teachers:
        print(f"  ID {teacher['id_teacher']}: {teacher['last_name']} {teacher['first_name']} "
              f"({teacher['academic_degree']}) - {teacher['email']}")

def demo_interactive_pagination(teacher_manager, format_name):
    """Интерактивный постраничный просмотр"""
    page_size = 3
    current_page = 1
    total_teachers = teacher_manager.get_count()
    total_pages = (total_teachers + page_size - 1) // page_size

    while True:
        print(f"\nСтраница {current_page} из {total_pages}:")
        short_list = teacher_manager.get_k_n_short_list(page_size, current_page)

        if not short_list:
            print("  На этой странице нет преподавателей")
            if current_page > 1:
                current_page -= 1
            continue

        for i, short_teacher in enumerate(short_list, 1):
            print(f"  {i}. {short_teacher['last_name']} {short_teacher['first_name']} "
                  f"({short_teacher['academic_degree']}) - {short_teacher['email']}")

        print(f"\n  Команды: [n] следующая, [p] предыдущая, [число] перейти на страницу, [q] выход")
        command = input("  Введите команду: ").strip().lower()

        if command == 'q':
            print("  Выход из постраничного просмотра")
            break
        elif command == 'n':
            if current_page < total_pages:
                current_page += 1
            else:
                print("  Это последняя страница!")
        elif command == 'p':
            if current_page > 1:
                current_page -= 1
            else:
                print("  Это первая страница!")
        elif command.isdigit():
            page_num = int(command)
            if 1 <= page_num <= total_pages:
                current_page = page_num
            else:
                print(f"  Номер страницы должен быть от 1 до {total_pages}")
        else:
            print("  Неизвестная команда")

    # def demo_json_format():
    # """Демонстрация работы с JSON форматом"""

def demo_format(teacher_manager, format_name):
    """Общая демонстрация для любого формата"""
    # print_separator("ДЕМОНСТРАЦИЯ РАБОТЫ С JSON ФАЙЛОМ")
    # teacher_manager = TeacherRepJson("teachers.json")

    # 1. Получение количества элементов (метод i)
    print_separator("1. Получение количества элементов (get_count)")
    count = teacher_manager.get_count()
    print(f"  Количество преподавателей в базе: {count}")

    # 2. Чтение всех значений (метод a) - с сортировкой по ID
    print_separator("2. Чтение всех значений (read_all)")
    all_teachers = teacher_manager.read_all()
    all_teachers_sorted = sorted(all_teachers, key=lambda x: x['id_teacher'])
    display_teachers(all_teachers_sorted, "Все преподаватели")

    # 3. Добавление новых преподавателей (метод f)
    print_separator("3. Добавление новых преподавателей (add_teacher)")
    new_teachers = [
        ("Галина", "Борисова", "borisova@university.edu", "Доктор наук", "Декан", 26),
        ("Виталий", "Киселев", "kiselev@university.edu", "Доктор наук", "Профессор", 20),
        ("Лариса", "Михайлова", "mikhailova@university.edu", "Кандидат наук", "Доцент", 12),
        ("Никита", "Титов", "titov@university.edu", "Кандидат наук", "Ассистент", 3)
    ]

    print("  Добавление новых преподавателей:")
    for teacher_data in new_teachers:
        new_id = teacher_manager.add_teacher(*teacher_data)
        if new_id != -1:
            print(f"Добавлен преподаватель с ID {new_id}: {teacher_data[1]} {teacher_data[0]}")
        else:
            print(f"Ошибка при добавлении: {teacher_data[1]} {teacher_data[0]}")

    # 4. Получение объекта по ID (метод c)
    print_separator("4. Получение объекта по ID (get_by_id)")
    test_id = 2
    teacher_by_id = teacher_manager.get_by_id(test_id)
    if teacher_by_id:
        print(f"  Найден преподаватель с ID {test_id}:")
        print(f"    {teacher_by_id['last_name']} {teacher_by_id['first_name']}")
        print(f"    {teacher_by_id['email']}")
        print(f"    {teacher_by_id['academic_degree']}")
        print(f"    {teacher_by_id['administrative_position']}")
        print(f"    Стаж: {teacher_by_id['experience_years']} лет")
    else:
        print(f"  Преподаватель с ID {test_id} не найден")

    # 5. Получение короткого списка (метод d) + сразу интерактивная пагинация
    print_separator("5. Получение короткого списка (get_k_n_short_list)")
    k = 3
    n = 1
    short_list = teacher_manager.get_k_n_short_list(k, n)
    display_short_teachers(short_list, f"Короткий список (страница {n}, по {k} элементов)")

    # demo_interactive_pagination(teacher_manager, "JSON")
    demo_interactive_pagination(teacher_manager, format_name)

    # 6. Сортировка элементов (метод e)
    print_separator("6. Сортировка элементов (sort_by_field)")
    teacher_manager.sort_by_field('last_name')
    sorted_teachers = teacher_manager.read_all()
    display_teachers(sorted_teachers, "Преподаватели после сортировки по фамилии")

    # 7. Обновление элемента (метод g)
    print_separator("7. Обновление элемента (update_teacher)")
    update_id = 2
    print(f"  Обновление преподавателя с ID {update_id}:")
    print("  До обновления:")
    teacher_before = teacher_manager.get_by_id(update_id)
    if teacher_before:
        print(f"    {teacher_before['last_name']} {teacher_before['first_name']}")
        print(f"    {teacher_before['email']}")
        print(f"    {teacher_before['administrative_position']}")
        print(f"    Стаж: {teacher_before['experience_years']} лет")

    result = teacher_manager.update_teacher(
        update_id,
        email="alegr_mar@yandex.ru",
        experience_years=20,
        administrative_position="Старший преподаватель"
    )

    print("  После обновления:")
    if result:
        print(f"    {result['last_name']} {result['first_name']}")
        print(f"    {result['email']}")
        print(f"    {result['administrative_position']}")
        print(f"    Стаж: {result['experience_years']} лет")
    else:
        print("  Преподаватель не найден")

    # 8. Удаление элемента (метод h)
    print_separator("8. Удаление элемента (delete_teacher)")
    delete_id = 3
    print(f"  Удаление преподавателя с ID {delete_id}:")
    teacher_to_delete = teacher_manager.get_by_id(delete_id)
    if teacher_to_delete:
        print(f"    Удаляем: {teacher_to_delete['last_name']} {teacher_to_delete['first_name']}")
        result = teacher_manager.delete_teacher(delete_id)
    else:
        print(f"    Преподаватель с ID {delete_id} не найден")

    # 9. Финальный просмотр всех данных
    final_teachers = teacher_manager.read_all()
    final_teachers_sorted = sorted(final_teachers, key=lambda x: x['id_teacher'])
    display_teachers(final_teachers_sorted, "Финальный список преподавателей")

    # 10. Итоговое количество
    final_count = teacher_manager.get_count()
    print(f"\n  Итоговое количество преподавателей: {final_count}")

    return teacher_manager

'''def demo_yaml_format():
    """Демонстрация работы с YAML форматом"""
    print_separator("ДЕМОНСТРАЦИЯ РАБОТЫ С YAML ФАЙЛОМ")
    teacher_manager = TeacherRepYaml("teachers.yaml")

    # 1. Получение количества элементов (метод i)
    print_separator("1. Получение количества элементов (get_count)")
    count = teacher_manager.get_count()
    print(f"  Количество преподавателей в базе: {count}")

    # 2. Чтение всех значений (метод a) - с сортировкой по ID
    print_separator("2. Чтение всех значений (read_all)")
    all_teachers = teacher_manager.read_all()
    all_teachers_sorted = sorted(all_teachers, key=lambda x: x['id_teacher'])
    display_teachers(all_teachers_sorted, "Все преподаватели")

    # 3. Добавление новых преподавателей (метод f)
    print_separator("3. Добавление новых преподавателей (add_teacher)")
    new_teachers = [
        ("Галина", "Борисова", "borisova@university.edu", "Доктор наук", "Декан", 26),
        ("Виталий", "Киселев", "kiselev@university.edu", "Доктор наук", "Профессор", 20),
        ("Лариса", "Михайлова", "mikhailova@university.edu", "Кандидат наук", "Доцент", 12),
        ("Никита", "Титов", "titov@university.edu", "Кандидат наук", "Ассистент", 3)
    ]

    print("  Добавление новых преподавателей:")
    for teacher_data in new_teachers:
        new_id = teacher_manager.add_teacher(*teacher_data)
        print(f"  Добавлен преподаватель с ID {new_id}: {teacher_data[1]} {teacher_data[0]}")

    # 4. Получение объекта по ID (метод c)
    print_separator("4. Получение объекта по ID (get_by_id)")
    test_id = 2
    teacher_by_id = teacher_manager.get_by_id(test_id)
    if teacher_by_id:
        print(f"  Найден преподаватель с ID {test_id}:")
        print(f"    {teacher_by_id['last_name']} {teacher_by_id['first_name']}")
        print(f"    {teacher_by_id['email']}")
        print(f"    {teacher_by_id['academic_degree']}")
        print(f"    {teacher_by_id['administrative_position']}")
        print(f"    Стаж: {teacher_by_id['experience_years']} лет")
    else:
        print(f"  Преподаватель с ID {test_id} не найден")

    # 5. Получение короткого списка (метод d) + сразу интерактивная пагинация
    print_separator("5. Получение короткого списка (get_k_n_short_list)")
    k = 3
    n = 1
    short_list = teacher_manager.get_k_n_short_list(k, n)
    display_short_teachers(short_list, f"Короткий список (страница {n}, по {k} элементов)")

    demo_interactive_pagination(teacher_manager, "YAML")

    # 6. Сортировка элементов (метод e)
    print_separator("6. Сортировка элементов (sort_by_field)")
    print("  Сортировка по фамилии:")
    teacher_manager.sort_by_field('last_name')
    sorted_teachers = teacher_manager.read_all()
    display_teachers(sorted_teachers, "Преподаватели после сортировки по фамилии")

    # 7. Обновление элемента (метод g)
    print_separator("7. Обновление элемента (update_teacher)")
    update_id = 2
    print(f"  Обновление преподавателя с ID {update_id}:")
    print("  До обновления:")
    teacher_before = teacher_manager.get_by_id(update_id)
    if teacher_before:
        print(f"    {teacher_before['last_name']} {teacher_before['first_name']}")
        print(f"    {teacher_before['email']}")
        print(f"    {teacher_before['administrative_position']}")
        print(f"    Стаж: {teacher_before['experience_years']} лет")

    result = teacher_manager.update_teacher(
        update_id,
        email="alegr_mar@yandex.ru",
        experience_years=20,
        administrative_position="Старший преподаватель"
    )

    print("  После обновления:")
    if result:
        print(f"    {result['last_name']} {result['first_name']}")
        print(f"    {result['email']}")
        print(f"    {result['administrative_position']}")
        print(f"    Стаж: {result['experience_years']} лет")
    else:
        print("  Преподаватель не найден")

    # 8. Удаление элемента (метод h)
    print_separator("8. Удаление элемента (delete_teacher)")
    delete_id = 3
    print(f"  Удаление преподавателя с ID {delete_id}:")
    teacher_to_delete = teacher_manager.get_by_id(delete_id)
    if teacher_to_delete:
        print(f"    Удаляем: {teacher_to_delete['last_name']} {teacher_to_delete['first_name']}")
        result = teacher_manager.delete_teacher(delete_id)
    else:
        print(f"    Преподаватель с ID {delete_id} не найден")

    # 9. Финальный просмотр всех данных
    print_separator("9. Финальный просмотр всех данных")
    final_teachers = teacher_manager.read_all()
    final_teachers_sorted = sorted(final_teachers, key=lambda x: x['id_teacher'])
    display_teachers(final_teachers_sorted, "Финальный список преподавателей")

    # 10. Итоговое количество
    final_count = teacher_manager.get_count()
    print(f"\n  Итоговое количество преподавателей: {final_count}")

    return teacher_manager'''

def demo_database_format():
    """Демонстрация работы с базой данных PostgreSQL"""
    print_separator("ДЕМОНСТРАЦИЯ РАБОТЫ С БАЗОЙ ДАННЫХ")

    try:
        # Используем синглтон DatabaseManager
        db_manager = DatabaseManager()  # Создаем экземпляр класса
        if not db_manager.connect():
            print("Не удалось подключиться к базе данных")
            return None

        # Создаем TeacherRepDB который делегирует работу к DatabaseManager
        teacher_manager = TeacherRepDB()
        return demo_format(teacher_manager, "DATABASE")

    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None

    '''db_connection = DBConnection(
        dbname="postgres",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )

    if not db_connection.connect():
        print("Не удалось подключиться к базе данных")
        return None

    try:
        teacher_manager = TeacherRepDB(db_connection)
        return demo_format(teacher_manager, "DATABASE")

    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        db_connection.disconnect()'''

def demo_adapter_format():
    """Демонстрация работы с адаптером для базы данных"""
    print_separator("ДЕМОНСТРАЦИЯ РАБОТЫ С АДАПТЕРОМ БАЗЫ ДАННЫХ")

    try:
        adapter = TeacherDBAdapter("dummy_path")

        print("Адаптер успешно создан")
        print(f"Тип адаптера: {type(adapter).__name__}")

        from BaseTeacherRepository import BaseTeacherRepository
        is_correct_type = isinstance(adapter, BaseTeacherRepository)
        print(f"Адаптер является экземпляром BaseTeacherRepository: {is_correct_type}")

        if hasattr(adapter, 'clear_table_completely'):
            print("Адаптер имеет специфические методы БД")

        return demo_format(adapter, "ADAPTER")

    except Exception as e:
        print(f"Ошибка при работе с адаптером: {e}")
        return None

def demo_adapter_vs_direct():
    """Сравнительная демонстрация адаптера и прямого доступа к БД"""
    print_separator("СРАВНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ: АДАПТЕР vs ПРЯМОЙ ДОСТУП")

    try:
        # Создаем оба экземпляра'
        direct_db = TeacherRepDB()
        adapter_db = TeacherDBAdapter("dummy_path")

        print("1. Сравнение количества преподавателей:")
        direct_count = direct_db.get_count()
        adapter_count = adapter_db.get_count()
        print(f"   Прямой доступ: {direct_count} преподавателей")
        print(f"   Через адаптер: {adapter_count} преподавателей")
        print(f"   Результаты совпадают: {direct_count == adapter_count}")

        print("\n2. Сравнение чтения данных:")
        direct_teachers = direct_db.read_all()
        adapter_teachers = adapter_db.read_all()
        print(f"   Прямой доступ: {len(direct_teachers)} записей")
        print(f"   Через адаптер: {len(adapter_teachers)} записей")
        print(f"   Данные идентичны: {direct_teachers == adapter_teachers}")

        return adapter_db

    except Exception as e:
        print(f"Ошибка при сравнительной демонстрации: {e}")
        return None

def demo_decorator_functionality():
    """Демонстрация работы декоратора с фильтрами и сортировками"""
    print_separator("ДЕМОНСТРАЦИЯ ПАТТЕРНА ДЕКОРАТОР ДЛЯ БАЗЫ ДАННЫХ")

    try:
        base_db_repo = TeacherRepDB()

        # 1. Демонстрация фильтрации по опыту работы
        print("\n1. Преподаватели с опытом > 15 лет")
        experience_filter = ExperienceFilter(min_experience=15)
        filtered_repo = TeacherRepDecorator(base_db_repo)
        filtered_repo.add_filter(experience_filter)

        filtered_count = filtered_repo.get_count()
        filtered_list = filtered_repo.get_k_n_short_list(10, 1)

        print(f"   Найдено преподавателей: {filtered_count}")
        for teacher in filtered_list:
            print(f"   - {teacher['last_name']} {teacher['first_name']} ({teacher['experience_years']} лет)")

        # 2. Демонстрация фильтрации по ученой степени
        print("\n2. Доктора наук")
        degree_filter = AcademicDegreeFilter("Доктор наук")
        doctors_repo = TeacherRepDecorator(base_db_repo)
        doctors_repo.add_filter(degree_filter)

        doctors_count = doctors_repo.get_count()
        doctors_list = doctors_repo.get_k_n_short_list(10, 1)

        print(f"   Докторов наук: {doctors_count}")
        for teacher in doctors_list:
            print(f"   - {teacher['last_name']} {teacher['first_name']}")

        # 3. Демонстрация сортировки
        print("\n3. По фамилии (по убыванию)")
        sorted_repo = TeacherRepDecorator(base_db_repo)
        sorted_repo.set_sorter(TeacherSorter.by_surname(reverse=True))

        sorted_list = sorted_repo.get_k_n_short_list(5, 1)

        print("   Первые 5 преподавателей отсортированных по фамилии (Z-A):")
        for teacher in sorted_list:
            print(f"   - {teacher['last_name']} {teacher['first_name']}")

        # 4. Демонстрация фильтрации по фамилии
        print("\n4. Фамилия начинается на 'С'")
        surname_filter = SurnameFilter("С")
        surname_repo = TeacherRepDecorator(base_db_repo)
        surname_repo.add_filter(surname_filter)

        surname_count = surname_repo.get_count()
        surname_list = surname_repo.get_k_n_short_list(10, 1)

        print(f"   Преподавателей с фамилией на 'С': {surname_count}")
        for teacher in surname_list:
            print(f"   - {teacher['last_name']} {teacher['first_name']}")

        # 5. Демонстрация комбинированной фильтрации и сортировки
        print("\n5. Доктора наук с опытом > 10 лет, отсортированные по фамилии")
        composite_filter = CompositeFilter()
        composite_filter.add_filter(AcademicDegreeFilter("Доктор наук"))
        composite_filter.add_filter(ExperienceFilter(min_experience=10))

        combined_repo = TeacherRepDecorator(base_db_repo)
        combined_repo.add_filter(composite_filter)
        combined_repo.set_sorter(TeacherSorter.by_surname())

        combined_count = combined_repo.get_count()
        combined_list = combined_repo.get_k_n_short_list(10, 1)

        print(f"   Докторов наук с опытом > 10 лет: {combined_count}")
        for teacher in combined_list:
            print(f"   - {teacher['last_name']} {teacher['first_name']} ({teacher['experience_years']} лет)")

        # 6. Демонстрация разных способов сортировки
        print("\n6. РАЗНЫЕ ВАРИАНТЫ СОРТИРОВКИ")

        sort_options = [
            ("по фамилии (А-Я)", TeacherSorter.by_surname()),
            ("по опыту (по убыванию)", TeacherSorter.by_experience(reverse=True)),
            ("по ученой степени", TeacherSorter.by_academic_degree()),
            ("по должности", TeacherSorter.by_position())
        ]

        for sort_name, sorter in sort_options:
            sorted_repo = TeacherRepDecorator(base_db_repo)
            sorted_repo.set_sorter(sorter)
            sorted_list = sorted_repo.get_k_n_short_list(3, 1)
            print(f"   {sort_name}:")
            for teacher in sorted_list:
                if "опыту" in sort_name:
                    print(f"     - {teacher['last_name']} ({teacher['experience_years']} лет)")
                elif "ученой степени" in sort_name:
                    print(f"     - {teacher['last_name']} ({teacher['academic_degree']})")
                elif "должности" in sort_name:
                    print(f"     - {teacher['last_name']} ({teacher['administrative_position']})")
                else:
                    print(f"     - {teacher['last_name']} {teacher['first_name']}")

        return base_db_repo

    except Exception as e:
        print(f"Ошибка при демонстрации декораторов: {e}")
        return None

def demo_decorator_with_pagination():
    """Демонстрация работы декоратора с пагинацией"""
    print_separator("ДЕКОРАТОР С ПАГИНАЦИЕЙ")

    try:
        # Создаем репозиторий с фильтром и сортировкой
        base_repo = TeacherRepDB()

        # Фильтр: кандидаты наук с опытом > 10 лет, сортировка по фамилии
        composite_filter = CompositeFilter()
        composite_filter.add_filter(AcademicDegreeFilter("Кандидат наук"))
        composite_filter.add_filter(ExperienceFilter(min_experience=10))

        decorated_repo = TeacherRepDecorator(base_repo)
        decorated_repo.add_filter(composite_filter)
        decorated_repo.set_sorter(TeacherSorter.by_surname())

        total_count = decorated_repo.get_count()
        print(f"Всего кандидатов наук с опытом > 10 лет: {total_count}")

        page_size = 3
        total_pages = (total_count + page_size - 1) // page_size

        for page in range(1, total_pages + 1):
            print(f"\nСтраница {page}/{total_pages}:")
            page_data = decorated_repo.get_k_n_short_list(page_size, page)
            for teacher in page_data:
                print(f"   - {teacher['last_name']} {teacher['first_name']} ({teacher['experience_years']} лет)")
        demo_interactive_pagination(decorated_repo, "фильтр: кандидаты наук + опыт > 10 лет")

        return decorated_repo

    except Exception as e:
        print(f"Ошибка при демонстрации пагинации: {e}")
        return None

def main():
    # Демонстрация работы с JSON
    json_manager = demo_format(TeacherRepJson("teachers.json"), "JSON")
    # Демонстрация работы с YAML
    yaml_manager = demo_format(TeacherRepYaml("teachers.yaml"), "YAML")
    # Демонстрация работы с базой данных PostgreSQL
    db_manager = demo_database_format()
    # Демонстрация работы через адаптер
    managers = {}
    adapter_manager = demo_adapter_format()
    managers['adapter'] = adapter_manager
    comparison_manager = demo_adapter_vs_direct()
    managers['comparison'] = comparison_manager
    # Демонстрация функциональности декоратора
    decorator_demo = demo_decorator_functionality()
    # Демонстрация пагинации с декоратором
    pagination_demo = demo_decorator_with_pagination()

if __name__ == "__main__":
    main()