from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# encode
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest("prova prova prova".encode("utf-8"))
nonce = cipher.nonce

# decode
cipher = AES.new(key, AES.MODE_GCM, nonce)
decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

print(decrypted_data.decode("utf-8"))
