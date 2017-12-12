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
def initPublicKey():
    
    with open("public.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),backend=default_backend()
            )
    return public_key

def aesEncryption():
    backend = default_backend()
    #Generate 256 bit AES key (#1)
    aesKey = os.urandom(32)
    #Prepend the IV
    iv = os.urandom(16)
    #Initialize AES object
    cipher = Cipher(algorithms.AES(aesKey),modes.CBC(iv), backend = backend)
    #Sets up encryptor
    encryptor = cipher.encryptor()
    #AES encrypts the message
    ct = encryptor.update(b'Some secret message here')
    return ct


def runHmac(ct):
    #Generate a key for HMAC (#2)
    hmacKey = os.urandom(32)
    #Run HMAC (Sha256)
    h = hmac.HMAC(hmacKey, hashes.SHA256(), backend = default_backend())
    #The bytes to hash and authenticate
    h.update(ct)
    #Finalize the current context and return the message digest as bytes.
    tag = h.finalize()
    return tag


def rsaEncrypt(public_key,keysConcat):
    #RSA encryption on keys
    rsaCipherText = public_key.encrypt(keysConcat,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return rsaCipherText

def jsonConv(rsaCipherText):
    d = {
	'RSA Ciphertext': rsaCipherText,

    }
    f = json.dumps(d, sort_keys=True, indent=4)
    print(f)
    return f


def printCipher(rsaCipherText,ct,tag):
    #RSA ciphertext
    print ("RSA ciphertext")
    print()
    print(rsaCipherText)
    print()
    print("----------------------")

    #AES ciphertext

    print("AES ciphertext")
    print()
    print(ct)
    print()

    print("----------------------")
    #HMAC ciphertext
    print("HMAC tag")
    print()
    print(tag)
    print("----------------------")
    return
