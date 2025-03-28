from argon2.low_level import hash_secret, Type
import hashlib

#Set personal key
PERSONAL_KEY = b"HELLO_IM_UNDER_THE_WATER"

def create_key(password):
    #Create salt by SHA-3-256 hashing password + pepper  
    salt = hashlib.sha256(password.encode() + PERSONAL_KEY).digest()

    #Create key by argon2 hashing the password with salt
    argon2_hash = hash_secret(password.encode(), salt, time_cost=20, memory_cost=1048576, parallelism=8, hash_len=32, type=Type.ID)

    #Hash key again with SHA-3-256 to remove possible patterns left by argon2
    sha3_hash = hashlib.sha3_256(argon2_hash).digest()

    #Make sure key is 32 byte or 256 bits
    return sha3_hash[:32]

print(create_key("password"))