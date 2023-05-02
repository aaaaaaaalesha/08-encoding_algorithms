import binascii
import socket

import crc

from src.constants import ERR_MSG


def __int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return __int2bytes(n).decode(encoding, errors)


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Подключено:', addr)
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                print('Полученные данные:', data)
                decoded_data = crc.decode(data)

                if decoded_data != 'ERROR':
                    print(f'Получено сообщение: {text_from_bits(decoded_data)}')
                    conn.sendall('Сообщение успешно доставлено!'.encode())
                else:
                    print('При отправке произошла ошибка. Отправляю запрос на переотправку...')
                    conn.sendall(ERR_MSG.encode())
