import sys
from cli import Params
from api import get_packages, get_log

def main():
    try:
        params = Params(sys.argv)
    except (ValueError, IndexError) as e:
        print("-------")
        print("[Error] Specify repo name after -r")
        print("-------")
        exit()

    response = get_packages(params.repo)


if __name__ == "__main__":
    main()


