from hamming.utils import is_even, is_pow_two, flip


class HammingCode():
    def __init__(self, codeword: str, guess: int,
                 is_even_parity: bool = True) -> None:
        """
            Initialize a HammingCode instance with the given codeword and user-supplied guess.
                Parameters
                ----------
                codeword : str
                    The received Hamming codeword (including data and parity bits).
                guess : int
                    A user-supplied upper bound for the number of parity bits.
                is_even_parity : bool, optional
                    Whether the code uses even parity (default is True).
                """
        self.codeword_len = len(codeword)
        self.original_codeword = codeword
        self.reverse_original_codeword = self.original_codeword[::-1]  # reverse codeword so that traversal can be easier
        self.guess = guess
        self.is_even_parity = is_even_parity  # i notied I dont need as much inputs to my fuction when using classes cause of globalness of variables
        self.num_of_parity_bits = None  # number of redundant/parity bits
        self.original_parity_mapping = {}  # map parity positions to the bits in the codeword
        self.correct_parity_mapping = {}  # parity positions to the actual correct bits
        self.parity_coverage_mapping = None
        self.correct_codeword = None
        self.syndrome = 0  # stores the position of error if any
        self.correct_dataword = None

    def get_parity_bit_count(self):
        """
                Determine and store the number of parity bits in the codeword.

                Uses the user's guess to iteratively solve the Hamming equation:
                2^p - p >= n + 1, where p is parity bits and n is total codeword length.

                Raises
                ------
                ValueError
                    If the number of parity bits cannot be determined within the guess.
            """
        for p in range(1,
                       self.guess + 1):  # so it works when the user guesses the exact number and wont start from 0 which is a meaningless number in this case
            if pow(2, p) >= self.codeword_len + 1:
                self.num_of_parity_bits = p
                break
        else:
            self.num_of_parity_bits = -1  # is 0 a better choice 'cause it's falsy?
            raise ValueError(
                f"Could not determine the number of parity bits for a code word length of {self.codeword_len}. "
                f"Try a higher guess than {self.guess}")

    def map_original_parity_bits(self):
        """Map parity bit positions to their current values in the codeword."""
        self.original_parity_mapping = {
            pow(2, i): self.reverse_original_codeword[pow(2, i) - 1]
            for i in range(self.num_of_parity_bits)
        }  # maps parity bits to their positions as they are in the inputted code word

    def map_parity_coverage(self):
        """
        Map each parity bit position to the list of bit positions it covers.
        Uses binary position masks to determine which bits are checked by each parity bit.
        Updates `self.parity_coverage_mapping`.
        """
        all_positions = [bin(i + 1) for i in range(self.codeword_len)]
        bin_parity_positions = [bin(p) for p in self.original_parity_mapping]
        positions = {int(p, 2): [] for p in bin_parity_positions}
        for p_pos in bin_parity_positions:
            binary_p_pos = p_pos.split('b')[1]  # convert parity position to binary
            for pos in all_positions:
                binary_pos = pos.split('b')[1]  # converts each position to binary
                if int(binary_p_pos, 2) & int(binary_pos, 2) != 0:  # uses bitwise AND to check if a parity checks it
                    positions[int(binary_p_pos, 2)].append(int(binary_pos, 2))
        self.parity_coverage_mapping = positions

    def calculate_parity_bits(self):
        """
                Calculate and return the correct parity bits based on coverage positions.

                For each parity bit, counts the number of '1's in its coverage range and
                determines what the correct parity value should be under the selected parity scheme.
                """
        for i in range(self.codeword_len):
            if is_pow_two(i):
                temp = []
                for check_position in self.parity_coverage_mapping[i]:
                    temp.append(self.reverse_original_codeword[check_position - 1])
                one_count = temp[1:].count('1')  # do not add the parity position
                if self.is_even_parity:
                    self.correct_parity_mapping[i] = '0' if is_even(one_count) else '1'
                else:  # for odd parity
                    self.correct_parity_mapping[i] = '1' if is_even(one_count) else '0'

    def calculate_syndrome(self):
        """
               Compute and return the syndrome, indicating the error bit position if any.

               Compares the original parity bits with the calculated correct ones and uses XOR
               to locate the position of a single-bit error. A syndrome of 0 indicates no detected error.
               """
        error_positions = []
        for (key1, value1), (key2, value2) in zip(self.original_parity_mapping.items(),
                                                  self.correct_parity_mapping.items()):
            # compare the correct parity mapping to the original in the codeword
            if value1 != value2:
                error_positions.append(key1)
        if error_positions:
            for position in error_positions:
                self.syndrome ^= position  # using XOR to detect error position in code word
        else:
            self.syndrome = 0

    def correct_wrong_bit(self):
        """
                Correct a single-bit error in the codeword based on the syndrome.

                Flips the erroneous bit (if any) and updates `self.correct_codeword`.
                Returns the corrected codeword string.
                """
        if self.syndrome != 0 and self.syndrome < self.codeword_len:
            original_codeword_list = list(self.reverse_original_codeword)
            original_codeword_list[self.syndrome - 1] = flip(original_codeword_list[self.syndrome - 1])
            self.correct_codeword = ''.join(original_codeword_list[::-1])
            return
        elif self.syndrome > self.codeword_len:
            return
        elif self.syndrome == 0:
            self.correct_codeword = self.original_codeword
            return

    def extract_correct_databits(self):
        """
                Extract and return the original data bits from the corrected codeword.

                Removes parity bit positions and reverses the bit order to reconstruct the dataword.
                Updates `self.correct_dataword`.
                """
        if self.correct_codeword:
            parity_positions = [k - 1 for k in self.parity_coverage_mapping.keys()]
            rev_correct_codeword = self.correct_codeword[::-1]
            # extract all the data bits in reverse
            data_bits = [rev_correct_codeword[i] for i in range(self.codeword_len) if i not in parity_positions]

            self.correct_dataword = ''.join(data_bits[::-1])

    def combine_all_steps(self):
        """
        Run the full error detection and correction pipeline.
                This method executes all steps in sequence:
                1. Determine parity bit count.
                2. Map parity coverage.
                3. Calculate correct parity bits.
                4. Compute the syndrome.
                5. Correct the erroneous bit (if any).
                6. Extract the data bits.
        """
        try:
            self.get_parity_bit_count()  # updates self.num_of_parity_bits
        except ValueError as e:
            print(e)
            return  # halt program
        self.map_original_parity_bits()  # map parity positions to their bits as it is in the code word the user entered
        self.map_parity_coverage()  # updates self.parity_check_pos
        self.calculate_parity_bits()  # updates correct_parity_mapping dict with the right parity bits
        self.calculate_syndrome()  # find the erroneous bit position by comparing the original parity mapping and
        self.correct_wrong_bit()
        self.extract_correct_databits()

    def display_results(self):
        """
        Print a summary of the error detection and correction process.

        Displays the original codeword, error location (if any), corrected codeword,
        and recovered data bits.
        Includes a playful message for the no-error case.
        """
        print("\n=== Hamming Code Check Summary ===")
        print(f"Original codeword:  {self.original_codeword}")

        if self.syndrome == 0:
            print("No single bit error detected, might be a double or quintuple bit error but lets not jinx it 😉")
        else:
            print(f"Detected error at position: {self.syndrome}")
            if self.correct_codeword:
                print(f"Corrected codeword: {self.correct_codeword}")

        if self.correct_dataword:
            print(f"Recovered data:    {self.correct_dataword}")
        print("==================================\n")

