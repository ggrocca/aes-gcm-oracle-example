from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encode(input_string):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(input_string.encode("utf-8"))
    nonce = cipher.nonce
    return key, ciphertext, tag, nonce

def decode(key, ciphertext, tag, nonce):
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data.decode("utf-8")

key, ciphertext, tag, nonce = encode("foo bar azang zving")
data = decode(key, ciphertext, tag, nonce)
print(data)
