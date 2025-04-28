from argon2 import PasswordHasher
import hashlib
import sys, os


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
        self.filename = ""
        self.ex = ".GG"

    def sha256_hash(self, data):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        return sha256_hash.hexdigest()

    def xor_gate(self, key, message):
        encrypted_message = bytearray()
        key_length = len(key)
        for i in range(len(message)):
            encrypted_byte = message[i] ^ key[i % key_length]
            encrypted_message.append(encrypted_byte)
        return encrypted_message
    
    def MakeKeys(self):
        for i in range(5):
            self.key = self.sha256_hash(self.key)
            self.keys.append(self.key)

        for pp in self.keys:
            print(pp)

    def decrypt_file(self):
        with open(self.filename, "rb") as r1:
            enc = r1.read()

        
        for i in range(len(self.keys)-1, -1, -1):
            enc = self.xor_gate(self.keys[i].encode(), enc)
            
        
        with open(self.filename, "wb") as r2:
            r2.write(enc)

        os.rename(self.filename, self.filename.replace(self.ex, ""))


    def encrypt_file(self):
        with open(self.filename, "rb") as r1:
            enc = r1.read()

        
        for i in range(len(self.keys)):
            enc = self.xor_gate(self.keys[i].encode(), enc)

        
        with open(self.filename, "wb") as r2:
            r2.write(enc)

        os.rename(self.filename, self.filename + self.ex)



    def run(self):
        """if len(sys.argv) != 3:
            print("Usage: sudo python3 CRYP256.py <filename/.txt/.png/.jpg> <key/sha640>")
            print("Example: sudo python3 CRYP256.py cat.png 3f307c4a23b754bc8e6f4a119ca4558e0e06d99287810e175ed870cea26fccd2b1354a4b49303a10")
            sys.exit(1)

        self.filename = sys.argv[1]
        self.key = sha640(sys.argv[2].encode("utf-8"))
        self.switch = self.switch_the_switch()
        self.make_keys()

        if self.filename.endswith(".CRYP256"):
            self.decrypt_file()
        else:
            self.encrypt_file()"""
        


        self.filename = "leo/test.txt.GG"
        self.key = "password1234"
        self.MakeKeys()

        if self.filename.endswith(self.ex):
            self.decrypt_file()
        else:
            self.encrypt_file()


if __name__ == "__main__":
    AES().run()