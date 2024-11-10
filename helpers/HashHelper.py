import hashlib


class HashHelper:

    @staticmethod
    def hash(password: str) -> str:
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed
