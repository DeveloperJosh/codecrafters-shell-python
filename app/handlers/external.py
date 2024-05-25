import os
import shutil

def handle_external_command(user_command, user_args, PATH):
    try:
        # Check if the command exists in the system PATH
        if shutil.which(user_command) is None:
            print(f"{user_command}: command not found")
        else:
            os.system(f"{user_command} {' '.join(user_args)}")
    except Exception as e:
        print(f"An error occurred: {e}")
