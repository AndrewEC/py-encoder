from typing import List
import string
from random import randrange
import unittest
from base64 import b64encode

from timeout import timeout

from ..lib.encode import encode_string
from ..lib.decode import decode_to_string
from ..lib.generator import generate_encoding_dictionary


class EncodeDecodeTest(unittest.TestCase):

    @timeout(3)
    def test_base64_encoding(self):
        generated_strings = self._generate_test_strings()
        for generated_string in generated_strings:
            with self.subTest(generated_string):
                custom_encoded_string = encode_string(generated_string)
                standard_encoded_string = str(b64encode(bytes(generated_string, 'utf-8')), 'utf-8')

                self.assertNotEqual(generated_string, custom_encoded_string)
                self.assertEqual(custom_encoded_string, standard_encoded_string)

                decoded_string = decode_to_string(custom_encoded_string)
                self.assertEqual(generated_string, decoded_string)

    @timeout(3)
    def test_encoding_generated_dictionary(self):
        generated_strings = self._generate_test_strings()

        for generated_string in generated_strings:
            binary_key_length = randrange(3, 6)
            representation_length = randrange(1, 2)

            with self.subTest(generated_string):
                dictionary = generate_encoding_dictionary(binary_key_length, representation_length, '=')

                encode_result = encode_string(generated_string, dictionary.mappings, dictionary.padding_character)
                self.assertNotEqual(encode_result,generated_string)

                decode_result = decode_to_string(encode_result, dictionary.mappings, dictionary.padding_character)
                self.assertEqual(decode_result, generated_string)

    def _generate_test_strings(self) -> List[str]:
        generated_strings = []
        while len(generated_strings) < 100:
            generated_string = self._generate_string()
            if generated_string in generated_strings:
                continue
            generated_strings.append(generated_string)
        return generated_strings

    def _generate_string(self) -> str:
        string_length = randrange(1, 1000)
        characters = string.ascii_uppercase + string.ascii_lowercase + string.punctuation
        character_count = len(characters)
        return ''.join(characters[randrange(character_count)] for _ in range(string_length))
