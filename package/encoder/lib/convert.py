from .pad_string import lpad_string
from .data import BinaryChunkIterator


_BINARY_CHUNK_LENGTH = 8
_PREFIX_END_POSITION = 2


def binary_to_bytes(binary_string: str) -> bytes:
    return bytes(int(chunk, 2) for chunk in BinaryChunkIterator(binary_string, _BINARY_CHUNK_LENGTH))


def strip_binary_prefix(value: str) -> str:
    return value[_PREFIX_END_POSITION:]


def _format_binary_string(value: str) -> str:
    return lpad_string(strip_binary_prefix(value), _BINARY_CHUNK_LENGTH, '0')


def bytes_to_binary(value: bytes) -> str:
    return ''.join([_format_binary_string(bin(char)) for char in value])


def string_to_binary(value: str) -> str:
    value_bytes = bytes(value, 'utf-8')
    return bytes_to_binary(value_bytes)
