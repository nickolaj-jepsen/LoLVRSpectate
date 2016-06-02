import os
import sys


def is_excluded():
    file_name = os.path.basename(sys.argv[0])

    path = os.path.dirname(os.getenv("APPDATA"))  # get path to APPDATA
    path += "\\Local\\Animation Labs\\vorpX\\vorpControl.ini"
    with open(path, mode="r") as f:
        return file_name in f.read()


if __name__ == '__main__':
    is_excluded()