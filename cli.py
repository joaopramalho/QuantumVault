import os
import sys
from utils.logging import log_message
from utils.cryptography import encrypt_hybrid, decrypt_hybrid_qvault
from utils.qvaults import QVaultFormat

def initCli(args):
    if args[0] == "-e" or args[0] == "--encrypt":
        try:
            input_file = args[1]
            output_file = args[2]

        except IndexError:
            print("Invalid arguments. USAGE: -e <input_file> <output_file> or --encrypt <input_file> <output_file>")
            log_message("Invalid arguments for encryption command", "CLI ENCRYPT", "ERROR")

            return
        if not os.path.exists(input_file):
            print("Input file not found")
            log_message(f"Input file not found for encryption: {input_file}", "CLI ENCRYPT", "ERROR")

            return
        
        if not output_file.endswith('.qvault'):
            output_file += '.qvault'
        
        print(f"Encrypting {input_file} to {output_file}")

        encrypt_hybrid(input_file, output_file)

    elif args[0] == "-d" or args[0] == "--decrypt":
        try:
            input_file = args[1]

            output_file = args[2]

        except IndexError:
            print("Error: Invalid arguments. USAGE: -d <input_file> <output_file> or --decrypt <input_file> <output_file>")
            log_message("Invalid arguments for decryption command", "CLI DECRYPT", "ERROR")

            return
        if not os.path.exists(input_file):
            print("Input file not found")

            log_message(f"Input file not found for decryption: {input_file}", "CLI DECRYPT", "ERROR")
            return

        if input_file.endswith('.qvault') or QVaultFormat.is_qvault_file(input_file):
            print(f"Decrypting {input_file} to {output_file}")
            
            secret_key_file = input_file.replace('.qvault', '.key')
            if not os.path.exists(secret_key_file):
                print(f"Secret key file not found: {secret_key_file}")
                print("The key file is not in the same folder as the qvault fiel")
                log_message(f"Secret key file not found: {secret_key_file}", "CLI DECRYPT", "ERROR")
                return
            
            decrypt_hybrid_qvault(input_file, output_file, secret_key_file)
        else:
            print("Input file is not a .qvault file")
            print("Try to use legacy decryption for separate files")
            log_message(f"Input file is not a valid .qvault file: {input_file}", "CLI DECRYPT", "ERROR")
    
    elif args[0] == "-i" or args[0] == "--info":
        try:
            file_path = args[1]
        except IndexError:
            print("Invalid arguments. USAGE: -i <file> or --info <file>")

            log_message("Invalid arguments for info command", "CLI INFO", "ERROR")
            return
        
        if not os.path.exists(file_path):
            print("File not found")
            log_message(f"File not found for : {file_path}", "CLI INFO", "ERROR")
            return
        
        if QVaultFormat.is_qvault_file(file_path):
            info = QVaultFormat.get_qvault_info(file_path)
            if info:
                print(f"File Information:")
                print(f"Version: {info['version']}")
                print(f"Flags: {info['flags']}")
                print(f"Original Extension: {info['original_extension'] or '(none)'}")
                print(f"Data Size: {info['data_size']} bytes")
                print(f"IV Size: {info['iv_size']} bytes")
                print(f"KEM Size: {info['kem_size']} bytes")
                print(f"Public Key Size: {info['pub_key_size']} bytes")
                print(f"Extension Size: {info['ext_size']} bytes")
                print(f"Total Size: {info['total_size']} bytes")
            else:
                print("Could not read .qvault file information")
        else:
            print("File is not a valid .qvault file")
            log_message(f"File is not a valid .qvault file: {file_path}", "CLI INFO", "ERROR")
    
    elif args[0] == "-h" or args[0] == "--help":

        print(commands())
    elif args[0] == "-v" or args[0] == "--version":

        print("Version 1.0.0")
    else:

        print(commands())

def commands():
    return """
    List of commands:
    -e <input_file> <output_file> or --encrypt <input_file> <output_file>
        Encrypt a file to .qvault format
    
    -d <input_file> <output_file> or --decrypt <input_file> <output_file>
        Decrypt a .qvault file to plain text
    
    -i <file> or --info <file>
        Show information about a .qvault file
    
    -h or --help
        Show this help message
    
    -v or --version
        Show version information
    """

if __name__ == "__main__":
    initCli(sys.argv[1:])