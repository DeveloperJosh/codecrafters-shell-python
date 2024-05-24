import sys


def main():
    
    valid_commands = {"exit"}
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = input()
        user_input_list = user_input.split(" ", 1)
        user_command = user_input_list[0] if len(user_input_list) > 0 else None
        user_args = user_input_list[1:] if len(user_input_list) > 1 else None
        if user_command is None:
            continue
        if user_command not in valid_commands:
            print(f"{user_command}: command not found")
            continue
        if user_command == "exit":
            break
        break
    return 0


if __name__ == "__main__":
    main()
