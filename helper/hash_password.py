from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes="bcrypt", deprecated="auto")

def hash_pass(password):
    return bcrypt_context.hash(password)

def verify_pass(request_pass, hashed_pass):
    return bcrypt_context.verify(request_pass, hashed_pass)
