# an AES-GCM microservice example

This is the example implementation of a micro-service that encrypts a text payload with a random key, using AES-GCM. I have coded this to learn a bit of Python, Flask and pycryptodome (all technologies that are new to me), and to better understand the properties of the AES-GCM encryption algorithm. Basic unit and integration tests are provided too. Anyway, don't assume that this code is optimaal, correct or without errors.

## Main goals and working assumptions
- The micro-service is accessible through https only (given that this is a working example, ad-hoc certificates will be used).
- The micro-service does not internally store uploaded data payloads, nor generated keys.
- The micro-service generates a new random key every time a new call is made.
- The micro-service provides a single API call. Input: payload; output: encrypted paylod and anything that is needed for decryption.
- The micro-service assumes a text (UTF-8) payload.
- There is no need for additional data to be authenticated, but not encrypted (this is a feature that AES-GCM could provide, though).
- No salt step is necessary when creating the key, given that we are not starting from a passphrase but we're directly generating random keys.

## Specification and implementation details
- Call syntax: POST `/oracleinvocation/`, with JSON payload
```
{
    data: "<clear-text>"
}
```
- Call response:
```
{
    data: "<base64-encoded-cypher-text>",
    key: "<base64-encoded-key>",
    mac: <base64-encoded-mac>,
    nonce: "<base64-encoded-nonce>"
}
```
- Unit test: <TBD. python unittest?> 
- Integration test: <TBD. call with ... requires curl+bash?>

## Using and running
After cloning, do
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

To get out of the virtual environment, run `deactivate`.

To perform provided unit tests on the aesgc_wrapper module, run:
```
python3 -m unittest aesgcm_wrapper.py
```


## Appendix
I've only tested and used this on macOS, with python 3.8 installed using brew. Should work everywhere else, though.

### Sources and resources
[Bytes to string in AES encryption and decryption in Python 3 - Stack Overflow](https://stackoverflow.com/questions/50481366/bytes-to-string-in-aes-encryption-and-decryption-in-python-3/50482935)
[GitHub - wolf43/AES-GCM-example: An example of AES GCM encryption mode using Pycryptodome](https://github.com/wolf43/AES-GCM-example)
[Galois/Counter Mode - Wikipedia](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
[Advanced Encryption Standard - Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
[Getting Started With Testing in Python – Real Python](https://realpython.com/python-testing/#automated-vs-manual-testing)
