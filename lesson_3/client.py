import json
import sys
import socket
import time


from constantsnutils.constants import ACTION, PRESENCE, TIME, USER,\
    ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from constantsnutils.utils import make_message, send_message


def client_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_answer(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('В диапазоне порта может быть число от 1024 до 65535.')
        sys.exit(1)


    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = client_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_answer(make_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Сообщение сервера не декодировать')


if __name__ == '__main__':
    main()
