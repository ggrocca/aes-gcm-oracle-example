from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json
import unittest

def encode_raw(input_string):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(input_string.encode("utf-8"))
    nonce = cipher.nonce
    return key, ciphertext, tag, nonce

def decode_raw(key, ciphertext, tag, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode("utf-8")

class TestWrapper(unittest.TestCase):
    def test_raw(self):
        clear_text = "foo bar azang zving"
        key, ciphertext, tag, nonce = encode_raw(clear_text)
        decoded_text = decode_raw(key, ciphertext, tag, nonce)
        self.assertEqual(clear_text, decoded_text)


# json request syntax:
# {
#     data: "<clear-text>"
# }
# def encode_json(json_request):
    

# json response syntax:
# {
#     data: "<base64-encoded-cypher-text>",
#     key: "<base64-encoded-key>",
#     mac: <base64-encoded-mac>,
#     nonce: "<base64-encoded-nonce>"
# }
# def decode_json(json_response)

