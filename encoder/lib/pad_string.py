def _get_padding(value: str, target_length: int, padding_character: str) -> str:
    if len(value) >= target_length:
        return ''
    return padding_character * (target_length - len(value))


def lpad_string(value: str, target_length: int, padding_character: str) -> str:
    """
    Prepends the padding_character to the value string until the length of the value string is equal to the
    target_length and then returns the result. This will effectively return a copy of the input value string
    if the length of value is greater than, or equal to, target_length.

    :param value: The string to be padded.
    :param target_length: The desired length of the output string.
    :param padding_character: The character to be prepended as padding.
    :return: A new string whose length is minimally equal to the length of specified by the target_length. If the
        length of the input value string is already greater or equal to target_length then a copy of value will
        be returned.
    """

    padding = _get_padding(value, target_length, padding_character)
    return f'{padding}{value}'


def rpad_string(value: str, target_length: int, padding_character: str) -> str:
    """
    Appends the padding_character to the value string until the length of the value string is equal to the
    target_length and then returns the result. This will effectively return a copy of the input value string
    if the length of value is greater than, or equal to, target_length.

    :param value: The string to be padded.
    :param target_length: The desired length of the output string.
    :param padding_character: The character to be appended as padding.
    :return: A new string whose length is minimally equal to the length of specified by the target_length. If the
        length of the input value string is already greater or equal to target_length then a copy of value will
        be returned.
    """

    padding = _get_padding(value, target_length, padding_character)
    return f'{value}{padding}'
