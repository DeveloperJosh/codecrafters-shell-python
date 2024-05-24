import os
import sys
from typing import Optional

def main():
    PATH = os.environ.get("PATH", None)
    shell_builtins = {"exit", "echo", "type"}

    def path_value(cmd: str, path: str) -> Optional[str]:
        potential_paths = path.split(":")
        for potential_path in potential_paths:
            full_path: str = os.path.join(potential_path, cmd)
            if os.path.exists(full_path):
                return full_path
        return None

    def get_type(cmd: str) -> None:
        found_path = path_value(cmd, PATH) if PATH else None
        if cmd in shell_builtins:
            print(f"{cmd} is a shell builtin")
        elif found_path:
            print(f"{cmd} is {found_path}")
        else:
            print(f"{cmd}: not found")
            
    def is_executable(cmd: str) -> bool:
        if os.path.exists(cmd):
            return True
        if PATH and path_value(cmd, PATH):
            return True
        return False

    while True:
        user_input = input("$ ").strip().split()
        if not user_input:
            continue
        user_command, *user_args = user_input

        if user_command in shell_builtins:
            if user_command == "exit":
                break
            elif user_command == "echo":
                print(*user_args)
            elif user_command == "type":
                for cmd in user_args:
                    get_type(cmd)
        elif is_executable(user_command):
            cmd = (
                user_command + " " + " ".join(a for a in user_args)
                if user_args
                else user_command
            )
            os.system(cmd)
        else:
            found_path = path_value(user_command, PATH)
            if found_path:
                os.execv(found_path, [user_command] + user_args)
            else:
                print(f"{user_command}: not found")

if __name__ == "__main__":
    main()