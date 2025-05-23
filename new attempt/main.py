from pass_expan import expand_password
from key_expan import expand_key
from constants import *
import sys, os

class AES:
    def __init__(self):
        self.keys = []
        self.filename = ""
        self.ex = ".cooked"

    def get_keys(self):
        password = str(input("Enter passord: "))
        initial_key = expand_password(password)
        keys = expand_key(initial_key)
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