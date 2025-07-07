from gui import initGui
from cli import initCli
import sys

def main():
    # Check if is gui or cli
    if len(sys.argv) > 1:
        initCli(sys.argv[1:])
    else:
        initGui()

if __name__ == "__main__":
    main()
