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
