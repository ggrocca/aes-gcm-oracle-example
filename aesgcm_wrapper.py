from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json
import unittest

def encode_raw_bytes(input_bytes):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(input_bytes)
    nonce = cipher.nonce
    return key, ciphertext, tag, nonce

def decode_raw_bytes(key, ciphertext, tag, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data
    except:
        return None
    


# json request syntax:
# {
#     data: "<clear-text>"
# }
# json response syntax:
# {
#     data: "<base64-encoded-cypher-text>",
#     key: "<base64-encoded-key>",
#     mac: <base64-encoded-mac>,
#     nonce: "<base64-encoded-nonce>"
# }
def encode_json(json_request):
    json_response = '{"data":"TWFu","key":"TWFu","mac":"TWFu","nonce":"TWFu"}'
    return json_response
    

class TestWrapper(unittest.TestCase):

    clear_text = "foo bar azang zving"

    def test_raw_correct(self):
        key, ciphertext, tag, nonce = encode_raw_bytes(self.clear_text.encode("utf-8"))
        decoded_text = decode_raw_bytes(key, ciphertext, tag, nonce).decode("utf-8")
        self.assertEqual(self.clear_text, decoded_text)

    def test_raw_wrong(self):
        key, ciphertext, tag, nonce = encode_raw_bytes(self.clear_text.encode("utf-8"))
        wrong_key = get_random_bytes(16)
        decoded_text = decode_raw_bytes(wrong_key, ciphertext, tag, nonce)
        self.assertIsNone(decoded_text)

    def test_json(self):
        json_request = json.dumps({'data': self.clear_text})
        json_response = encode_json(json_request)

        result = json.loads(json_response)

        for k, v in result.items ():
            result[k] = base64.b64decode(v)

        decoded_text = decode_raw_bytes(result['key'], result['data'], result['mac'], result['nonce']).decode("utf-8")
        self.assertEqual(self.clear_text, decoded_text)
