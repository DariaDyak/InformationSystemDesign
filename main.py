from TeacherRepJson import TeacherRepJson
from TeacherRepYaml import TeacherRepYaml

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

def demo_json_format():
    """Демонстрация работы с JSON форматом"""
    print_separator("ДЕМОНСТРАЦИЯ РАБОТЫ С JSON ФАЙЛОМ")
    teacher_manager = TeacherRepJson("teachers.json")

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

    demo_interactive_pagination(teacher_manager, "JSON")

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
    final_teachers = teacher_manager.read_all()
    final_teachers_sorted = sorted(final_teachers, key=lambda x: x['id_teacher'])
    display_teachers(final_teachers_sorted, "Финальный список преподавателей")

    # 10. Итоговое количество
    final_count = teacher_manager.get_count()
    print(f"\n  Итоговое количество преподавателей: {final_count}")

    return teacher_manager

def demo_yaml_format():
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

    return teacher_manager


def main():
    # Демонстрация работы с JSON
    json_manager = demo_json_format()

    # Демонстрация работы с YAML
    yaml_manager = demo_yaml_format()

if __name__ == "__main__":
    main()