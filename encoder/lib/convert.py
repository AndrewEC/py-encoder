from .pad_string import lpad_string
from .binary_chunk_iterator import BinaryChunkIterator


_BITS_IN_BYTE = 8
_PREFIX_END_INDEX = 2


def binary_to_bytes(binary_string: str) -> bytes:
    """
    Converts the binary string to bytes.

    :param binary_string: The binary string to convert to bytes.
    :return: A byte representation of the binary string.
    """

    return bytes(int(chunk, 2) for chunk in BinaryChunkIterator(binary_string, _BITS_IN_BYTE))


def strip_binary_prefix(value: str) -> str:
    """
    Strips the 0b prefix from a binary string. If the prefix does not exist on the string then the
    original input string will be returned without modification.

    :param value: The binary string containing the prefix to remove.
    :return: The binary string less the prefix or, if the binary string does not have the prefix in question,
        the original input string.
    """

    if '0b' not in value:
        return value
    return value[_PREFIX_END_INDEX:]


def _format_binary_string(value: str) -> str:
    return lpad_string(strip_binary_prefix(value), _BITS_IN_BYTE, '0')


def bytes_to_binary(value: bytes) -> str:
    """
    Converts bytes to a binary string.

    :param value: The bytes to be converted to binary.
    :return: A binary string representation of the bytes.
    """

    return ''.join(_format_binary_string(bin(single_byte)) for single_byte in value)


def string_to_binary(value: str) -> str:
    """
    Converts the input string to bytes then to a binary string representation of those bytes.

    :param value: The string to be converted to binary.
    :return: A binary representation of the input string.
    """

    value_bytes = bytes(value, 'utf-8')
    return bytes_to_binary(value_bytes)
