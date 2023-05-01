import socket
import random


def crc_remainder(
        input_bitstring: str,
        initial_filler,
        gen_poly='1011',
):
    """
    Calculate the CRC remainder of a string of bits using a chosen polynomial.
    initial_filler should be '1' or '0'.
    """
    gen_poly = gen_poly.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = (len(gen_poly) - 1) * initial_filler
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(gen_poly)):
            input_padded_array[cur_shift + i] = str(int(gen_poly[i] != input_padded_array[cur_shift + i]))
    return ''.join(input_padded_array)[len_input:]


def crc_check(
        input_bitstring,
        check_value,
        gen_poly='1011',
):
    """
    Calculate the CRC check of a string of bits using a chosen polynomial.
    """
    gen_poly = gen_poly.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = check_value
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(gen_poly)):
            input_padded_array[cur_shift + i] = str(int(gen_poly[i] != input_padded_array[cur_shift + i]))
    return '1' not in ''.join(input_padded_array)[len_input:]


if __name__ == '__main__':
    crc_check('11010011101100', crc_remainder('11010011101100', '0'))


    # Создаем сокет и подключаемся к серверу
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(("localhost", 12345))
    #
    # # Бесконечный ввод сообщений
    # while True:
    #     # Запрашиваем ввод сообщения
    #     message = input("Введите сообщение: ")
    #     # Кодируем сообщение кодом CRC
    #     message_with_crc_bytes = crc_encode(message)
    #     # Отправляем сообщение на сервер
    #     client_socket.sendall(message_with_crc_bytes)
    #     # Получаем ответ от сервера
    #     response_with_crc_bytes = client_socket.recv(1024)
    #
    #     # Закрываем сокет
    # client_socket.close()
