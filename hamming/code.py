# code_word = input('Enter the code word: ')
# add user input for how many possible parity bits the user thinks a word should have
# from left to right, that's how the parity bits for this code is generated
# generate_hamming_code('10101001110')
# print(how_many_parity(11))

class HammingCode():
    def __init__(self, word, guess, is_even_parity=True):  # ask why I always need to define my inputs using self inside __init__
        self.word_len = len(word)
        self.original_word = word
        self.reverse_original_word = self.original_word[::-1]  # reverse word so that traversal can be easier
        self.guess = guess
        self.is_even_parity = is_even_parity  # i notied I dont need as much inputs to my fuction when using classes cause of globalness of variables
        self.num_of_parity_bits = None  # number of redundant/parity bits
        self.num_of_data_bits = None  # number of actual data bits
        self.original_parity_mapping = {}  # map parity positions to the bits in the word
        self.correct_parity_mapping = {}  # parity positions to the actual correct bits
        self.parity_check_pos = None
        self.correct_word = None

    def how_many_parity_bits(self):
        for p in range(self.guess):
            if pow(2, p) - p >= self.word_len + 1:
                self.num_of_parity_bits = p
                break
        else:
            self.num_of_parity_bits = -1 # is 0 a better choice 'cause it's falsy?
            raise ValueError(
                f"Could not determine the number of parity bits for a word length of {self.word_len}. "
                f"Try a higher guess than {self.guess}")

    def get_bit_to_check(self):
        all_positions = [bin(i + 1) for i in range(self.word_len)]
        parity_positions = [bin(p) for p in self.original_parity_mapping]
        positions = {int(p, 2): [] for p in parity_positions}
        for p_pos in parity_positions:
            binary_p_pos = p_pos.split('b')[1]
            for pos in all_positions:
                binary_pos = pos.split('b')[1]
                if int(binary_p_pos, 2) & int(binary_pos, 2) != 0:
                    positions[int(binary_p_pos, 2)].append(int(binary_pos, 2))
        self.parity_check_pos = positions

    def check_bits(self):
        for i in range(self.word_len):
            if is_pow_two(i):
                temp = []
                print(self.parity_check_pos[i])
                for check_position in self.parity_check_pos[i]:
                    temp.append(self.reverse_original_word[check_position - 1])
                    one_count = temp.count('1')
                    if self.is_even_parity:
                        if is_even(one_count):
                            self.correct_parity_mapping[i] = '0'
                        else: self.correct_parity_mapping[i] = '1'
                    else:  # for odd parity
                        if is_even(one_count):
                            self.correct_parity_mapping[i] = '1'
                        else: self.correct_parity_mapping[i] = '0'
        print(self.correct_parity_mapping)

    def fix_original_word(self):
        reverse_correct_word = list(self.reverse_original_word)  # copy the value of the reverse of the original word
        for pos, bit in self.correct_parity_mapping.items():
            reverse_correct_word[pos-1] = bit
        self.correct_word = ''.join(reverse_correct_word[::-1])
        print(self.correct_word)

    def generate_hamming_code(self):
        try:
            self.how_many_parity_bits()  # updates self.num_of_parity_bits
        except ValueError as e:
            print(e)
            return
        self.num_of_data_bits = self.num_of_parity_bits - self.word_len
        self.original_parity_mapping = {
            pow(2, i): self.reverse_original_word[(pow(2, i) - 1)] for i in range(self.num_of_parity_bits)
        }
        print(self.original_parity_mapping)
        self.get_bit_to_check()  # updates self.parity_check_pos
        print(self.parity_check_pos)


def is_pow_two(n: int):
    return n > 0 and (n & (n - 1)) == 0

def is_even(n):
    return n % 2 == 0

is_pow_two(48)

n = HammingCode('10101001110', guess=100)
n.generate_hamming_code()
n.check_bits()
n.fix_original_word()

