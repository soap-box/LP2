'''
Columnar transposition
'''


def encrypt(plaintext, key):
    col = len(key)
    row = len(plaintext) // col
    if len(plaintext) % col != 0:
        row += 1
    matrix = [['' for _ in range(col)] for _ in range(row)]
    for i in range(row):
        for j in range(col):
            if i * col + j < len(plaintext):
                matrix[i][j] = plaintext[i * col + j]
            else:
                matrix[i][j] = 'Z'
    print(matrix)
    cipher = ''
    key_order = []
    for i in range(len(key)):
        key_order.append((key[i], i))
    key_order = sorted(key_order)
    for i in range(col):
        for j in range(row):
            cipher += matrix[j][key_order[i][1]]
    return cipher

def decrypt(cipher, key):
    # key = sorted(key)
    # key_order = [key.index(c) for c in key]
    key_order = []
    for i in range(len(key)):
        key_order.append((key[i], i))
    key_order = sorted(key_order)
    col = len(key)
    row = len(cipher) // col
    matrix = [['' for _ in range(col)] for _ in range(row)]
    for i in range(col):
        for j in range(row):
            matrix[j][key_order[i][1]] = cipher[i * row + j]
    print(matrix)
    plaintext = ''
    for i in range(row):
        for j in range(col):
            plaintext += matrix[i][j]
    return plaintext

# def single_columnar(plaintext, key):
#     cipher_text = encrypt()

# print(encrypt('CHINMAY', 'KEY'))
cipher_text = encrypt('CHINMAY', 'KEY')
print(cipher_text)
print(decrypt(cipher_text, 'KEY'))
