import os
import sys
from typing import Optional


def main():
    
    PATH = os.environ.get("PATH", None)
    
    valid_commands = {"exit", "echo", "type"}
    
    def path_value(cmd: str, path: str) -> Optional[str]:
        potential_paths = path.split(":")
        for potential_path in potential_paths:
            full_path: str = potential_path + "/" + cmd
            if os.path.exists(full_path):
                return full_path
        return None
    def get_type(cmd: str) -> None:
        found_path = path_value(cmd, PATH) if PATH else None
        if cmd in valid_commands:
            print(f"{cmd} is a shell builtin")
        elif found_path:
            print(f"{cmd} is {found_path}")
        else:
            print(f"{cmd}: not found")

    
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
            print(*user_args) if user_args else print("")
            continue
        elif user_command == "type":
            if user_args:
                for cmd in user_args:
                    get_type(cmd)
        else:
            continue
    return 0


if __name__ == "__main__":
    main()
