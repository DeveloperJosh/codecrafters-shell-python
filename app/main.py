import sys


def main():
    print("Logs from your program will appear here!")

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        input()


if __name__ == "__main__":
    main()
