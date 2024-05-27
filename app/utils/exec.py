import os
import shutil
from commands.init import get_command

def execute_command(command_name, args):
    command = get_command(command_name)
    if command:
        command.execute(args)
    else:
        handle_external_command(command_name, args)

def handle_external_command(user_command, user_args):
    try:
        # Check if the command exists in the system PATH
        if shutil.which(user_command) is None:
            print(f"{user_command}: command not found")
        else:
            command_str = f"{user_command} {' '.join(user_args)}"
            print(f"Executing external command: {command_str}")
            os.system(command_str)
    except Exception as e:
        print(f"An error occurred: {e}")
