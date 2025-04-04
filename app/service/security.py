from passlib.context import CryptContext

security_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return security_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return security_context.hash(password)
