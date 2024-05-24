import sys


def main():
    
    vaild_commands = {}
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_commands = input()
        if user_commands not in vaild_commands:
            print(f"Command {user_commands} not found")


if __name__ == "__main__":
    main()
