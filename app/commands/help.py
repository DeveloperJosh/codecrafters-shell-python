# src/commands/help.py

class HelpCommand:
    def execute(self, args):
        help = """
        Built-in Commands:
        -----------------
        help: Shows this help message
        code: The in house code editor (BETA)
        echo: Prints the arguments to the standard output
        type: Prints the contents of a file
        sysinfo: Prints system information
        clear: Clears the screen
        ls: Lists files in the current directory
        pwd: Prints the current working directory
        kill: Kills a process by ID
        exit: Exits the shell
        cd: Changes the current directory
        cat: Prints the contents of a file
        ps: Lists all running processes
        """
        print(help)