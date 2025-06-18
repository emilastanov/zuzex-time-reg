import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode


class Crypt:
    def __init__(self, pin, salt):
        self.pin = pin
        self.salt = salt

    def encrypt(self, string):
        key = self.derive_key()
        fernet = Fernet(key)
        return fernet.encrypt(string.encode()).decode("utf-8")

    def decrypt(self, string):
        fernet = Fernet(self.derive_key())
        return fernet.decrypt(string.encode("utf-8")).decode("utf-8")

    def derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100_000,
            salt=self.salt,
            length=32,
        )
        return urlsafe_b64encode(kdf.derive(self.pin.encode()))

    @staticmethod
    def gen_salt():
        return os.urandom(16)
