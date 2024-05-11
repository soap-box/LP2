'''
RSA
'''

import random

def isPrime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
        else:
            i = i + 1
    return True
        
def isCoPrime(n1, n2):
    res = 1
    while(n2 != 0):
        res = n1 % n2
        n1 = n2
        n2 = res
    return True if n1==1 else False

def generatePrime():
    while True:
        n = random.randrange(300, 500)
        if(isPrime(n) == True):
            return n
        
def generateE(phiOfN):
    while True:
        e = random.randrange(2, phiOfN)
        if(isCoPrime(phiOfN, e) == True):
            return e

def calculateD(phiOfN, e):
    d = 0
    while((d*e) % phiOfN != 1):
        d += 1
    return d

def cipher(plainText, e, n):
    # temp = len(plainText)
    cipherText = []
    for i in plainText:
        cipherText.append((ord(i) ** e) % n)
    return cipherText

def decipher(cipherText, d, n):
    text = []
    for i in cipherText:
        text.append(chr((i ** d) % n))
    return text

if __name__=='__main__':
    text = input("Enter text: ")
    p = generatePrime()
    q = generatePrime()
    n = p * q
    phiOfN = (p-1)*(q-1)
    e = generateE(phiOfN=phiOfN)
    ct = cipher(plainText=text, e=e, n=n)
    print(ct)
    d = calculateD(phiOfN=phiOfN, e=e)
    pt = decipher(cipherText=ct, d=d, n=n)
    print(pt)