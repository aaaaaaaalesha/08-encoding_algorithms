import socket


# Функция для декодирования сообщения с кодом CRC
def crc_decode(message_with_crc_bytes):
    generator_polynomial = 0b1011
    # Разделяем сообщение и CRC
    message, crc = message_with_crc_bytes[:-1], int.from_bytes(message_with_crc_bytes[-1:], byteorder='big')
    # Проверяем CRC
    crc_check = 0
    for i in range(len(message)):
        if (crc_check >> 2) & 1:
            crc_check = ((crc_check << 1) & 0b111) ^ generator_polynomial
        else:
            crc_check = (crc_check << 1) & 0b111
        crc_check ^= int(message[i]) & 1
    # Если CRC корректный, возвращаем сообщение
    if crc_check == crc:
        return message.decode()
    else:
        return None


if __name__ == '__main__':
    # Создаем сокет и связываем его с адресом
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(1)

    # Бесконечный цикл ожидания подключений
    while True:
        # Принимаем подключение
        connection, address = server_socket.accept()
        print(f"Подключение от {address}")
        # Бесконечный цикл обработки сообщений

        # Получаем сообщение от клиента
        message_with_crc_bytes = connection.recv(1024)
        # Если сообщение пустое, значит клиент закрыл соединение
        if not message_with_crc_bytes:
            break
        # Декодируем сообщение и проверяем его CRC
        message = crc_decode(message_with_crc_bytes)
        if message is not None:
            print(f"Получено сообщение: {message}")
            # # Отправляем ответ клиенту
            # response = f"Сообщение '{message}' получено"
            # # response_with_crc_bytes = crc_encode(response.encode())
            # connection.sendall(response_with_crc_bytes)
        else:
            print(f"Ошибка при передаче сообщения от {address}")

    # Закрываем соединение
    connection.close()

    # Закрываем сокет
    server_socket.close()
