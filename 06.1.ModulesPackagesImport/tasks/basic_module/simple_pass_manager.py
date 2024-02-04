# TODO: Split this file into pkg

from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import string
import secrets
import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


BACKEND = default_backend()
ITERATIONS = 100_000


def generate_key() -> bytes:
    """Generate key for encryption"""
    return Fernet.generate_key()


def key_encrypt(message: bytes, key: bytes) -> bytes:
    """Encrypt message using secret key"""
    return Fernet(key).encrypt(message)


def key_decrypt(token: bytes, key: bytes) -> bytes:
    """Decrypt message from token using secret key"""
    return Fernet(key).decrypt(token)


def _derive_key(password: bytes, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str, iterations: int = ITERATIONS) -> bytes:
    """Encrypt message using password to generate key"""
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )


def password_decrypt(token: bytes, password: str) -> bytes:
    """Decrypt message from token using password to generate key"""
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)


LETTERS = string.ascii_letters
DIGITS = string.digits
SPECIAL = '-_+#!@$%^:;*()[]'


def generate_password(pass_len: int = 32, letters: bool = True, digits: bool = True, special: bool = True) -> str:
    """Generate pass with alphabet control"""
    assert pass_len > 0

    alphabet: str = ''
    if letters:
        alphabet += LETTERS
    if digits:
        alphabet += DIGITS
    if special:
        alphabet += SPECIAL

    assert alphabet, 'Can not generate password with empty alphabet'

    return ''.join(secrets.choice(alphabet) for i in range(pass_len))


def generate_urlsafe_password(pass_len: int = 32) -> str:
    """Generate url-safe pass"""
    assert pass_len > 0
    return secrets.token_urlsafe(pass_len)[:pass_len]


class PasswordManagerError(ValueError):
    pass


class PasswordNotStoredError(PasswordManagerError):
    pass


class PasswordLengthError(PasswordManagerError):
    pass


PASS_LEN_MIN = 4


class PasswordManager:
    def __init__(self, secret_password: str, default_pass_len: int = 32):
        assert len(secret_password) > 0
        self._secret_hash = self._hash(secret_password)
        self._secret_storage: dict[str, bytes] = {}

        if default_pass_len < PASS_LEN_MIN:
            raise PasswordLengthError(f'Password length should be >= {PASS_LEN_MIN}')
        self._default_pass_len = default_pass_len

    @staticmethod
    def _hash(obj: str | bytes) -> str:
        if isinstance(obj, str):
            obj = obj.encode()

        return hashlib.sha256(obj).hexdigest()

    def __len__(self) -> int:
        return len(self._secret_storage)

    def validate_secret_hash(self, secret_password: str) -> bool:
        return self._secret_hash == self._hash(secret_password)

    def add_password(self, password: str, name: str) -> None:
        self._secret_storage[name] = password_encrypt(password.encode(), self._secret_hash)

    def get_password(self, name: str) -> str:
        if name not in self._secret_storage:
            raise PasswordNotStoredError(f'{name} is not stored')

        return password_decrypt(self._secret_storage[name], self._secret_hash).decode()

    def generate_password(self, pass_len: int | None = None) -> str:
        pass_len = pass_len or self._default_pass_len
        if pass_len < PASS_LEN_MIN:
            raise PasswordLengthError(f'Password length should be >= {PASS_LEN_MIN}')

        return generate_urlsafe_password(pass_len)
