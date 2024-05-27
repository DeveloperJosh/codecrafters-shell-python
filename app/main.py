import os
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from utils.exec import execute_command  # Import the execute_command function

def main():
    history = InMemoryHistory()

    while True:
        try:
            user_input = prompt(HTML(f'<ansigreen>(Shell)</ansigreen> {os.getcwd()} $ '), history=history).strip().split()
        except EOFError:
            break

        if not user_input:
            continue
        
        user_command, *user_args = user_input
        execute_command(user_command, user_args)

if __name__ == "__main__":
    main()
