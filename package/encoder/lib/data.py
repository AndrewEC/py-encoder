from typing import Dict

_BASE_64_PADDING_CHARACTER = '='
_BASE_64_ENCODING_DICTIONARY: Dict[str, str] = {
    '000000': 'A',
    '000001': 'B',
    '000010': 'C',
    '000011': 'D',
    '000100': 'E',
    '000101': 'F',
    '000110': 'G',
    '000111': 'H',
    '001000': 'I',
    '001001': 'J',
    '001010': 'K',
    '001011': 'L',
    '001100': 'M',
    '001101': 'N',
    '001110': 'O',
    '001111': 'P',
    '010000': 'Q',
    '010001': 'R',
    '010010': 'S',
    '010011': 'T',
    '010100': 'U',
    '010101': 'V',
    '010110': 'W',
    '010111': 'X',
    '011000': 'Y',
    '011001': 'Z',
    '011010': 'a',
    '011011': 'b',
    '011100': 'c',
    '011101': 'd',
    '011110': 'e',
    '011111': 'f',
    '100000': 'g',
    '100001': 'h',
    '100010': 'i',
    '100011': 'j',
    '100100': 'k',
    '100101': 'l',
    '100110': 'm',
    '100111': 'n',
    '101000': 'o',
    '101001': 'p',
    '101010': 'q',
    '101011': 'r',
    '101100': 's',
    '101101': 't',
    '101110': 'u',
    '101111': 'v',
    '110000': 'w',
    '110001': 'x',
    '110010': 'y',
    '110011': 'z',
    '110100': '0',
    '110101': '1',
    '110110': '2',
    '110111': '3',
    '111000': '4',
    '111001': '5',
    '111010': '6',
    '111011': '7',
    '111100': '8',
    '111101': '9',
    '111110': '+',
    '111111': '/',
}


def get_or_default_padding(padding_character: str | None) -> str:
    return padding_character if padding_character is not None else _BASE_64_PADDING_CHARACTER


def get_or_default_dictionary(encoding_dictionary: Dict[str, str] | None) -> Dict[str, str]:
    return encoding_dictionary if encoding_dictionary is not None else _BASE_64_ENCODING_DICTIONARY.copy()


class BinaryChunkIterator:

    """
    Utility class to assist in iterating over a binary string for n number of characters per iteration. The number
    of characters iterated over per iteration is defined by the chunk_size constructor argument.

    For example if the chunk size is 8 each iteration will yield a binary string containing 8 characters or 8 bits or
    1 byte.
    """

    def __init__(self, value: str, chunk_size: int):
        self._value = value
        self._chunk_size = chunk_size
        self._value_length = len(value)

    def _next_chunk_size(self, current_position: int):
        remaining = self._value_length - current_position
        return min(remaining, self._chunk_size)

    def __iter__(self):
        position = 0
        while True:
            chunk_size = self._next_chunk_size(position)
            if chunk_size == 0:
                break
            yield self._value[position:position + chunk_size]
            position = position + chunk_size


class EncodingDefinitionTable:

    """
    Contains basic logic to validate the encoding dictionary and padding characters.

    This class will validate the encoding dictionary to ensure the following rules are met will ensure the following:
    - All binary keys are of the same length
    - Each binary key is made up of the characters: 0 and 1
    - All character representations are of the same length
    - The padding character doesn't improperly overlap with a trailing character one of the character representations
    """

    def __init__(self, encoding_dictionary: Dict[str, str], padding_character: str):
        if len(encoding_dictionary) == 0:
            raise ValueError('The provided encoding dictionary must contain at least one entry.')
        self._encoding_dictionary = encoding_dictionary.copy()
        self._padding_character = padding_character
        self._binary_key_length = len(next(_ for _ in encoding_dictionary.keys()))
        self._representation_value_length = len(next(_ for _ in encoding_dictionary.values()))
        self._even_key_length = self._binary_key_length % 2 == 0
        self._validate_dictionary_keys()
        self._validate_dictionary_values()
        self._validate_padding_character()

    def _validate_dictionary_keys(self):
        if self._binary_key_length <= 0:
            raise ValueError(f'The length of the binary key needs to be greater than 0.')
        for binary_key, representation in self._encoding_dictionary.items():
            if len(binary_key) != self._binary_key_length:
                raise ValueError(
                    f'Binary key [{binary_key}] for representation [{representation}] does not match length of first '
                    f'binary key of [{self._binary_key_length}]')
            if len(binary_key.replace('0', '').replace('1', '')) != 0:
                raise ValueError(
                    f'Binary key [{binary_key} for representation[{representation}] is invalid. The binary key can '
                    'only contain the characters 0 and 1.')

    def _validate_dictionary_values(self):
        if self._representation_value_length <= 0:
            raise ValueError(f'The length of the encoded character representation needs to be greater than 0.')
        for binary_key, representation in self._encoding_dictionary.items():
            if len(representation) != self._representation_value_length:
                raise ValueError(
                    f'Representation [{representation}] for binary key [{binary_key}] does not match length of first '
                    f'representation of [{self._representation_value_length}]')

    def _validate_padding_character(self):
        for key, value in self._encoding_dictionary.items():
            if value.endswith(self._padding_character):
                raise ValueError(f'The character [{self._padding_character}] cannot be used for padding as it matches '
                                 f'the trailing characters for the character representation [{value}] associated with '
                                 f'binary key [{key}]')
