from argon2 import PasswordHasher


ph = PasswordHasher()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return ph.verify(hash=hashed_password, password=plain_password)


def get_hashed_password(password: str) -> str:
    return ph.hash(password=password)
