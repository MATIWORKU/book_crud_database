from passlib.context import CryptContext

pwd_hashed = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_hashed.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_hashed.verify(plain_password, hashed_password)
