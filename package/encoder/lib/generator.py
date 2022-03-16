from typing import Dict, List
import string
from random import randrange

from .convert import strip_binary_prefix
from .pad_string import lpad_string


_EXCLUDE_CHARACTERS = '\\"`\''


def generate_encoding_dictionary(binary_key_length: int, representation_length: int, padding_character: str = '=') -> Dict[str, str]:
    _validate_values(binary_key_length, representation_length, padding_character)
    keys = _generate_keys(binary_key_length)
    representations = _generate_representations(len(keys), representation_length, padding_character)
    return {keys[i]: representations[i] for i in range(len(keys))}


def _validate_values(binary_key_length: int, representation_length: int, padding_character: str):
    if binary_key_length <= 0:
        raise ValueError('The length of the binary key must be a whole number with a value greater than 0.')
    if representation_length <= 0:
        raise ValueError('The length of the representation character(s) must be a whole number with a value greater '
                        'than 0.')
    if len(padding_character) == 0:
        raise ValueError('The padding character must consist of, at minimum, one character.')


def _generate_representations(number_of_characters: int, representation_length: int, padding_character: str) -> List[str]:
    character_options = string.ascii_uppercase + string.ascii_lowercase + string.punctuation
    for character in padding_character + _EXCLUDE_CHARACTERS:
        character_options = character_options.replace(character, '')
    representations = []
    for i in range(number_of_characters):
        encoding = _generate_representation(character_options, representation_length)
        while encoding in representations:
            encoding = _generate_representation(character_options, representation_length)
        representations.append(encoding)
    return representations


def _generate_representation(character_options: str, representation_length: int) -> str:
    option_count = len(character_options)
    return ''.join([character_options[randrange(option_count)] for _ in range(representation_length)])


def _generate_keys(binary_key_size: int) -> List[str]:
    maximum = int('1' * binary_key_size, 2)
    return [_generate_key(i, binary_key_size) for i in range(maximum + 1)]


def _generate_key(value: int, binary_key_size: int) -> str:
    key = strip_binary_prefix(bin(value))
    return lpad_string(key, binary_key_size, '0')
