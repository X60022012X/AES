from pass_expan import expand_password

first_key = expand_password("password")
print(first_key)
print(list(first_key))
print(bytes(list(first_key)))

words = []

for i in range(0, 32, 4):
    word = first_key[i:i+4]
    words.append(word)


print(first_key)
print(len(list(first_key)))

print(words)