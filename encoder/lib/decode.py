from typing import Dict

from .data import EncodingDefinitionTable, get_or_default_dictionary, get_or_default_padding
from .convert import binary_to_bytes


class _EncodedStringSplitter:

    """
    Utility class that helps iterate over characters in an encoded string. The number of characters yielded
    per iteration is equal to the representation_value_length constructor argument.

    This starts at the end of the string. Meaning the first iteration will yield n characters that appear at the end
    of the string in the order that they appear in the string. For example if representation_value_length is 2
    the first iteration of 'hello_world!' would yield 'd!'.

    The first iteration is also a special exception in that it can yield more characters than the length specified
    by representation_value_length as the first iteration will also yield all the padding characters if there are
    any.
    """

    def __init__(self, encoded_string: str, padding_character: str, representation_value_length: int):
        self._encoded_string = encoded_string
        self._padding_character = padding_character
        self._representation_value_length = representation_value_length
        self._encoded_string_length = len(encoded_string)

    def __iter__(self):
        current_position = self._encoded_string_length
        while current_position > 0:
            representation = self._next_representation(current_position)
            yield representation
            current_position = current_position - len(representation)

    def _next_representation(self, current_position: int) -> str:
        padding = self._get_padding_characters(current_position)
        padding_length = len(padding)
        start_position = current_position - self._representation_value_length - padding_length
        return self._encoded_string[start_position:current_position]

    def _get_padding_characters(self, current_position: int) -> str:
        next_position = current_position
        padding_characters = ''
        while True:  # pragma: no mutate
            if not self._is_character_at_position_padding(next_position - 1):
                break
            padding_characters = padding_characters + self._padding_character
            next_position = next_position - 1
        return padding_characters

    def _is_character_at_position_padding(self, position: int) -> bool:
        return self._encoded_string[position] == self._padding_character


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
        splitter = _EncodedStringSplitter(encoded_string, self._padding_character, self._representation_value_length)
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
