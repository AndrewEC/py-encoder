class EncodedStringSpliterator:

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
        while True:
            if not self._is_character_at_position_padding(next_position - 1):
                break
            padding_characters = padding_characters + self._padding_character
            next_position = next_position - 1
        return padding_characters

    def _is_character_at_position_padding(self, position: int) -> bool:
        return self._encoded_string[position] == self._padding_character
