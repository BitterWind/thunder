from passlib.hash import sha256_crypt

def verify_password(plain_password: str, hashed_password: str):
    return sha256_crypt.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return sha256_crypt.hash(password)