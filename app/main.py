import os
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from utils.exec import execute_command  # Import the execute_command function

def main():
    current_dir = os.getcwd()

    # If the current directory is the root directory (unlikely), change to the user's home directory
    if current_dir == os.path.sep:
        os.chdir(os.path.expanduser('~'))
    else:
        os.chdir(current_dir)
    
    history = InMemoryHistory()

    while True:
        try:
            user_input = prompt(HTML(f'<ansigreen>(Shell)</ansigreen> {os.getcwd()} $ '), history=history).strip().split()
        except EOFError:
            break
        except KeyboardInterrupt:
            # show ^C on the console
            print("^C")
            continue

        if not user_input:
            continue
        
        user_command, *user_args = user_input
        execute_command(user_command, user_args)

if __name__ == "__main__":
    main()
