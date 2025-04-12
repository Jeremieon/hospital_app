import json
import base64
import hashlib
from django.conf import settings
from django.http import JsonResponse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def load_public_key_components(pem_key):
    public_key = serialization.load_pem_public_key(pem_key.encode("utf-8"))

    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError("Expected RSA public key")

    numbers = public_key.public_numbers()
    n = numbers.n
    e = numbers.e

    # Base64URL encode modulus and exponent
    def b64url_uint(val):
        return (
            base64.urlsafe_b64encode(val.to_bytes((val.bit_length() + 7) // 8, "big"))
            .rstrip(b"=")
            .decode("utf-8")
        )

    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "n": b64url_uint(n),
        "e": b64url_uint(e),
        "kid": generate_kid(pem_key),
    }
    return jwk


def generate_kid(pem_key):
    """Generate a kid from the SHA-256 hash of the public key."""
    key_bytes = pem_key.encode("utf-8")
    sha256 = hashlib.sha256(key_bytes).digest()
    kid = base64.urlsafe_b64encode(sha256).decode("utf-8").rstrip("=")
    return kid


def jwks_view(request):
    public_key = settings.SIMPLE_JWT["VERIFYING_KEY"]
    jwk = load_public_key_components(public_key)
    return JsonResponse({"keys": [jwk]})
