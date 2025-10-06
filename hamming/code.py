# code_word = input('Enter the code word: ')
# add user input for how many possible parity bits the user thinks a word should have
# from left to right, that's how the parity bits for this code is generated
# generate_hamming_code('10101001110')
# print(how_many_parity(11))

class HammingCode():
    def __init__(self, word, guess, is_even_parity=True):  # ask why I always need to define my inputs using self inside __init__
        self.word_len = len(word)
        self.word = word
        self.guess = guess
        self.is_even_parity = is_even_parity  # i notied I dont need as much inputs to my fuction when using classes cause of globalness of variables
        self.num_of_parity_bits = None
        self.num_of_data_bits = None
        self.parity_bits_mappings = None
        self.parity_check_pos = None

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
        parity_positions = [bin(p) for p in self.parity_bits_mappings]
        positions = {int(p, 2): [] for p in parity_positions}
        for p_pos in parity_positions:
            binary_p_pos = p_pos.split('b')[1]
            for pos in all_positions:
                binary_pos = pos.split('b')[1]
                if int(binary_p_pos, 2) & int(binary_pos, 2) != 0:
                    positions[int(binary_p_pos, 2)].append(int(binary_pos, 2))
        self.parity_check_pos = positions

    def check_bits(self):
        if self.is_even_parity:
            ...
    def generate_hamming_code(self):
        self.how_many_parity_bits()  # updates self.num_of_parity_bits
        self.num_of_data_bits = self.num_of_parity_bits - self.word_len
        self.parity_bits_mappings = {
            pow(2, i): self.word[(pow(2, i) - 1)] for i in range(self.num_of_parity_bits)
        }
        # print(self.parity_bits_mappings)
        self.get_bit_to_check()  # updates self.parity_check_pos
        print(self.parity_check_pos)




n = HammingCode('10101001110', guess=100)

n.generate_hamming_code()