import sys


def main():
    
    valid_commands = {"exit", "echo", "type"}
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = input()
        user_input_list = user_input.lstrip().split()
        user_command = user_input_list[0] if len(user_input_list) > 0 else None
        user_args = user_input_list[1:] if len(user_input_list) > 1 else None
        if user_command is None:
            continue
        if user_command not in valid_commands:
            print(f"{user_command}: command not found")
            continue
        if user_command == "exit":
            break
        elif user_command == "echo":
            if user_args is None:
                print("")
                continue
            else:
                print(user_args[0])
                continue
        elif user_command == "type":
            if user_args:
                type_command = user_args[0]
                if type_command in valid_commands:
                    print(f"{type_command}: is a shell builtin")
                    continue
                else:
                    print(f"{type_command}: not found")
                    continue
        else:
            continue
        break
    return 0


if __name__ == "__main__":
    main()
