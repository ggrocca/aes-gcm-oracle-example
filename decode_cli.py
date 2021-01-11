import sys
import base64
from aesgcm_wrapper import decode_raw_bytes


if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} key data mac nonce")
    exit(1)

response = [];
for arg in sys.argv[1:]:
    response.append(base64.b64decode(arg.encode("utf-8")))

decoded_text = decode_raw_bytes(response[0], response[1], response[2], response[3]).decode("utf-8")

print(decoded_text);
