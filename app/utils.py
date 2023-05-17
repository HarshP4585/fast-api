from passlib.context import CryptContext
context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(data):
    return context.hash(data)
