from typing import Dict

from .base64_defaults import get_or_default_dictionary, get_or_default_padding
from .convert import binary_to_bytes
from .encoding_definition_table import EncodingDefinitionTable
from .encoded_string_spliterator import EncodedStringSpliterator


class Decoder(EncodingDefinitionTable):

    def __init__(self, encoding_dictionary: Dict[str, str], padding_character: str):
        super().__init__(encoding_dictionary, padding_character)

    def _get_binary_key(self, value: str) -> str:
        for key in self._encoding_dictionary:
            if self._encoding_dictionary[key] == value:
                return key
        raise Exception(f'Could not find a binary key in encoding dictionary that maps to representation: [{value}]')

    def _get_binary_from_representation(self, representation: str) -> str:
        padding_multiplier = 2 if self._even_key_length else 1
        padding_character_count = (len(representation) - self._representation_value_length) * padding_multiplier
        binary_key = self._get_binary_key(representation[:self._representation_value_length])
        return binary_key[:len(binary_key) - padding_character_count]

    def decode(self, encoded_string: str) -> bytes:
        splitter = EncodedStringSpliterator(encoded_string, self._padding_character, self._representation_value_length)
        binary_string = ''.join(reversed(list(map(self._get_binary_from_representation, splitter))))
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
