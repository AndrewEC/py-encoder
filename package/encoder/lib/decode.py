from typing import Dict, Tuple

from .data import EncodingDefinitionTable, get_or_default_dictionary, get_or_default_padding
from .convert import binary_to_bytes


class _EncodedCharacterIterator:

    """
    Utility class that helps iterate over characters in an encoded string. The number of characters yielded
    per iteration is equal to the encoded_character_length constructor argument.

    This starts at the end of the string. Meaning the first iteration will yield n characters that appear at the end
    of the string in the order that they appear in the string. For example if encoded_character_length is 2
    the first iteration of 'hello_world!' would yield 'd!'.
    """

    def __init__(self, encoded_string: str, padding_character: str, encoded_character_length: int):
        self._encoded_string = encoded_string
        self._padding_character = padding_character
        self._encoded_character_length = encoded_character_length

    def _strip_padding_characters(self) -> Tuple[str, int]:
        encoded_string_cp = self._encoded_string[:]
        count = 0
        while encoded_string_cp.endswith(self._padding_character):
            count = count + 1
            encoded_string_cp = encoded_string_cp[:len(encoded_string_cp) - len(self._padding_character)]
        return encoded_string_cp, count

    def __iter__(self):
        encoded_less_padding, padding_character_count = self._strip_padding_characters()
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
        padding_character_count = (len(characters) - self._representation_value_length) * padding_multiplier
        binary_key = self._try_get_binary_key(characters[:self._representation_value_length])
        return binary_key[:len(binary_key) - padding_character_count]

    def decode(self, encoded_string: str) -> bytes:
        iterator = _EncodedCharacterIterator(encoded_string, self._padding_character, self._representation_value_length)
        binary_string = ''.join(reversed(list(map(self._get_binary_from_representation, iterator))))
        return binary_to_bytes(binary_string)

    def decode_string(self, encoded_string: str) -> str:
        return str(self.decode(encoded_string), 'utf-8')


def decode_to_string(encoded: str,
                     encoding_dictionary: Dict[str, str] | None = None,
                     padding_character: str | None = None) -> str:
    """
    Decodes the input value string using the encoding_dictionary and padding_character back to its original value.
    If no dictionary or padding character have been provided then this will fall back to the default base64 dictionary
    and padding character.

    :param encoded: The already encoded string to be decoded.
    :param encoding_dictionary: The dictionary containing the binary keys and encoded character representations.
    :param padding_character: The padding character.
    :return: The decoded, original, representation of the input encoded string.
    """

    return Decoder(
        get_or_default_dictionary(encoding_dictionary),
        get_or_default_padding(padding_character)
    ).decode_string(encoded)


def decode_to_bytes(encoded: str,
                    encoding_dictionary: Dict[str, str] | None = None,
                    padding_character: str | None = None) -> bytes:
    """
    Decodes the input value string using the encoding_dictionary and padding_character back to its original byte value.
    If no dictionary or padding character have been provided then this will fall back to the default base64 dictionary
    and padding character.

    :param encoded: The already encoded string to be decoded.
    :param encoding_dictionary: The dictionary containing the binary keys and encoded character representations.
    :param padding_character: The padding character.
    :return: The decoded, original, byte representation of the input encoded string.
    """

    return Decoder(
        get_or_default_dictionary(encoding_dictionary),
        get_or_default_padding(padding_character)
    ).decode(encoded)
