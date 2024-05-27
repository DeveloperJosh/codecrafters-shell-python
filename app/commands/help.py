# src/commands/help.py

class HelpCommand:
    def execute(self, args):
        print("Available commands:")
        print("cd <path>: Change the current working directory")
        print("echo <text>: Print text to the console")
        print("type <filename>: Print the contents of a file")
        print("sysinfo: Print system information")
        print("help: Print this help message")
        print("clear: Clear the console screen")
        print("ls: List files and directories")
        print("pwd: Print the current working directory")
        print("kill <pid>: Kill a process by ID")
        print("exit: Exit the shell")