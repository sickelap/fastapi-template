from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

ph = PasswordHasher()


def password_rules_ok(password):
    return True


def verify_password(plain_password, hashed_password):
    try:
        return ph.verify(hashed_password, plain_password)
    except VerificationError:
        return False


def get_password_hash(password):
    return ph.hash(password)
