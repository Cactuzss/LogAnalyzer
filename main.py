import sys
from cli import Params
from api import get_packages

def main():
    try:
        params = Params(sys.argv)
    except (ValueError, IndexError) as e:
        print("-------")
        print("[Error] Specify repo name after -r")
        print("-------")
        exit()

    response = get_packages(params.repo)
    print(response[0].url)



if __name__ == "__main__":
    main()


