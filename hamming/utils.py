def is_pow_two(n: int) -> bool:
    """Checks if an integer is a power of two"""
    return n > 0 and (n & (n - 1)) == 0

def is_even(n: int) -> bool:
    """Checks if an integer is even"""
    return n % 2 == 0

def flip(bit: str) -> str:
    """Flips a single bit"""
    bit = '0' if bit == '1' else '1'
    return bit

def is_binary(word: str) -> bool:
    for bit in word:
        try:
            if int(bit) not in [0, 1]: return False
        except ValueError: return False
    return True