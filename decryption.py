from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os
import json

aesKey = os.urandom(32)
hmacKey = os.urandom(64)

def initPrivateKey():
    # Initialize RSA object + load private key into RSA object
    with open("private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
            )
    return private_key

def decryptRSA(private_key,rsaCipherText):
#Decrypt the RSA Ciphertext
    plaintext = private_key.decrypt(
        rsaCipherText,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            ) )
    return plaintext


def decryptEverything(plainText,cipherText,tag):
    #Recover keys (#2)
    
    aesKey = plainText[:len(plainText)//2]
    hmacKey = plainText[:len(plainText)//2]

    h = hmac.HMAC(hmacKey, hashes.SHA256(), backend = default_backend())

    h.update(cipherText)            

    comparisonTag = h.finalize()
    
    if comparisonTag != tag:
        print ("FK it didnt work")
        return
    
    else:
        ##### AES PART ######
        backend = default_backend()
        #Generate 256 bit AES key (#1)
        aesKey = os.urandom(32)         ##MAKE NEW KEY OR USE OLD ONE???
        #Prepend the IV
        iv = os.urandom(16)
        #Initialize AES object
        cipher = Cipher(algorithms.AES(aesKey),modes.CBC(iv), backend = backend)
        #Sets up encryptor
        encryptor = cipher.encryptor()
        #AES encrypts the message
        newCt = encryptor.update(b'Some secret message here')   ##SAME MESSAGE??#
        #Decrpy the ciphertext
        decryptor = cipher.decryptor()
        aesPlainText = decryptor.update(newCt) + decryptor.finalize()
        
    print (aesPlainText)

