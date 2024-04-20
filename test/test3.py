import os
from cryptography.fernet import Fernet


key = Fernet.generate_key()
print("The key is", key)
text = "Hello, World!"

print("Original text:", text)
cipher_text = Fernet(key).encrypt(text.encode())
print("Encrypted text:", cipher_text)
plain_text = Fernet(key).decrypt(cipher_text).decode()
print("Decrypted text:", plain_text)
