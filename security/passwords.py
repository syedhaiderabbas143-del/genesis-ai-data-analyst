"""Password hashing using PBKDF2-HMAC-SHA256 from the Python standard library."""
import base64, hashlib, hmac, secrets
ITERATIONS = 310_000

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, ITERATIONS)
    return f'pbkdf2_sha256${ITERATIONS}${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}'

def verify_password(password: str, encoded: str) -> bool:
    try:
        _, iterations, salt_b64, digest_b64 = encoded.split('$', 3)
        salt=base64.urlsafe_b64decode(salt_b64.encode()); expected=base64.urlsafe_b64decode(digest_b64.encode())
        actual=hashlib.pbkdf2_hmac('sha256', password.encode(), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except Exception: return False
