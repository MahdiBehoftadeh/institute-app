import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


class EncryptionHelper:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY').encode()
        self.fernet = Fernet(self.key)

    def encrypt(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode()
