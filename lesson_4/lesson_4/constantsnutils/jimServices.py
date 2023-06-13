
from config import *
import json
import time

def getopts(argv):
    """
    Принимает набор параметров из командной строки и возвращает словарь, где ключ - имя параметра, значение - значение парметра, заданное пользователем
    По умолчанию возвращает 
    :param список параметров
    :return словарь параметров
    """
    opts={"p":PORT, "a":HOSTS, NAME:"Guest"}

    while argv:
        k=argv[0].split(":")
        if  k[0]=="r":
            opts[argv[0]] = READCLIENT
        elif k[0]=="p":
            opts[argv[0]] = int(argv[0])       
        elif k[0]=="a":            
            opts[argv[0]] = argv[0]
        elif k[0]==NAME:            
             opts[k[0]] = k[1]
        argv = argv[1:]
    return opts

def dictToBytes(d):
    """
    Перевод словаря в байты.
    :param: d - словрь
    """
    if isinstance(d, dict):
        return json.dumps(d,ensure_ascii=False).encode(ENCODING)
    else:
        raise TypeError

def bytesToDict(b):
    """
    Перевод байт в словарь.
    :param: b - байты
    """
    if isinstance(b, bytes):
        return dict(json.loads(b.decode(ENCODING)))
    else:
        raise TypeError
        
    
def sendMessage(sock, message):
    """
    Отправка сообщения
    :param sock: сокет
    :param message: словарь сообщения
    :return: None
    """
    # Словарь переводим в байты
    bprescence = dictToBytes(message)
    # Отправляем
    sock.send(bprescence)


def getMessage(sock):
    """
    Получение сообщения
    :param sock:
    :return: словарь ответа
    """
    # Получаем байты
    bresponse = sock.recv(1024)
    # переводим байты в словарь
    response = bytesToDict(bresponse)
    # возвращаем словарь
    return response


def createMessage(user_message, from_account="Guest", to_account="#all"):

    message = {ACTION: MSG, TIME: time.time(), TO: to_account, USER: {ACCOUNT_NAME:from_account}, MSG: user_message}
    
    return message