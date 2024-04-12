from typing import Dict, List
import string
from random import randrange
import math

from .convert import strip_binary_prefix
from .pad_string import lpad_string


_EXCLUDE_CHARACTERS = '\\"`\''


class EncodingDictionary:

    def __init__(self, padding_character: str, mappings: Dict[str, str]):
        self.padding_character = padding_character
        self.mappings = mappings

    def __iter__(self):
        yield 'padding', self.padding_character
        yield 'mappings', self.mappings


def generate_encoding_dictionary(binary_key_length: int, representation_length: int, padding_character: str = '=') -> EncodingDictionary:
    """
    Generates a pseudo-random character encoding dictionary that can be used to with the encoder and decoder provided
    in this package.

    :param binary_key_length: The length of the binary string to be mapped to an encoded character representation.
    :param representation_length: The number of characters to be used as an encoded representation of the binary value.
    :param padding_character: The character to be used as padding.
    :return: An encoding dictionary containing the padding character and a nested dictionary of binary keys
        and the encoded characters they map to.
    """

    _validate_values(binary_key_length, representation_length, padding_character)
    keys = _generate_keys(binary_key_length)
    representations = _generate_representations(len(keys), representation_length, padding_character)
    mappings = {keys[i]: representations[i] for i in range(len(keys))}
    return EncodingDictionary(padding_character, mappings)


def _validate_values(binary_key_length: int, representation_length: int, padding_character: str):
    if binary_key_length <= 0:
        raise ValueError('The length of the binary key must be a whole number with a value greater than 0.')
    if representation_length <= 0:
        raise ValueError('The length of the representation character(s) must be a whole number with a value greater '
                         'than 0.')
    if len(padding_character) != 1:
        raise ValueError('The padding character must be a single character.')

    unique_character_count = len(_get_available_characters(padding_character))
    unique_combinations = math.pow(unique_character_count, representation_length)
    max_decimal_value = _max_decimal_value_for_bit_count(binary_key_length)
    if max_decimal_value >= unique_combinations:
        raise ValueError(f'A representation length of [{representation_length}] allows for [{unique_combinations}] unique combinations to represent a binary value. '
                         f'However the a binary key length of [{binary_key_length}] requires [{max_decimal_value}] unique combinations to be available.')


def _generate_representations(number_of_characters: int, representation_length: int, padding_character: str) -> List[str]:
    character_options = _get_available_characters(padding_character)
    representations = []
    for i in range(number_of_characters):
        encoding = _generate_representation(character_options, representation_length)
        while encoding in representations:  # pragma: no mutate
            encoding = _generate_representation(character_options, representation_length)
        representations.append(encoding)
    return representations


def _generate_representation(character_options: str, representation_length: int) -> str:
    return ''.join(character_options[randrange(len(character_options))] for _ in range(representation_length))


def _generate_keys(binary_key_size: int) -> List[str]:
    return [_generate_key(i, binary_key_size) for i in range(_max_decimal_value_for_bit_count(binary_key_size) + 1)]


def _max_decimal_value_for_bit_count(bit_count: int) -> int:
    return int('1' * bit_count, 2)


def _generate_key(value: int, binary_key_size: int) -> str:
    key = strip_binary_prefix(bin(value))
    return lpad_string(key, binary_key_size, '0')


def _get_available_characters(padding_character: str) -> str:
    characters = string.ascii_uppercase + string.ascii_lowercase + string.punctuation
    for character in padding_character + _EXCLUDE_CHARACTERS:
        characters = characters.replace(character, '')
    return characters
