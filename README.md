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
