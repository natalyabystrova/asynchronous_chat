import socket
import sys
import argparse
import json
import logging
from errors import IncorrectDataRecivedError
from constantsnutils import constants
from constantsnutils import utils
import logs.server_log_config
from decos import log


LOGGER = logging.getLogger('server')


@log
def process_client_message(message):
    LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if constants.ACTION in message and message[constants.ACTION] == constants.PRESENCE and constants.TIME in message and \
            constants.USER in message and message[constants.USER][constants.ACCOUNT_NAME] == 'Guest':
        return {constants.RESPONSE: 200}
    return {
        constants.RESPONSE: 400,
        constants.ERROR: 'Bad Request'
    }


@log
def create_arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=constants.DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    """Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию"""
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
                        f'Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, адрес,'
                f' с которого принимаются подключения: {listen_address}. '
                f'Если адрес не указан, принимаются соединения с любых адресов.')
    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(constants.MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_cient = utils.make_message(client)
            LOGGER.debug(f'Получено сообщение {message_from_cient}')
            print(message_from_cient)
            response = process_client_message(message_from_cient)
            LOGGER.info(f'Cформирован ответ клиенту {response}')
            utils.send_message(client, response)
            LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            LOGGER.error(f'Не удалось декодировать Json строку, '
                         f'полученную от клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                         f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()