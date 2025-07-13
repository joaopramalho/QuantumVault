import os
from Crypto.Cipher import AES
from pqcrypto.kem.ml_kem_1024 import generate_keypair, encrypt as kem_encrypt, decrypt as kem_decrypt
from utils.logging import log_message
from .qvaults import QVaultFormat

def padding(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    
    if pad_len < 1 or pad_len > 16:
        log_message(f"Invalid Padding when unpadding {data}", "CRYPTOGRAPHY UNPADDING", "ERROR")
        raise ValueError("Invalid padding")
    
    log_message(f"Success on unpadding data", "CRYPTOGRAPHY UNPADDING", "SUCESS")
    return data[:-pad_len]

def encryptAES(input_file, aes_key):
    iv = os.urandom(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    padded = padding(plaintext)

    ciphertext = cipher.encrypt(padded)
    return ciphertext, iv

def encrypt_hybrid(input_file, output_file):
    try:
        public_key, secret_key = generate_keypair()
        kem_ciphertext, shared_secret = kem_encrypt(public_key)

        aes_key = shared_secret[:32]
        ciphertext, iv = encryptAES(input_file, aes_key)

        if output_file.endswith('.qvault'):
            import os
            _, original_extension = os.path.splitext(input_file)
            
            QVaultFormat.pack_qvault(
                ciphertext,
                iv,
                kem_ciphertext,
                public_key,
                output_file,
                original_extension
            )
            
            # salvar key
            secret_key_file = output_file.replace('.qvault', '.key')
            try:
                with open(secret_key_file, 'wb') as f:
                    f.write(secret_key)
                log_message(f"Secret key saved successfully to: {secret_key_file}", "HYBRID CRYPTOGRAPHY", "INFO")
            except IOError as e:
                log_message(f"Error saving secret key to {secret_key_file}: {e}", "HYBRID CRYPTOGRAPHY", "ERROR")
                raise
            
            log_message(f"Hybrid-encrypted {input_file} to {output_file} using .qvault format", "HYBRID CRYPTOGRAPHY", "SUCCESS")
            log_message(f"Secret key saved separately to {secret_key_file}", "HYBRID CRYPTOGRAPHY", "INFO")
        else:

            with open(output_file, 'wb') as out:
                out.write(ciphertext)
            with open(output_file + ".iv", 'wb') as iv_file:
                iv_file.write(iv)
            with open(output_file + ".kem", 'wb') as kem_file:
                kem_file.write(kem_ciphertext)
            with open(output_file + ".pub", 'wb') as pub_file:
                pub_file.write(public_key)
            with open(output_file + ".sec", 'wb') as sec_file:
                sec_file.write(secret_key)
            log_message(f"Hybrid-encrypted {input_file} using Kyber KEM (legacy format)", "HYBRID CRYPTOGRAPHY", "SUCCESS")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        log_message(f"File not found during encryption: {e}", "HYBRID CRYPTOGRAPHY", "ERROR")
    except Exception as e:
        print(f"Hybrid encryption failed: {e}")
        log_message(f"Hybrid encryption error: {e}", "HYBRID CRYPTOGRAPHY", "ERROR")

def decrypt_hybrid(input_file, output_file, sec_key_path, kem_cipher_path, iv_path):
    try:
        with open(sec_key_path, 'rb') as f:
            secret_key = f.read()
        with open(kem_cipher_path, 'rb') as f:
            kem_ciphertext = f.read()
        with open(iv_path, 'rb') as f:
            iv = f.read()
        with open(input_file, 'rb') as f:
            ciphertext = f.read()

        shared_secret = kem_decrypt(secret_key, kem_ciphertext)
        aes_key = shared_secret[:32]

        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext))

        with open(output_file, 'wb') as f:
            f.write(plaintext)

        log_message(f"Hybrid-decrypted {input_file} to {output_file}", "HYBRID CRYPTOGRAPHY", "SUCCESS")

    except Exception as e:
        print(f"Hybrid decryption failed: {e}")
        log_message(f"Hybrid decryption error: {e}", "HYBRID CRYPTOGRAPHY", "ERROR")

def decrypt_hybrid_qvault(input_file, output_file, secret_key_file=None):
    try:
        encrypted_data, iv, kem_ciphertext, public_key, original_extension = QVaultFormat.unpack_qvault(input_file)
    
        if secret_key_file is None:
            secret_key_file = input_file.replace('.qvault', '.key')
        
        if not os.path.exists(secret_key_file):
            log_message(f"Secret key file not found: {secret_key_file}", "HYBRID CRYPTOGRAPHY", "ERROR")
            raise FileNotFoundError(f"Secret key file not found: {secret_key_file}")
        
        try:
            with open(secret_key_file, 'rb') as f:
                secret_key = f.read()
            log_message(f"Successfully loaded secret key from: {secret_key_file}", "HYBRID CRYPTOGRAPHY", "INFO")
        except IOError as e:
            log_message(f"Error reading secret key from {secret_key_file}: {e}", "HYBRID CRYPTOGRAPHY", "ERROR")
            raise
        
        shared_secret = kem_decrypt(secret_key, kem_ciphertext)
        aes_key = shared_secret[:32]

        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(encrypted_data))

        if not os.path.splitext(output_file)[1] and original_extension:
            output_file = output_file + original_extension

        with open(output_file, 'wb') as f:
            f.write(plaintext)

        log_message(f"Hybrid-decrypted {input_file} to {output_file} using .qvault format", "HYBRID CRYPTOGRAPHY", "SUCCESS")

    except FileNotFoundError as e:
        print(f" Secret key file not found: {e}")
        log_message(f"Secret key file not found during decryption: {e}", "HYBRID CRYPTOGRAPHY", "ERROR")
    except Exception as e:
        print(f"Hybrid .qvault decryption failed: {e}")
        log_message(f"Hybrid .qvault decryption error: {e}", "HYBRID CRYPTOGRAPHY", "ERROR")