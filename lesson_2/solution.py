# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
# «отчетный» файл в формате CSV. Для этого:
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
# их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных
# выражений извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения каждого параметра поместить в соответствующий список. Должно получиться
# четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции
# создать главный список для хранения данных отчета — например, main_data — и поместить в него названия
# столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
# каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
# В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение
# подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().

import csv
import os
import re
import json
import yaml


current_dir = os.path.dirname(os.path.abspath(__file__))

def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    for file in os.listdir(current_dir):
        if file.endswith('.txt'):
            filepath = os.path.join(current_dir, file)

            with open(filepath) as f_n:
                for line in f_n.readlines():
                    os_name_list += re.findall(r'\w{9}\s{1}\w{7}\s{1}\d{1,2}.?\d?\s\w+.?', line)
                    os_type_list += re.findall(r'\w{1}\d{2}\S{1}\w{5}\s{1}\w{2}', line)
                    os_code_list += re.findall(r'\d{5}-OEM-\d{7}-\d{5}', line)
                    os_prod_list += re.findall(r'[A-Z]{4,6}[\n]', line)

    for i in range(len(os_prod_list)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])
    return main_data


def write_to_csv(filepath):
    data = get_data()
    dir_, filename = os.path.split(filepath)
    os.makedirs(dir_, exist_ok=True)
    filepath = os.path.join(current_dir, dir_, filename)

    with open(filepath, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for line in data:
            writer.writerow(line)
    return filepath


### 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о
# заказах. Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
# количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна предусматривать
# запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4
# пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значени
# й каждого параметра.
#
def write_order_to_json(item, quantity, price, buyer, date ):
    filename = os.path.join(current_dir, 'orders.json')
    if os.path.exists(filename):
        data = {}
        with open(filename, encoding="utf-8") as f_n:
            data = json.loads(f_n.read())
        data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})
        with open(filename, "w", encoding="utf-8") as f_n:
            json.dump(data, f_n, indent=4, separators=(',', ': '), ensure_ascii=False)
        print(f'Данные добавлены в {filename}')
        with open(filename) as f_n:
            objs = json.load(f_n)
            for section, commands in data.items():
                return commands

    else:
        return f'Файл по пути {filename} не найден'


write_order_to_json('macbook', '1', '200000', 'Быстрова', '06.04.2023')
write_order_to_json('macbook2', '2', '200000', 'Быстров', '06.04.2023')


### 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение
# данных в файле YAML-формата. Для этого:
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму
# — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод
# -символом, отсутствующим в кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить
# стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с
# юникодом: allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.

filename = os.path.join(current_dir, 'file.yaml')
dct = {'numbers' : [1, 2, 3], 'number': 1, 'price': {'macbook' : '2000€', 'ipad' : '1000€'}}

with open(filename, 'w') as f_n:
    yaml.dump(dct, f_n, default_flow_style=True, allow_unicode=True)

with open(filename) as f_n:
    print(f_n.read())