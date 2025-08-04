import struct
import os
from typing import Tuple, Optional
from utils.logging import log_message

QV_MAGIC = b'QVLT'
QV_VERSION = 1

# Credits: João Pedro da Silva Ramalho, https://github.com/joaopramalho/quantumvault
# File format structure:
# [4 bytes] Magic bytes (QVLT)
# [1 byte]  Version (1)
# [1 byte]  Flags (reserved for future use)
# [2 bytes] Reserved (padding)
# [4 bytes] Header length (uint32)
# [4 bytes] Data length (uint32)
# [4 bytes] IV length (uint32)
# [4 bytes] KEM ciphertext length (uint32)
# [4 bytes] Public key length (uint32)
# [4 bytes] Original extension length (uint32)
# [header_length] Header data
# [ext_length] Original file extension
# [data_length] Encrypted data
# [iv_length] IV data
# [kem_length] KEM ciphertext
# [pub_length] Public key

class QVaultFormat:
    @staticmethod
    def create_header(
        data_length: int,
        iv_length: int,
        kem_length: int,
        pub_length: int,
        ext_length: int,
        flags: int = 0
    ) -> bytes:
        header_data = b''  # header
        header_length = len(header_data)
        
        header = struct.pack(
            '<4sBBHIIIIII',
            QV_MAGIC,           # 4 bytes
            QV_VERSION,         # 1 byte
            flags,              # 1 byte
            0,                  # 2 bytes
            header_length,      # 4 bytes
            data_length,        # 4 bytes
            iv_length,          # 4 bytes
            kem_length,         # 4 bytes
            pub_length,         # 4 bytes
            ext_length          # 4 bytes
        )
        
        return header + header_data
    
    @staticmethod
    def pack_qvault(
        encrypted_data: bytes,
        iv: bytes,
        kem_ciphertext: bytes,
        public_key: bytes,
        output_path: str,
        original_extension: str = ""
    ) -> bytes:
        if not original_extension and output_path.endswith('.qvault'):
            original_extension = ""
        
        ext_bytes = original_extension.encode('utf-8')
        
        header = QVaultFormat.create_header(
            len(encrypted_data),
            len(iv),
            len(kem_ciphertext),
            len(public_key),
            len(ext_bytes)
        )
        
        try:
            with open(output_path, 'wb') as f:
                f.write(header)
                f.write(ext_bytes)
                f.write(encrypted_data)
                f.write(iv)
                f.write(kem_ciphertext)
                f.write(public_key)
        except IOError as e:
            log_message(f"Error writing QVault file: {e}", "PACKING QVAULT FILE", "ERROR")
            raise
        
        return public_key
    
    @staticmethod
    def unpack_qvault(file_path: str) -> Tuple[bytes, bytes, bytes, bytes, str]:
        try:
            with open(file_path, 'rb') as f:
                magic = f.read(4)
                if magic != QV_MAGIC:
                    log_message("Invalid .qvault file: wrong magic bytes", "UNPACKING QVAULT FILE", "ERROR")
                    raise ValueError("Invalid .qvault file: wrong magic bytes") 
                
                version = struct.unpack('<B', f.read(1))[0]
                if version != QV_VERSION:
                    log_message(f"Unsupported .qvault version: {version}, use a older/newer version of QuantumVault, version not compatible", "UNPACKING QVAULT FILE", "ERROR")
                    raise ValueError(f"Unsupported .qvault version: {version}, use a older/newer version of QuantumVault, version not compatible")
                
                flags = struct.unpack('<B', f.read(1))[0]
                f.read(2)
                
                # lens
                header_len, data_len, iv_len, kem_len, pub_len, ext_len = struct.unpack('<IIIIII', f.read(24))
                
                f.read(header_len)
                
                # extensao
                ext_bytes = f.read(ext_len)
                original_extension = ext_bytes.decode('utf-8') if ext_bytes else ""
                
                # componentes
                encrypted_data = f.read(data_len)
                iv = f.read(iv_len)
                kem_ciphertext = f.read(kem_len)
                public_key = f.read(pub_len)
                
                log_message("Successfully unpacked .qvault file!", "UNPACKING QVAULT FILE", "SUCCESS")
                return encrypted_data, iv, kem_ciphertext, public_key, original_extension
        except FileNotFoundError as e:
            log_message(f"QVault file not found: {e}", "UNPACKING QVAULT FILE", "ERROR")
            raise
        except Exception as e:
            log_message(f"Error unpacking QVault file: {e}", "UNPACKING QVAULT FILE", "ERROR")
            raise
    
    @staticmethod
    def is_qvault_file(file_path: str) -> bool:
        try:
            with open(file_path, 'rb') as f:
                magic = f.read(4)
                if magic == QV_MAGIC:
                    log_message("File is a real QVault file! (correct magic bytes)", "VALID FILE CHECKER", "INFO")
                    return True
                else:
                    log_message("File is not a real QVault file!", "VALID FILE CHECKER", "ERROR")
                    return False
        except (IOError, OSError) as e:
            log_message(f"Error checking if file is QVault: {e}", "VALID FILE CHECKER", "ERROR")
            return False
    
    @staticmethod
    def get_qvault_info(file_path: str) -> Optional[dict]:
        try:
            with open(file_path, 'rb') as f:
                magic = f.read(4)
                if magic != QV_MAGIC:
                    log_message("File is not a real QVault file!", "QVAULT INFO PARSER", "ERROR")
                    return None
                
                version = struct.unpack('<B', f.read(1))[0] # retorna versao
                flags = struct.unpack('<B', f.read(1))[0] # retorna flags
                f.read(2)  # bits reservados
                
                header_len, data_len, iv_len, kem_len, pub_len, ext_len = struct.unpack('<IIIIII', f.read(24))
                
                # extensao original
                f.read(header_len)  # pular header de data
                ext_bytes = f.read(ext_len)
                original_extension = ext_bytes.decode('utf-8') if ext_bytes else ""

                log_message("Successfully parsed QVault file info!", "QVAULT INFO PARSER", "SUCCESS")
                
                return {
                    'version': version,
                    'flags': flags,
                    'data_size': data_len,
                    'iv_size': iv_len,
                    'kem_size': kem_len,
                    'pub_key_size': pub_len,
                    'ext_size': ext_len,
                    'original_extension': original_extension,
                    'total_size': os.path.getsize(file_path)
                }
        except FileNotFoundError as e:
            log_message(f"QVault file not found: {e}", "QVAULT INFO PARSER", "ERROR")
            return None
        except (IOError, OSError, struct.error) as e:
            log_message(f"Error parsing QVault file info: {e}", "QVAULT INFO PARSER", "ERROR")
            return None
