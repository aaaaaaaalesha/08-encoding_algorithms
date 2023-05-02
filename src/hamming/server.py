import socket

import hamming

from src.utils import text_from_bits

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

                print(f'Полученные данные:\n{data}')
                decoded_data, err_pos = hamming.decode(data)

                if err_pos is not None:
                    print(f'Исправлена ошибка в {err_pos} бите:\n{decoded_data}')

                print(f'Получено сообщение: {text_from_bits(decoded_data)}')
                conn.sendall('Сообщение успешно доставлено!\n'.encode())
