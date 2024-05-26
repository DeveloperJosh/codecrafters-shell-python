import os
from rlcompleter import Completer
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from handlers.builtins import handle_builtin_command
from handlers.external import handle_external_command
from utils.path_utils import shell_builtins

def main():
    PATH = os.environ.get("PATH", "")
    history = InMemoryHistory()

    while True:
        try:
        ##user_input = prompt(HTML(f'<ansigreen>{os.getcwd()} $ </ansigreen>'), history=history).strip().split()
         # (shell) PS E:\py-shell>
         user_input = prompt(HTML(f'<ansigreen>(Shell)</ansigreen> {os.getcwd()} $ '), history=history, ).strip().split()
        except EOFError:
            break
        if not user_input:
            continue
        user_command, *user_args = user_input

        if user_command in shell_builtins:
            handle_builtin_command(user_command, user_args)
        else:
            handle_external_command(user_command, user_args, PATH)

if __name__ == "__main__":
    main()
