"""Haffman coding module."""


def encode(data: str) -> str:
    bits = [int(bit) for bit in data]
    # Рассчитываем число проверочных битов.
    r = 0
    while 2 ** r < len(bits) + r + 1:
        r += 1

    # Вставляем проверочные биты в массив.
    result = [0] * (len(bits) + r)
    j = 0
    for i in range(len(result)):
        if i + 1 == 2 ** j:
            j += 1
        else:
            result[i] = bits.pop(0)

    # Рассчитываем значения проверочных битов.
    for i in range(r):
        pos = 2 ** i - 1
        check = 0
        for j in range(pos, len(result), 2 * pos + 2):
            check ^= result[j:j + pos + 1].count(1) % 2
        result[pos] = check

    return ''.join([str(bit) for bit in result])


def decode(data: str) -> tuple[str, int | None]:
    bits = [int(bit) for bit in data]
    r = 0
    while 2 ** r < len(bits):
        r += 1

    error_pos = 1

    # Вычисляем позицию ошибки, складывая все контрольные биты.
    for i in range(r):
        pos = 2 ** i - 1
        check = 0
        for j in range(pos, len(bits), 2 * pos + 2):
            check ^= bits[j:j + pos + 1].count(1) % 2
        if check != 0:
            error_pos += pos

    # Исправляем ошибку.
    if error_pos > 1:
        bits[error_pos - 1] ^= 1

    # Отбрасываем контрольные биты.
    result = []
    j = 0
    for i in range(len(bits)):
        if i + 1 == 2 ** j:
            j += 1
        else:
            result.append(bits[i])

    # Возвращаем декодированные данные и позицию ошибки, если она была найдена.
    return (
        ''.join([str(bit) for bit in result]),
        error_pos - 1 if error_pos > 1 else None,
    )
