import unittest

from ..lib.data import EncodingDefinitionTable, get_or_default_dictionary, get_or_default_padding


class EncodingDefinitionTableTest(unittest.TestCase):

    def test_initialize_table_with_invalid_definition(self):
        arguments = [
            ('Empty dictionary.', 'at least one entry.', '=', {}),
            ('Dictionary with 0 length key.', 'greater than 0.', '=', {'': '/'}),
            ('Different length binary keys.', 'does not match length of first', '=', {'1': '-', '12': '+'}),
            ('Binary key with more than 0 and 1.', 'only contain the characters 0 and 1', '=', {'2': '-'}),
            ('Dictionary with 0 length value.', 'greater than 0', '=', {'1': ''}),
            ('Different length representations.', 'does not match length of first', '=', {'1': '-', '0': '++'}),
            ('Padding matching trailing representation character.', 'the trailing characters for the character representation', '=', {'1': '_='})
        ]
        for args in arguments:
            with self.subTest(msg=args[0]):
                with self.assertRaises(ValueError) as context:
                    EncodingDefinitionTable(args[3], args[2])
                self.assertTrue(args[1] in str(context.exception))

    def test_initialize_table_with_valid_definition(self):
        EncodingDefinitionTable(get_or_default_dictionary(None), get_or_default_padding(None))
