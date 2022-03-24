import unittest

from ..lib.encode import encode_string
from ..lib.decode import decode_to_string
from ..lib.generator import generate_encoding_dictionary


class EncodeDecodeTest(unittest.TestCase):

    _UNENCODED = 'Testing123!@#'
    _ENCODED = 'VGVzdGluZzEyMyFAIw=='

    def test_base64_encoding(self):
        encode_result = encode_string(EncodeDecodeTest._UNENCODED)
        self.assertEqual(EncodeDecodeTest._ENCODED, encode_result)

        decode_result = decode_to_string(encode_result)
        self.assertEqual(EncodeDecodeTest._UNENCODED, decode_result)

    def test_encoding_generated_dictionary(self):
        dictionary = generate_encoding_dictionary(6, 1, '/')

        encode_result = encode_string(EncodeDecodeTest._UNENCODED, dictionary, '/')
        self.assertNotEqual(encode_result, EncodeDecodeTest._UNENCODED)

        decode_result = decode_to_string(encode_result, dictionary, '/')
        self.assertEqual(decode_result, EncodeDecodeTest._UNENCODED)
