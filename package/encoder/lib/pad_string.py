def _get_padding(value: str, target_length: int, padding_character: str) -> str:
    return padding_character * (target_length - len(value))


def lpad_string(value: str, target_length: int, padding_character: str) -> str:
    padding = _get_padding(value, target_length, padding_character)
    return f'{padding}{value}'


def rpad_string(value: str, target_length: int, padding_character: str) -> str:
    padding = _get_padding(value, target_length, padding_character)
    return f'{value}{padding}'
