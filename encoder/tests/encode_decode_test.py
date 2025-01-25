from typing import List
import string
from random import randrange
import unittest
from base64 import b64encode

from encoder.lib.encode import encode_string
from encoder.lib.decode import decode_to_string
from encoder.lib.generator import generate_encoding_dictionary


class EncodeDecodeTest(unittest.TestCase):

    def test_base64_encoding(self):
        for generated_string in self._generate_test_strings():
            with self.subTest(generated_string):
                custom_encoded_string = encode_string(generated_string)
                standard_encoded_string = str(b64encode(bytes(generated_string, 'utf-8')), 'utf-8')

                self.assertNotEqual(generated_string, custom_encoded_string)
                self.assertEqual(custom_encoded_string, standard_encoded_string)

                decoded_string = decode_to_string(custom_encoded_string)
                self.assertEqual(generated_string, decoded_string)

    def test_encoding_generated_dictionary(self):
        for generated_string in self._generate_test_strings():
            binary_key_length = randrange(3, 10)
            representation_length = randrange(5, 10)

            subtest_message = (f'key_length=[{binary_key_length}], '
                               f'representation_length=[{representation_length}], '
                               f'string=[{generated_string}]')

            with self.subTest(subtest_message):
                dictionary = generate_encoding_dictionary(binary_key_length, representation_length, '=')

                encode_result = encode_string(generated_string, dictionary.mappings, dictionary.padding_character)
                self.assertNotEqual(encode_result, generated_string)

                decode_result = decode_to_string(encode_result, dictionary.mappings, dictionary.padding_character)
                self.assertEqual(decode_result, generated_string)

    def _generate_test_strings(self) -> List[str]:
        generated_strings = set()
        while len(generated_strings) < 50:
            generated_strings.add(self._generate_string())
        return list(generated_strings)

    def _generate_string(self) -> str:
        string_length = randrange(1, 100)
        characters = string.ascii_uppercase + string.ascii_lowercase + string.punctuation
        character_count = len(characters)
        return ''.join(characters[randrange(character_count)] for _ in range(string_length))
