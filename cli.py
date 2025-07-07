import os

def initCli(args):
    # Encrypt function
    if args[0] == "-e" or args[0] == "--encrypt":
        try:
            file = args[1]
            password = args[2]
        except IndexError:
            print("Error: Invalid arguments. USAGE: -e <file> <password> or --encrypt <file> <password>")
            return
        if not os.path.exists(file):
            print("Error: File not found")
            return
        print(f"Encrypting {file} with password {password}")

    # Decriptition function
    elif args[0] == "-d" or args[0] == "--decrypt":
        try:
            file = args[1]
            password = args[2]
        except IndexError:
            print("Error: Invalid arguments. USAGE: -d <file> <password> or --decrypt <file> <password>")
            return
        if not os.path.exists(file):
            print("Error: File not found")
            return
        print(f"Decrypting {file} with password {password}")
    elif args[0] == "-h" or args[0] == "--help":
        print(commands())
    elif args[0] == "-v" or args[0] == "--version":
        print("Version 1.0.0")
    else:
        print(commands())

# Commands avaliable
def commands():
    return """
    List of commands:
    -e <file> <password> or --encrypt <file> <password>
    -d <file> <password> or --decrypt <file> <password>
    -h or --help
    -v or --version
    """

if __name__ == "__main__":
    initCli(sys.argv[1:])