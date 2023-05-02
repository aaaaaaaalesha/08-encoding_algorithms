import random
import socket

from contextlib import closing

import hamming

from src.utils import text_to_bits

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 12345
    s = socket.socket()
    s.connect((HOST, PORT))

    with closing(s) as sock:
        while True:
            input_string = input('Введите сообщение для отправки на сервер: ')
            data = text_to_bits(input_string)
            print(f'Сообщение в двоичном виде:\n{data}')

            answer = hamming.encode(data)
            print(f'Закодированное сообщение, готовое к отправке:\n{answer}')

            # С вероятностью, близкой к 0.5 вносим ошибку.
            if bool(random.getrandbits(1)):
                # Добавление случайной ошибки.
                bit_index = random.randint(0, len(answer) - 1)
                answer = (
                        answer[:bit_index]
                        + ('0' if answer[bit_index] == '1' else '1')
                        + answer[bit_index + 1:]
                )
                print(f'Внесена ошибка в {bit_index} бите:\n{answer}')

            sock.sendto(answer.encode(), (HOST, PORT))

            feedback = sock.recv(1024).decode()
            print(f'Ответ от сервера: {feedback}\n')
