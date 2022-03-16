from typing import Dict, Tuple

from .data import BASE_64_ENCODING_DICTIONARY, EncodingDefinitionTable, BASE_64_PADDING_CHARACTER
from .convert import binary_to_bytes


class _EncodedCharacterIterator:

    def __init__(self, encoded_string: str, padding_character: str, encoded_character_length: int):
        self._encoded_string = encoded_string
        self._padding_character = padding_character
        self._encoded_character_length = encoded_character_length

    def _strip_padding_characters(self, encoded_string: str, padding_character: str) -> Tuple[str, int]:
        encoded_string_cp = encoded_string[:]
        count = 0
        while encoded_string_cp.endswith(padding_character):
            count = count + 1
            encoded_string_cp = encoded_string_cp[:len(encoded_string_cp) - len(padding_character)]
        return encoded_string_cp, count

    def __iter__(self):
        encoded_less_padding, padding_character_count = self._strip_padding_characters(self._encoded_string, self._padding_character)
        position = len(encoded_less_padding)
        while True:
            if position <= 0:
                break
            characters = encoded_less_padding[position - self._encoded_character_length:position]
            position = position - len(characters)
            if position == len(encoded_less_padding) - 1:
                characters = characters + (self._padding_character * padding_character_count)
            yield characters


class Decoder(EncodingDefinitionTable):

    def __init__(self, encoding_dictionary: Dict[str, str], padding_character: str):
        super().__init__(encoding_dictionary, padding_character)

    def _try_get_binary_key(self, value: str) -> str:
        for key in self._encoding_dictionary:
            if self._encoding_dictionary[key] == value:
                return key
        raise Exception(f'Could not find a binary key in encoding dictionary that maps to representation: [{value}]')

    def _get_binary_from_representation(self, characters: str) -> str:
        padding_multiplier = 2 if self._even_key_length else 1
        padding_characters = (len(characters) - self._representation_value_length) * padding_multiplier
        binary_key = self._try_get_binary_key(characters[:self._representation_value_length])
        return binary_key[:len(binary_key) - padding_characters]

    def decode(self, encoded_string: str) -> bytes:
        iterator = _EncodedCharacterIterator(encoded_string, self._padding_character, self._representation_value_length)
        binary_string = ''.join(reversed(list(map(self._get_binary_from_representation, iterator))))
        return binary_to_bytes(binary_string)

    def decode_string(self, encoded_string: str) -> str:
        return str(self.decode(encoded_string), 'utf-8')


def decode_to_string(encoded: str,
                     encoding_dictionary: Dict[str, str] = BASE_64_ENCODING_DICTIONARY,
                     padding_character: str = BASE_64_PADDING_CHARACTER) -> str:
    return Decoder(encoding_dictionary, padding_character).decode_string(encoded)


def decode_to_bytes(encoded: str,
                    encoding_dictionary: Dict[str, str] = BASE_64_ENCODING_DICTIONARY,
                    padding_character: str = BASE_64_PADDING_CHARACTER) -> bytes:
    return Decoder(encoding_dictionary, padding_character).decode(encoded)
