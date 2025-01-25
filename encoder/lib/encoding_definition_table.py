from typing import Dict


class EncodingDefinitionTable:

    """
    Contains basic logic to validate the encoding dictionary and padding characters.

    This class will validate the encoding dictionary to ensure the following rules are met will ensure the following:
    - All binary keys are of the same length
    - Each binary key is made up of the characters: 0 and 1
    - All character representations are of the same length
    - The padding character doesn't improperly overlap with a trailing character one of the character representations
    """

    def __init__(self, encoding_dictionary: Dict[str, str], padding_character: str):
        if len(encoding_dictionary) == 0:
            raise ValueError('The provided encoding dictionary must contain at least one entry.')

        self._encoding_dictionary = encoding_dictionary.copy()
        self._padding_character = padding_character
        self._binary_key_length = len(next(_ for _ in encoding_dictionary.keys()))
        self._representation_value_length = len(next(_ for _ in encoding_dictionary.values()))
        self._even_key_length = self._binary_key_length % 2 == 0
        self._validate_dictionary_keys()
        self._validate_dictionary_values()
        self._validate_padding_character()

    def _validate_dictionary_keys(self):
        if self._binary_key_length <= 0:
            raise ValueError('The length of the binary key needs to be greater than 0.')

        for binary_key, representation in self._encoding_dictionary.items():

            if len(binary_key) != self._binary_key_length:
                raise ValueError(
                    f'Binary key [{binary_key}] for representation [{representation}] does not match length of first '
                    f'binary key of [{self._binary_key_length}]')

            if self._does_binary_contain_illegal_character(binary_key):
                raise ValueError(
                    f'Binary key [{binary_key} for representation[{representation}] is invalid. The binary key can '
                    'only contain the characters 0 and 1.')

    def _does_binary_contain_illegal_character(self, binary: str) -> bool:
        illegal_characters = binary.replace('0', '').replace('1', '')
        return len(illegal_characters) > 0

    def _validate_dictionary_values(self):
        if self._representation_value_length <= 0:
            raise ValueError('The length of the encoded character representation needs to be greater than 0.')

        for binary_key, representation in self._encoding_dictionary.items():
            if len(representation) != self._representation_value_length:
                raise ValueError(
                    f'Representation [{representation}] for binary key [{binary_key}] does not match length of first '
                    f'representation of [{self._representation_value_length}]')

    def _validate_padding_character(self):
        if len(self._padding_character) != 1:
            raise ValueError(f'The padding character must be a single character. '
                             f'Instead received: [{self._padding_character}]')

        for key, value in self._encoding_dictionary.items():
            if value.endswith(self._padding_character):
                raise ValueError(f'The character [{self._padding_character}] cannot be used for padding as it matches '
                                 f'the trailing characters for the character representation [{value}] associated with '
                                 f'binary key [{key}].')
