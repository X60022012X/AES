from pass_expan import expand_password
from constants import *

#Rotate bytes i word
def rot_word(word):
     return word[1:] + word[:1]

#Substitute bytes in word
def sub_word(temp):
    word = bytearray()
    for i in range(4):
        word.append(S_BOX[temp[i]])
    return bytes(word)

#XOR two byte objects
def xor(temp1, temp2):
    word = bytearray()
    for i in range(4):
        word.append(temp1[i] ^ temp2[i])
    return bytes(word)


def expand_key(password):
    initial_key = expand_password(password)

    words = []
    keys = []

    #Transform initial key to words(4 bytes)
    for i in range(0, 32, 4):
        word = initial_key[i:i+4]
        words.append(word)

    #Create remaining words(4 bytes)
    for i in range(8, 60):
            temp = words[i - 1]

            if i % 8 == 0:
                temp = rot_word(temp)
                temp = sub_word(temp)
                temp = xor(temp, RCON[i // 8].to_bytes(4, 'big'))
            elif i % 8 == 4:
                temp = sub_word(rot_word(temp)) 

            word = xor(temp, words[i - 8])
            words.append(word)

    #Transfrom from words(4 bytes) to keys(4 words)
    for i in range(0, len(words), 4):
        keys.append(b''.join(words[i:i+4]))

    return keys