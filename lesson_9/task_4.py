from subprocess import Popen
import os
def handler():
    count = int(input('Введите кол-во клиентов: '))

    instance_list = [i for i in range(count)]

    for i in instance_list:
        proc = Popen(f"open -n -a Terminal.app {os.path.normpath(os.path.join(f'{os.getcwd()}', '../lesson_4/client.py'))}", shell=True, text=True)
        proc.wait()
        if proc.returncode == 0:
            res_string = f'Узел доступен'
        else:
            res_string = f'Узел недоступен'
        print(res_string)


if __name__== "__main__":
    handler()
