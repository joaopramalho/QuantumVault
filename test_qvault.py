#!/usr/bin/env python3
"""
Test script for .qvault file format
"""

import os
import tempfile
from utils.cryptography import encrypt_hybrid, decrypt_hybrid_qvault
from utils.qvaults import QVaultFormat
from utils.logging import log_message

def test_qvault_format():
    """Test the .qvault file format"""
    print("Testing .qvault file format...")
    
    # Create a temporary test file with extension
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        test_content = "This is a test file for .qvault format.\nIt contains multiple lines.\nAnd some special characters: !@#$%^&*()"
        f.write(test_content)
        test_file = f.name
    
    # Create another test file with different extension
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        md_content = "# Test Markdown File\n\nThis is a **markdown** file with `code` and *formatting*."
        f.write(md_content)
        md_file = f.name
    
    try:
        # Test encryption to .qvault format
        print(f"1. Creating test file: {test_file}")
        print(f"   Content: {repr(test_content)}")
        
        # Encrypt to .qvault format
        qvault_file = test_file.replace('.txt', '.qvault')
        print(f"2. Encrypting to: {qvault_file}")
        encrypt_hybrid(test_file, qvault_file)
        
        # Check if .qvault file was created
        if os.path.exists(qvault_file):
            print(f"   ✓ .qvault file created successfully")
            
            # Test file info
            info = QVaultFormat.get_qvault_info(qvault_file)
            if info:
                print(f"   ✓ File info retrieved:")
                print(f"     - Version: {info['version']}")
                print(f"     - Data Size: {info['data_size']} bytes")
                print(f"     - Total Size: {info['total_size']} bytes")
            else:
                print("   ✗ Could not read file info")
                return False
        else:
            print("   ✗ .qvault file was not created")
            return False
        
        # Test decryption with automatic extension
        decrypted_file = test_file.replace('.txt', '_decrypted')  # No extension
        print(f"3. Decrypting to: {decrypted_file} (should auto-add .txt)")
        
        # Check if secret key file exists
        secret_key_file = qvault_file.replace('.qvault', '.key')
        if not os.path.exists(secret_key_file):
            print(f"   ✗ Secret key file not found: {secret_key_file}")
            return False
        
        decrypt_hybrid_qvault(qvault_file, decrypted_file, secret_key_file)
        
        # Verify decryption
        expected_decrypted_file = decrypted_file + '.txt'
        if os.path.exists(expected_decrypted_file):
            with open(expected_decrypted_file, 'r') as f:
                decrypted_content = f.read()
            
            if decrypted_content == test_content:
                print(f"   ✓ Decryption successful with auto-extension")
                print(f"   ✓ Content matches: {repr(decrypted_content)}")
            else:
                print(f"   ✗ Content mismatch!")
                print(f"     Original: {repr(test_content)}")
                print(f"     Decrypted: {repr(decrypted_content)}")
                return False
        else:
            print("   ✗ Decrypted file was not created")
            return False
        
        # Test markdown file encryption/decryption
        print(f"4. Testing markdown file encryption...")
        md_qvault_file = md_file.replace('.md', '.qvault')
        encrypt_hybrid(md_file, md_qvault_file)
        
        if os.path.exists(md_qvault_file):
            print(f"   ✓ Markdown .qvault file created")
            
            # Test decryption with .md extension
            md_decrypted_file = md_file.replace('.md', '_decrypted')
            
            # Check if secret key file exists
            md_secret_key_file = md_qvault_file.replace('.qvault', '.key')
            if not os.path.exists(md_secret_key_file):
                print(f"   ✗ Secret key file not found: {md_secret_key_file}")
                return False
            
            decrypt_hybrid_qvault(md_qvault_file, md_decrypted_file, md_secret_key_file)
            
            expected_md_file = md_decrypted_file + '.md'
            if os.path.exists(expected_md_file):
                with open(expected_md_file, 'r') as f:
                    md_decrypted_content = f.read()
                
                if md_decrypted_content == md_content:
                    print(f"   ✓ Markdown decryption successful with auto-extension")
                else:
                    print(f"   ✗ Markdown content mismatch!")
                    return False
            else:
                print("   ✗ Markdown decrypted file was not created")
                return False
        else:
            print("   ✗ Markdown .qvault file was not created")
            return False
        
        print("✓ All tests passed! .qvault format with extension preservation is working correctly.")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return False
    
    finally:
        # Cleanup
        files_to_clean = [test_file, md_file]
        if 'qvault_file' in locals() and os.path.exists(qvault_file):
            files_to_clean.append(qvault_file)
        if 'decrypted_file' in locals() and os.path.exists(decrypted_file):
            files_to_clean.append(decrypted_file)
        if 'expected_decrypted_file' in locals() and os.path.exists(expected_decrypted_file):
            files_to_clean.append(expected_decrypted_file)
        if 'md_qvault_file' in locals() and os.path.exists(md_qvault_file):
            files_to_clean.append(md_qvault_file)
        if 'md_decrypted_file' in locals() and os.path.exists(md_decrypted_file):
            files_to_clean.append(md_decrypted_file)
        if 'expected_md_file' in locals() and os.path.exists(expected_md_file):
            files_to_clean.append(expected_md_file)
        if 'secret_key_file' in locals() and os.path.exists(secret_key_file):
            files_to_clean.append(secret_key_file)
        if 'md_secret_key_file' in locals() and os.path.exists(md_secret_key_file):
            files_to_clean.append(md_secret_key_file)
        
        for file in files_to_clean:
            if os.path.exists(file):
                os.unlink(file)
                print(f"   Cleaned up: {file}")

if __name__ == "__main__":
    test_qvault_format() 