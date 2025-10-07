import pytest
from hamming.code import HammingCode

def test_get_parity_bit_count_sets_num_parity_bits():
    h = HammingCode('1101101010', 6)
    h.get_parity_bit_count()
    assert h.num_of_parity_bits == 4

def test_map_original_parity_bits(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'num_of_parity_bits', 4)
    h.map_original_parity_bits()
    assert h.original_parity_mapping == {1: '0', 2: '1', 4: '1', 8: '0'}

def test_get_parity_bit_count_raises_valueerror():
    h = HammingCode('1101101010', 2)
    with pytest.raises(ValueError):
        h.get_parity_bit_count()

def test_map_parity_coverage(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'original_parity_mapping', {1: '1', 2: '1', 4: '0', 8: '0'})
    h.map_parity_coverage()
    assert h.parity_coverage_mapping == {1: [1, 3, 5, 7, 9],
                      2: [2, 3, 6, 7, 10], 4: [4, 5, 6, 7],
                      8: [8, 9, 10]}


def test_calculate_parity_bits(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'parity_coverage_mapping', {1: [1, 3, 5, 7, 9],
                      2: [2, 3, 6, 7, 10], 4: [4, 5, 6, 7],
                      8: [8, 9, 10]})
    h.calculate_parity_bits()
    assert h.correct_parity_mapping == {1: '0', 2: '1', 4: '0', 8: '0'}

def test_calculate_syndrome(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'original_parity_mapping', {1: '0', 2: '1', 4: '1', 8: '0'})
    mocker.patch.object(h, 'correct_parity_mapping', {1: '0', 2: '1', 4: '0', 8: '0'})
    h.calculate_syndrome()
    assert h.syndrome == 4

def test_correct_wrong_bit_for_syndrome_greaterthanone(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'syndrome', 4)
    h.correct_wrong_bit()
    assert h.correct_codeword == '1101100010'

def test_correct_wrong_bit_for_syndrome_equaltozero(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'syndrome', 0)
    h.correct_wrong_bit()
    assert h.correct_codeword == h.original_codeword

def test_correct_wrong_bit_for_syndrome_greaterthancodewordlen(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'syndrome', 13)
    h.correct_wrong_bit()
    assert h.correct_codeword == None

def test_extract_correct_databits_with_incorrect_hammingcode(mocker):
    h = HammingCode('1101101010', 6)
    mocker.patch.object(h, 'correct_codeword', '1101100010')
    mocker.patch.object(h, 'parity_coverage_mapping', {1: '...', 2: '...', 4: '...', 8: '...'})
    h.extract_correct_databits()
    assert h.correct_dataword == '111100'

def test_extract_correct_databits_with_correct_hammingcode(mocker):
    h = HammingCode('1101100010', 6)
    mocker.patch.object(h, 'correct_codeword', h.original_codeword)
    mocker.patch.object(h, 'parity_coverage_mapping',  {1: '...', 2: '...', 4: '...', 8: '...'})
    h.extract_correct_databits()
    assert h.correct_dataword == '111100'

def test_extract_correct_databits_with_undetectable_error(mocker):
    h = HammingCode('1101100010', 6)
    mocker.patch.object(h, 'correct_codeword', None)
    h.extract_correct_databits()
    assert h.correct_dataword == None