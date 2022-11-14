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
    public_key_cert = public_key_cert = "-----BEGIN CERTIFICATE-----\nMIICoTCCAYkCBgGEdeUE9DANBgkqhkiG9w0BAQsFADAUMRIwEAYDVQQDDAlhZG1pbi1jbGkwHhcNMjIxMTE0MTEyNTU0WhcNMzIxMTE0MTEyNzM0WjAUMRIwEAYDVQQDDAlhZG1pbi1jbGkwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCdtho7ka+qmuK5EXNI9vjzSP5Joal6qamY3dYUMu5ZbxFmQcvRXSptwCKFzWh/PSl2dn31liMbsMZuuOKqEyttOZJm44CCZGuwB3TgAZ3RJTEhQXUQ2o+6UmCBXSxiIzo/uSGPZlRGQthFhs8V+raHVMoU5NNfjZY8bdff+bN0r8vCNi7lsUEeYSvBk66TmJl5XU5Umtw4LzUktBtaeAjbteaARsWqexUbWqzJQ7Kxb3WNY5uHLKd8j4wzcEtZuGS7gOVCkOyjRIeBMdQBc9yPOaYNHaFzkT/xNXn4GqCTfyJec/DXOa2uETooi+BAqE+x39SHVCsV1dnNZ1Gisnn1AgMBAAEwDQYJKoZIhvcNAQELBQADggEBABoDbV3kqHl3gmAAWaIrUjjUXhbcU/LprWQdsFoPbraEw4qKE3++9AyfFLS4u+dpQ/qhtxDyFEgCYOCG0O6qM5dQehTqpAaZDNt5GP0k5Pfe7f+ZNNNRwfiJ2CtxwA1V+5on0yqFo0//gxOFXf2yKbYjudhkmyhxoRuYGH1fEklNXQE1Zoq3/NBKxwmLPsdo30S6oGy7QCnaIWHEsCPJKUsuNRpwM9V9MFCkVOhScZYVFiR+aLB3Az8mHrzUQ1Oo/VcW5O3Vz4ckM9gPUTq6cHabVpzyAd3psDQTo6QrogAkKlCXIM1pA2qoMWOYS/BFGHhbOM5c1Ps0PqndHsFNiJM=\n-----END CERTIFICATE-----".encode('utf-8')
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
