from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
import base64
import os

load_dotenv()

key_base64 = os.getenv("AES_KEY")
key = base64.b64decode(key_base64)


def derive_iv(data, key):
    h = HMAC.new(key, digestmod=SHA256)
    h.update(data.encode())
    return h.digest()[:16]


def encrypt_cbc(plain_text, key):
    iv = derive_iv(plain_text, key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plain_text.encode(), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_text).decode()


def decrypt_cbc(encrypted_text, key, plain_text):
    iv = derive_iv(plain_text, key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decoded_encrypted_text = base64.b64decode(encrypted_text)
    decrypted_text = unpad(cipher.decrypt(decoded_encrypted_text), AES.block_size)
    return decrypted_text.decode()
