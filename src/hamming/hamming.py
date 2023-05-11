"""Haffman coding module."""

from src.utils import is_power_of_two


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

    error_pos = 0

    # Вычисляем позицию ошибки.
    check_bits = [2 ** i for i in range(r)]
    check_bits.reverse()
    for i, check_bit in enumerate(check_bits):
        check = 0
        for j in range(check_bit - 1, len(bits), check_bit * 2):
            check += sum(bits[j:j + check_bit])
        if check % 2 == 1:
            error_pos += check_bit

    # Исправляем ошибку.
    if error_pos > 0:
        bits[error_pos - 1] = 1 - bits[error_pos - 1]

    # Убираем биты проверки.
    decoded_data = ''.join(
        str(bit)
        for i, bit in enumerate(bits)
        if not is_power_of_two(i + 1)
    )

    return (
        decoded_data,
        error_pos - 1 if error_pos > 0 else None,
    )
