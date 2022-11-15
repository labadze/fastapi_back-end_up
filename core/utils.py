import base64
import os
import typing

import jwt
from cryptography.x509 import load_pem_x509_certificate


async def decode_token(encoded: str) -> typing.Any:
    options = {
        'verify_signature': False,
        'verify_exp': False,  # Skipping expiration date check
        'verify_aud': False
    }
    # public_key_cert = os.getenv("KEYCLOAK_CERT").encode('utf-8')
    public_key_cert = "-----BEGIN CERTIFICATE-----\n{certificate_value}\n-----END CERTIFICATE-----".format(
        certificate_value=os.getenv("KEYCLOAK_CERT")).encode('utf-8')
    cert_obj = load_pem_x509_certificate(public_key_cert)
    public_key = cert_obj.public_key()
    result = jwt.decode(encoded, public_key, algorithms=["RS256"], options=options)
    print(result)
    return result


"""
Decode base64 encoded string
in most cases it's private plain text data provided by user in request body
"""


async def decode_base64_string(encoded_string: str):
    return base64.b64decode(encoded_string).decode('utf-8')
