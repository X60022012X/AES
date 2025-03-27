from argon2 import PasswordHasher
import hashlib
import sys

def create_key(password):  
    ph = PasswordHasher()
    argon2_hash = ph.hash(password)

    sha3_hash = hashlib.sha3_256(argon2_hash.encode())
    key = sha3_hash.digest()

    return key[:32]


class AES:
    def __init__(self):
        self.key = ""
        self.keys = []

    def encrypt(self):
        pass

    def decrypt(self):
        pass





    def run(self):
        if len(sys.argv) != 3:
            print("Hello, im under the water, please help me.")
            sys.exit(1)

        self.filename = sys.argv[1]
        self.key = create_key(sys.argv[2])

        if self.filename.endswith(".GG"):
            self.decrypt()
        else:
            self.encrypt()


print(aes.key)


if __name__ == "__main__":
    aes = AES()
    aes.run()