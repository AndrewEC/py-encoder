import unittest

from ..lib.encode import encode_string
from ..lib.decode import decode_to_string


class EncodeDecodeTest(unittest.TestCase):

    _UNENCODED = 'Testing123!@#'
    _ENCODED = 'VGVzdGluZzEyMyFAIw=='

    def test_base64_encoding(self):
        encode_result = encode_string(EncodeDecodeTest._UNENCODED)
        self.assertEqual(EncodeDecodeTest._ENCODED, encode_result)

        decode_result = decode_to_string(encode_result)
        self.assertEqual(EncodeDecodeTest._UNENCODED, decode_result)
