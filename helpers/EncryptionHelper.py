import json
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class EncryptionHelper:
    def __init__(self):
        # Retrieve the encryption key from environment variable
        self.key = os.getenv('ENCRYPTION_KEY').encode()
        self.fernet = Fernet(self.key)

    def encrypt(self, data: str) -> bytes:
        return self.fernet.encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        return self.fernet.decrypt(encrypted_data).decode()
