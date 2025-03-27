from argon2 import PasswordHasher
import hashlib

def create_key(password):
    
    ph = PasswordHasher()

    argon2_hash = ph.hash(password)

    sha3_hash = hashlib.sha3_256(argon2_hash.encode())

    key = sha3_hash.digest()

    print(key[:32])


create_key("password")