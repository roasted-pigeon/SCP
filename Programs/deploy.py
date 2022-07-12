import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "SCPLib":
            from SCPLib import main
