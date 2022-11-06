import unittest

from .timeout_util import timeout

from ..lib.generator import generate_encoding_dictionary
from ..lib.data import EncodingDefinitionTable


class GeneratorTest(unittest.TestCase):

    @timeout(5)
    def test_generate_valid_dictionaries(self):
        arguments = [
            (6, 1, '='),
            (3, 2, '/#'),
            (7, 3, '_')
        ]
        for args in arguments:
            with self.subTest(binary_key_length=args[0], representation_length=args[1], padding_character=args[2]):
                dictionary = generate_encoding_dictionary(args[0], args[1], args[2])
                EncodingDefinitionTable(dictionary.mappings, dictionary.padding_character)

                first_key = next((_ for _ in dictionary.mappings.keys()))
                self.assertEqual(args[0], len(first_key))

                first_representation = next((_ for _ in dictionary.mappings.values()))
                self.assertEqual(args[1], len(first_representation))

    @timeout(5)
    def test_generate_dictionaries_with_invalid_inputs(self):
        arguments = [
            (0, 1, '='),
            (1, 0, '='),
            (1, 1, '')
        ]
        for args in arguments:
            with self.subTest(binary_key_length=args[0], representation_length=args[1], padding_character=args[2]):
                with self.assertRaises(ValueError):
                    generate_encoding_dictionary(args[0], args[1], args[2])
