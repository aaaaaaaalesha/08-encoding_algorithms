"""CRC coding module."""

# x^3 + x + 1
GEN_POLY = '1011'


def encode(data: str, gen_poly=GEN_POLY):
    remainder = __div(
        # Appends n - 1 zeroes at end of data.
        data + '0' * (len(gen_poly) - 1),
        gen_poly,
    )

    # Append remainder in the original data.
    codeword = data + remainder
    return codeword


def decode(data: str, gen_poly=GEN_POLY) -> str:
    remainder = __div(data, gen_poly)

    # If remainder is all zeroes (no error), return message without error bits.
    if remainder == '0' * (len(gen_poly) - 1):
        return data[:-len(gen_poly) + 1]

    # Otherwise, return 'ERROR' to indicate that an error was detected.
    return 'ERROR'


def __xor(a: str, b: str) -> str:
    return ''.join([
        '0' if a[i] == b[i] else '1'
        for i in range(1, len(b))
    ])


def __div(divisible: str, divisor: str) -> str:
    """Performs modulo-2 division."""
    # Number of bits to be XORed at a time.
    pick = len(divisor)

    # Slicing the dividend to appropriate length for particular step.
    tmp = divisible[:pick]

    while pick < len(divisible):
        if tmp[0] == '1':
            # Replace the dividend by the result of XOR and pull 1 bit down.
            tmp = __xor(divisor, tmp) + divisible[pick]

        else:  # If leftmost bit is '0'
            # If the leftmost bit of the dividend (or the part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an all-0s divisor.
            tmp = __xor('0' * pick, tmp) + divisible[pick]

        # increment pick to move further
        pick += 1

    # For the last n bits, we have to carry it out normally as increased value of pick will cause
    # Index Out of Bounds.
    if tmp[0] == '1':
        tmp = __xor(divisor, tmp)
    else:
        tmp = __xor('0' * pick, tmp)

    checkword = tmp
    return checkword
