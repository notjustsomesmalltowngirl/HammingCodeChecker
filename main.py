from hamming.code import HammingCode
from hamming.utils import is_binary
def main():
    code_word = input('Enter the code code_word: ')
    if not is_binary(code_word):
        print('Enter a Valid Binary Number.')
        return
    try:
        guess = int(input('How many parity bits do you think this code contains? '))
        hamming_code = HammingCode(code_word, guess)
        hamming_code.combine_all_steps()
        hamming_code.display_results()
    except ValueError:
        print('Ensure guess is an Integer')


if __name__ == '__main__':
    main()
