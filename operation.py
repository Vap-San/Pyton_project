from datetime import datetime
import csv
import os

# Минимальная длина заголовка и текста заметки
MIN_LEN = 3

# Основная программа
def run():
    choice = ''
    while choice != '7':
        view_menu()
        choice = input().strip()
        if choice == '1':
            show_in_file()
        if choice == '2':
            add_record()
            show_in_file()
        if choice == '3':
            delete_record()
        if choice == '4':
            edit_record()
        if choice == '5':
            show_records_for_date()
        if choice == '6':
            show_record()
        if choice == '7':
            break

# Вывод меню
def view_menu():

    print("\nВыберите действие:\n"
          "\n1 - вывод всех заметок из файла"
          "\n2 - создание заметки"
          "\n3 - удаление заметки"
          "\n4 - редактирование заметки"
          "\n5 - показать заметки на определенную дату"
          "\n6 - показать заметку по id"
          "\n7 - выход"
          "\n------------------------------------------"
          "\nВведите номер операции: ")


# Запись/добавление в файл
def write_file(array, mode):
    with open("note.csv", mode=mode, newline='', encoding='utf-8') as f:
        fieldnames = list(array[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        if mode == "w":
            writer.writeheader()
            for row in array:
                writer.writerow(row)
        elif mode == "a":
            if size_file_null():
                writer.writeheader()
            rec = array[-1]
            writer.writerow(rec)
    f.close()

# Проверка на пустоту файла
def size_file_null():
    check_file = os.path.getsize("note.csv")
    return not bool(check_file)

# Вывод содержимого файла заметок на экран
def show_in_file():
    filename = 'note.csv'
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=";")
        count = 0
        for row in reader:
            if count == 0:
                print(f'Файл содержит столбцы: {";".join(row)}')
            print(
                f'Код записи: {row["id"]}\nЗаголовок заметки: {row["title"]}\nТекст заметки: {row["text"]}\nДата и время создания заметки: {row["date"]} \n', end='')
            print("-"*80)
            count += 1
        print(f'Всего в файле {count} записей.')
    f.close()

# Заполнение списка из файла заметок
def read_file():
    try:
        array = []
        filename = 'note.csv'
        with open(filename, "r", encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                array.append(row)
        f.close()
    except Exception:
        print('Нет заметок')
    finally:
        return array


# Заполнение полей
def data_entry(row):
    title = input("Введите заголовок заметки: ")
    while len(title) < MIN_LEN:
        title = input("Введите заголовок заметки: ")
    row["title"] = title
    text = input("Введите текст заметки: ")
    while len(text) < MIN_LEN:
        text = input("Введите текст заметки: ")
    row["text"] = text
    row["date"] = str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))


# Вывод списка на экран
def print_array(array):
    for row in array:
        print(
            f'Код записи: {row["id"]}\nЗаголовок заметки: {row["title"]}\nТекст заметки: {row["text"]}\nДата и время создания заметки: {row["date"]} \n', end='')

        print("-"*80)


# Создание новой заметки
def add_record():
    row = {}
    array = read_file()
    row["id"] = 1 if size_file_null() else int(array[-1]["id"])+1
    print(
        f'Длина заголовка и текста заметки должна быть не менее {MIN_LEN} символов\n')
    print("Код новой заметки =", row["id"])
    data_entry(row)
    array.append(row)
    write_file(array, "a")
    print("Заметка добавлена")

# Редактирование заметки по id
def edit_record():
    array = read_file()
    print_array(array)
    id = input("Введите id заметки для редактирования: ")
    result = False
    for row in array:
        if id == row["id"]:
            result = True
            data_entry(row)
            print(f'Заметка с кодом {id} изменена\n')
            write_file(array, 'w')
            print('Смотрим, что в файле\n')
            show_in_file()
    if result == False:
        print('Заметка с таким id не обнаружена\n')


# Удаление записи по ее id
def delete_record():
    array = read_file()
    print_array(array)
    id = input("Введите id заметки для удаления: ")
    result = False
    for row in array:
        if id == row["id"]:
            result = True
            array.remove(row)
            print(f'Заметка с кодом {id} удалена\n')
            write_file(array, 'w')
            print('Смотрим, что в файле\n')
            show_in_file()
    if result == False:
        print('Заметка с таким id не обнаружена\n')

# Вывод на экран заметки по id
def show_record():
    array = read_file()
    id = input("Введите id заметки для просмотра: ")
    result = False
    for row in array:
        if id == row["id"]:
            result = True
            print(
                f'Код записи: {row["id"]}\nЗаголовок заметки: {row["title"]}\nТекст заметки: {row["text"]}\nДата и время создания заметки: {row["date"]} \n', end='')

            print("-"*80)
    if result == False:
        print('Заметка с таким id не обнаружена\n')

# Вывод на экран заметок на определенную дату
def show_records_for_date():
    array = read_file()
    date = input("Введите дату в формате dd.mm.yyyy: ")
    result = False
    for row in array:
        if date in row["date"]:
            result = True
            print(
                f'Код записи: {row["id"]}\nЗаголовок заметки: {row["title"]}\nТекст заметки: {row["text"]}\nДата и время создания заметки: {row["date"]} \n', end='')

            print("-"*80)
    if result == False:
        print('Заметки на указанную дату не обнаружены или дата введена с ошибками\n')