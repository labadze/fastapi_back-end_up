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
    public_key_cert = "-----BEGIN CERTIFICATE-----\nMIIClzCCAX8CBgGEcGBSXzANBgkqhkiG9w0BAQsFADAPMQ0wCwYDVQQDDARmYXB5MB4XDTIyMTExMzA5NDI1MVoXDTMyMTExMzA5NDQzMVowDzENMAsGA1UEAwwEZmFweTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAIMcKfI1wwT/7z+ulGSTu27TSzQiuP86YzoGRXZAyR/+8/8rdYKX7zYNqwi75tRWHtU32rKzs1FC2k4aBYlrDxRsfjKkAz0b6nmHMPtphOQEQZz/yL1nupHxBWs1sOl8pe9MX0aCbDZr4HV9sV9f7uRkEWC4C18wy6LLYFbJctYk0+U03AXZqvkKmIfUyZFYjw/9t767+PFbpw3AKwxvmAse2E1UFb/QPsAzcTsfBp0Z6nTJHGbTQX1TqDvkZ8oLPYocjHw09qE8iZMf0UKYj5RPReulLmgJUc+lQzhKHlujekg1V7FTpZt6iR/qXBH0mK4Y26lAqUvC47KTgOFwM7sCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAUDZ1YoF+mMpzg3h6u6VC4d8iEW/4SkKlgU5y51bjrLu5WlmTZxFI5lfOTDnnHWYLacrXRYyIVZarBd87lH0EzSN1Cs416xMaQCZVHhPzqj0Uzdb6ojOFPXcLqDLR48VeRQVgBuLHx/l44mP95QbwKjGuL6pHFR1/ivuAK5hi3A8drx8PLLxPZNzg/L1bXtqTfisvKOM8zsPCSiZZMGjZ97feZ6yIPsWEBE8q/f8vycYYG7jcIlXxd3gF3Vsovpn8cVA71c9eimd6x2c2oF5TybRkMSvPNBHCnY2txCmXR043zA2Esj/Gqj7rqeOPyxTC0KZuvvN5F7ciOXB0IN73ug==\n-----END CERTIFICATE-----".encode('utf-8')# os.getenv("KEYCLOAK_CERT").encode()
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
