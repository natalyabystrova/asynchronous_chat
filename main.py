#1 Каждое из слов «разработка», «сокет», «декоратор»
# представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера
# преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных

strings = ['разработка', 'сокет', 'декоратор']


for s in strings:
    print(s, type(s))


unicode_strs = ["\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430", "\u0441\u043e\u043a\u0435\u0442", "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"]

for i in unicode_strs:
    print(i, type(i))

# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без
# преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.

words = [b'class', b'function', b'method']

for w in words:
    print(f'тип переменной: {type(w)}')
    print(f'содержание переменной - {w}')
    print(f'длинна строки: {len(w)}')

# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

var2 = b'attribute'
var3 = b'класс'
var4 = b'функция'
var5 = b'type'

# Невозможно записать в байтовом типе строки записанные на кириллице- 'класс' и 'функция'.
# SyntaxError: bytes can only contain ASCII literal characters.


# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
# строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode)

words_2 = ['разработка', 'администрирование', 'protocol', 'standard']
for w in words_2:
    a = w.encode('utf-8')
    b = bytes.decode(a, 'utf-8')
    print(a, type(a), b, type(b))


# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на кириллице.
#
import subprocess

ping_resource = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]

for p in ping_resource:
    ping_process = subprocess.Popen(p, stdout=subprocess.PIPE)
    for line in ping_process.stdout:
        print(f'bytes_line: {line}')
        line_2 = line.decode('cp866').encode('utf-8').decode('utf-8')
        print(f' line_decode: {line_2}')



# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
# «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.

import locale

resource_string_2 = ['сетевое программирование', 'сокет', 'декоратор']

with open('resource.txt', 'w+') as f:
    for i in resource_string_2:
        f.write(i + '\n')
    f.seek(0)

print(f)

file_coding = locale.getpreferredencoding()


with open('resource.txt', 'r', encoding=file_coding) as f:
    for i in f:
        print(i)
    f.seek(0)