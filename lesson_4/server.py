import socket
import sys
import argparse
import json
import logging
from errors import IncorrectDataRecivedError
from constantsnutils import constants
from constantsnutils import utils

SERVER_LOGGER = logging.getLogger('server')

def process_client_message(message):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if constants.ACTION in message and message[constants.ACTION] == constants.PRESENCE and constants.TIME in message and \
            constants.USER in message and message[constants.USER][constants.ACCOUNT_NAME] == 'Guest':
        return {constants.RESPONSE: 200}
    return {
        constants.RESPONSE: 400,
        constants.ERROR: 'Bad Request'
    }


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=constants.DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))


    transport.listen(constants.MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_cient = utils.make_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_cient}')
            response = process_client_message(message_from_cient)
            SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
            utils.send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
