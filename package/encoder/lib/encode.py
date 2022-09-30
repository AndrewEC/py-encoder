from typing import Dict

from .convert import string_to_binary, bytes_to_binary
from .pad_string import rpad_string
from .data import EncodingDefinitionTable, BinaryChunkIterator, get_or_default_padding,\
    get_or_default_dictionary


class Encoder(EncodingDefinitionTable):

    def __init__(self, encoding_dictionary: Dict[str, str], padding_character: str):
        super().__init__(encoding_dictionary, padding_character)

    def _try_get_representation(self, binary_key: str) -> str:
        if binary_key not in self._encoding_dictionary:
            raise Exception(f'Provided encoding dictionary has no binary key matching: [{binary_key}]')
        return self._encoding_dictionary[binary_key]

    def _get_encoded_representation(self, binary_chunk: str) -> str:
        binary_chunk_length = len(binary_chunk)

        if binary_chunk_length == self._binary_key_length:
            return self._try_get_representation(binary_chunk)

        padded_binary_string = rpad_string(binary_chunk, self._binary_key_length, '0')
        unpadded_representation = self._try_get_representation(padded_binary_string)

        padding_length_div = 2 if self._even_key_length else 1
        padding_length = int((self._binary_key_length - binary_chunk_length) / padding_length_div)
        padding = self._padding_character * padding_length
        return f'{unpadded_representation}{padding}'

    def encode(self, binary_string: str) -> str:
        iterator = BinaryChunkIterator(binary_string, self._binary_key_length)
        return ''.join(map(self._get_encoded_representation, iterator))

    def encode_string(self, string_to_encode: str) -> str:
        return self.encode(string_to_binary(string_to_encode))

    def encode_bytes(self, bytes_to_encode: bytes) -> str:
        return self.encode(bytes_to_binary(bytes_to_encode))


def encode_string(value: str,
                  encoding_dictionary: Dict[str, str] | None = None,
                  padding_character: str | None = None) -> str:
    """
    Encodes the input value string using the encoding_dictionary and padding_character. If no dictionary or padding
    character have been provided then this will fall back to the default base64 dictionary and padding character.

    :param value: The input string to be encoded.
    :param encoding_dictionary: The dictionary containing the binary keys and encoded character representations.
    :param padding_character: The padding character.
    :return: An encoded string representation of the original value string.
    """

    return Encoder(
        get_or_default_dictionary(encoding_dictionary),
        get_or_default_padding(padding_character)
    ).encode_string(value)


def encode_bytes(value: bytes,
                 encoding_dictionary: Dict[str, str] | None = None,
                 padding_character: str | None = None) -> str:
    """
    Encodes a series of bytes into an encoded string representation using the encoding_dictionary and padding_character.
    If no dictionary or padding character have been provided then this will fall back to the default base64 dictionary
    and padding character.

    :param value: The bytes to be encoded to a string.
    :param encoding_dictionary: The dictionary containing the binary keys and encoded character representations.
    :param padding_character: The padding character.
    :return: An encoded string representation of the original bytes.
    """

    return Encoder(
        get_or_default_dictionary(encoding_dictionary),
        get_or_default_padding(padding_character)
    ).encode_bytes(value)
