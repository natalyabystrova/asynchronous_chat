import sys
import json
import socket
import time
import argparse
import logging
from logs import client_log_config
from constantsnutils import constants
from constantsnutils import utils
from errors import ReqFieldMissingError
from decos import log


LOGGER = logging.getLogger('client')

@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if constants.ACTION in message and message[constants.ACTION] == constants.MESSAGE and \
            constants.SENDER in message and constants.MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[constants.SENDER]}:\n{message[constants.MESSAGE_TEXT]}')
        LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[constants.SENDER]}:\n{message[constants.MESSAGE_TEXT]}')
    else:
        LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')

@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        constants.ACTION: constants.MESSAGE,
        constants.TIME: time.time(),
        constants.ACCOUNT_NAME: account_name,
        constants.MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def create_presence(account_name='Guest'):
    out = {
        constants.ACTION: constants.PRESENCE,
        constants.TIME: time.time(),
        constants.USER: {
            constants.ACCOUNT_NAME: account_name
        }
    }
    LOGGER.debug(f'Сформировано {constants.PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_ans(message):
    LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if constants.RESPONSE in message:
        if message[constants.RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[constants.ERROR]}'
    raise ReqFieldMissingError(constants.RESPONSE)


@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=constants.DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=constants.DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: '
                f'{server_address}, порт: {server_port}')
    # Инициализация сокета и обмен

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        utils.send_message(transport, message_to_server)
        answer = process_ans(utils.make_message(transport))
        LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
    except ConnectionRefusedError:
        LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                        f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
