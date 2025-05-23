from argon2.low_level import hash_secret, Type
import hashlib
import sys, os

BLOCK_SIZE = 16
PERSONAL_KEY = b"HELLO_IM_UNDER_THE_WATER"

RCON = [
     0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x1B000000, 0x36000000,0x6C000000, 0xD8000000, 0xAB000000, 0x4D000000, 0x9A000000
]

S_BOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

S_BOX_INV = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]


class AES:
    def __init__(self):
        self.keys = []
        self.filename = ""
        self.ex = ".gg"

    def expand_password(self, password):
        salt = hashlib.sha256(password.encode() + PERSONAL_KEY).digest()
        argon2_hash = hash_secret(password.encode(), salt, time_cost=20, memory_cost=1048576, parallelism=8, hash_len=32, type=Type.ID)
        sha3_hash = hashlib.sha3_256(argon2_hash).digest()
        return sha3_hash[:32]

    def rot_word(self, word):
        return word[1:] + word[:1]

    def sub_word(self, temp):
        word = bytearray()
        for i in range(4):
            word.append(S_BOX[temp[i]])
        return bytes(word)

    def xor(self, temp1, temp2):
        word = bytearray()
        for i in range(4):
            word.append(temp1[i] ^ temp2[i])
        return bytes(word)

    def expand_key(self, initial_key):
        words = []
        keys = []

        for i in range(0, 32, 4):
            word = initial_key[i:i+4]
            words.append(word)

        for i in range(8, 60):
                temp = words[i - 1]

                if i % 8 == 0:
                    temp = self.rot_word(temp)
                    temp = self.sub_word(temp)
                    temp = self.xor(temp, RCON[i // 8].to_bytes(4, 'big'))
                elif i % 8 == 4:
                    temp = self.sub_word(self.rot_word(temp)) 

                word = self.xor(temp, words[i - 8])
                words.append(word)

        for i in range(0, len(words), 4):
            keys.append(b''.join(words[i:i+4]))
        return keys

    def get_keys(self):
        password = str(input("Enter passord: "))
        initial_key = self.expand_password(password)
        keys = self.expand_key(initial_key)
        return keys

    def pad(self, data):
        padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        padding = bytes([padding_len] * padding_len)
        return data + padding
    

    def unpad(self, data):
        padding_len = data[-1]
        return data[:-padding_len]
    
    def bytes_to_matrix(self, block):
        matrix = []
        for i in range(4):
            matrix.append(list(block[i::4]))
        return matrix

    def matrix_to_bytes(self, matrix):
        liste = []
        for i in range(4):
            for j in matrix:
                liste.append(j[i])
        return bytes(liste)
    
    def sub_bytes(self, matrix):
        for i in range(4):
            for j in range(4):
                matrix[i][j] = S_BOX[matrix[i][j]]
        return matrix   
    
    def shift_rows(self, matrix):
        for i in range(1, 4):
            matrix[i] = matrix[i][i:] + matrix[i][:i]
        return matrix
    
    def gmul(self, a, b):
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a = (a << 1) & 0xFF
            if hi_bit_set:
                a ^= 0x1B
            b >>= 1
        return p
    
    def mix_single_column(self, col):
        a = col[:]
        col[0] = self.gmul(a[0], 2) ^ self.gmul(a[1], 3) ^ a[2] ^ a[3]
        col[1] = a[0] ^ self.gmul(a[1], 2) ^ self.gmul(a[2], 3) ^ a[3]
        col[2] = a[0] ^ a[1] ^ self.gmul(a[2], 2) ^ self.gmul(a[3], 3)
        col[3] = self.gmul(a[0], 3) ^ a[1] ^ a[2] ^ self.gmul(a[3], 2)
        return col
    
    def mix_columns(self, matrix):
        for i in range(4):
            col = []
            for j in range(4):
                col.append(matrix[j][i])
            mixed = self.mix_single_column(col)
            for row in range(4):
                matrix[row][i] = mixed[row]
        return matrix

    def add_round_key(self, matrix, key):
        matrix_key = self.bytes_to_matrix(key)
        for i in range(4):
            for j in range(4):
                matrix[i][j] = matrix[i][j] ^ matrix_key[i][j]
        return matrix
    
    def inv_shift_rows(self, matrix):
        for i in range(1, 4):
            matrix[i] = matrix[i][-i:] + matrix[i][:-i]
        return matrix
    
    def inv_sub_bytes(self, matrix):
        for i in range(4):
            for j in range(4):
                matrix[i][j] = S_BOX_INV[matrix[i][j]]
        return matrix
    
    def inv_mix_single_column(self, col):
        a = col[:]
        return [
            self.gmul(a[0], 14) ^ self.gmul(a[1], 11) ^ self.gmul(a[2], 13) ^ self.gmul(a[3], 9),
            self.gmul(a[0], 9) ^ self.gmul(a[1], 14) ^ self.gmul(a[2], 11) ^ self.gmul(a[3], 13),
            self.gmul(a[0], 13) ^ self.gmul(a[1], 9) ^ self.gmul(a[2], 14) ^ self.gmul(a[3], 11),
            self.gmul(a[0], 11) ^ self.gmul(a[1], 13) ^ self.gmul(a[2], 9) ^ self.gmul(a[3], 14)
        ]
    
    def inv_mix_columns(self, matrix):
        for i in range(4):
            col = []
            for j in range(4):
                col.append(matrix[j][i])
            mixed = self.inv_mix_single_column(col)
            for row in range(4):
                matrix[row][i] = mixed[row]
        return matrix
  
    def encrypt_block(self, block):
        matrix = self.bytes_to_matrix(block)

        matrix = self.add_round_key(matrix, self.keys[0])

        for i in range(1, 14):
            matrix = self.sub_bytes(matrix)
            matrix = self.shift_rows(matrix)
            matrix = self.mix_columns(matrix)
            matrix = self.add_round_key(matrix, self.keys[i])

        matrix = self.sub_bytes(matrix)
        matrix = self.shift_rows(matrix)
        matrix = self.add_round_key(matrix, self.keys[14])
        
        enc_block = self.matrix_to_bytes(matrix)
        return enc_block
  
    def decrypt_block(self, enc_block):
        matrix = self.bytes_to_matrix(enc_block)

        matrix = self.add_round_key(matrix, self.keys[14])

        for i in range(13, 0, -1):
            matrix = self.inv_shift_rows(matrix)
            matrix = self.inv_sub_bytes(matrix)
            matrix = self.add_round_key(matrix, self.keys[i])
            matrix = self.inv_mix_columns(matrix)

        matrix = self.inv_shift_rows(matrix)
        matrix = self.inv_sub_bytes(matrix)
        matrix = self.add_round_key(matrix, self.keys[0])

        plain = self.matrix_to_bytes(matrix)
        return plain

    def encrypt(self):
        with open(self.filename, "rb") as r1:
            plaintext = r1.read()

        padded = self.pad(plaintext)

        ciphertext = bytearray()
        for i in range(0, len(padded), BLOCK_SIZE):
            block = padded[i:i+BLOCK_SIZE]
            encrypted = self.encrypt_block(block)
            ciphertext.extend(encrypted)

        with open(self.filename, "wb") as r2:
            r2.write(ciphertext)

        os.rename(self.filename, self.filename + self.ex)

    def decrypt(self):
        with open(self.filename, "rb") as r1:
            ciphertext = r1.read()

        decrypted = bytearray()
        for i in range(0, len(ciphertext), BLOCK_SIZE):
            block = ciphertext[i:i+BLOCK_SIZE]
            plaintext = self.decrypt_block(block)
            decrypted.extend(plaintext)
            
        unpadded = self.unpad(decrypted)
        
        with open(self.filename, "wb") as r2:
            r2.write(unpadded)

        os.rename(self.filename, self.filename.replace(self.ex, ""))

    def run(self):  
        self.filename = str(input("Enter filename: "))   
        self.keys = self.get_keys()

        if self.filename.endswith(self.ex):
            self.decrypt()
        else:
            self.encrypt()

if __name__ == "__main__":
    AES().run()