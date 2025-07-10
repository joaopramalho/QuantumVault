from logging import log_message
import os
from Crypto.Cipher import AES

def padding(data):
    pad_len = 16 - len(data) % 16
    pad = bytes([pad_len] * pad_len)
    return data + pad

def unpad(data):
    pad_len = data[-1] # Last byte = num of pad bytes
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encryptAES(input, output):
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        with open(input, 'rb') as file:
            plaintext = file.read()

        pad_plain = padding(plaintext)
        ciphertxt = cipher.encrypt(pad_plain)

        with open(output, "wb") as file:
            file.write(ciphertxt)
        
        encoded_key = key.hex()
        encoded_iv = iv.hex()
        log_message(f"Successfully aes-encrypted for {input} to {output}", "AES Cryptography", "SUCCESS")
        return encoded_key, encoded_iv
    except Exception as e:
        print(f"Error when encrypting AES KEY: {e}")
        log_message(f"Error when encrypting file: {e}", "AES Cryptography", "ERROR")
        return None, None

def decryptAES(key, iv, input_file, output_file):
    try:
        decoded_key = bytes.fromhex(key)
        iv_bytes = bytes.fromhex(iv)
        if len(decoded_key) != 32:
            raise ValueError("Incorrect AES key length")
        cipher = AES.new(decoded_key, AES.MODE_CBC, iv_bytes)
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = unpad(cipher.decrypt(encrypted_data))
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
            log_message(f"Successfully decrypted for {input_file} to {output_file}", "AES Decryptography", "SUCCESS")
    except Exception as e:
        print(f"An error occurred during decryption: {e}")
        log_message(f"Error when decrypting file: {e}", "AES Decryptography", "ERROR")