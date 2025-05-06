import hashlib

def sha256_hash(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()


def xor_gate(key, message):
    encrypted_message = bytearray()
    key_length = len(key)
    for i in range(len(message)):
        encrypted_byte = message[i] ^ key[i % key_length]
        print(message[i], key[i % key_length])
        print(encrypted_byte)
        encrypted_message.append(encrypted_byte)
    return encrypted_message


key = "night"
keys = []

plaintext = "hello world"

print("Start KEY ---------------")
print(key)
print("---------------------\n")

key = sha256_hash(key)
keys.append(key)
key = sha256_hash(key)
keys.append(key)
key = sha256_hash(key)
keys.append(key)

print("plaintext ---------------")
print(plaintext)
print("---------------------\n")

print("KEYS ---------------")
for k in keys:
    print(k)
print("---------------------\n")


enc = xor_gate(keys[0].encode(), plaintext.encode())
enc = xor_gate(keys[1].encode(), enc)
enc = xor_gate(keys[2].encode(), enc)

print("Encrypted ---------------")
print(enc.hex())
print("---------------------\n")

enc = xor_gate(keys[2].encode(), enc)
enc = xor_gate(keys[1].encode(), enc)
enc = xor_gate(keys[0].encode(), enc)

print("Decrypted ---------------")
print(enc.decode())
print("---------------------\n")