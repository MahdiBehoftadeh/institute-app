import hashlib
import os

import bcrypt
from dotenv import load_dotenv


class HashHelper:

    @staticmethod
    def hash(password: str) -> str:
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        # Check if the plain password, hashed with the fixed salt, matches the stored hash
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
