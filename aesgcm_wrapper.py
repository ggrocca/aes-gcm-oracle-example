from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json
import unittest

def encode_raw_bytes(input_bytes):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, mac = cipher.encrypt_and_digest(input_bytes)
    nonce = cipher.nonce
    return key, ciphertext, mac, nonce

def decode_raw_bytes(key, ciphertext, mac, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, mac)
        return decrypted_data
    except:
        return None
    


# dict request syntax:
# {
#     data: "<clear-text>"
# }
# dict response syntax:
# {
#     data: "<base64-encoded-cypher-text>",
#     key: "<base64-encoded-key>",
#     mac: <base64-encoded-mac>,
#     nonce: "<base64-encoded-nonce>"
# }
def encode_dict(request):
    key, ciphertext, mac, nonce = encode_raw_bytes(request['data'].encode("utf-8"))
    response = {
        "data": base64.b64encode(ciphertext).decode("utf-8"),
        "key": base64.b64encode(key).decode("utf-8"),
        "mac": base64.b64encode(mac).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
    }

    return response
    


class TestWrapper(unittest.TestCase):

    clear_text = "foo bar azang zving"

    def test_raw_correct(self):
        key, ciphertext, mac, nonce = encode_raw_bytes(self.clear_text.encode("utf-8"))
        decoded_text = decode_raw_bytes(key, ciphertext, mac, nonce).decode("utf-8")
        self.assertEqual(self.clear_text, decoded_text)

    def test_raw_wrong(self):
        key, ciphertext, mac, nonce = encode_raw_bytes(self.clear_text.encode("utf-8"))
        wrong_key = get_random_bytes(16)
        decoded_text = decode_raw_bytes(wrong_key, ciphertext, mac, nonce)
        self.assertIsNone(decoded_text)

    def test_json(self):
        request = {
            'data': self.clear_text
        }
        response = encode_dict(request)

        for k, v in response.items ():
            response[k] = base64.b64decode(v.encode("utf-8"))

        decoded_text = decode_raw_bytes(response['key'], response['data'], response['mac'], response['nonce']).decode("utf-8")
        self.assertEqual(self.clear_text, decoded_text)
