import os

def get_type(cmd):
    if cmd in shell_builtins:
        print(f"{cmd} is a shell builtin")
    elif os.path.isfile(cmd):
        print(f"{cmd} is a file")
    else:
        print(f"{cmd} not found")

shell_builtins = {
    "exit", "echo", "type", "cd", "ls", "clear", "help", "sysinfo",
    "pwd", "cat", "mkdir", "rmdir", "mv", "cp", "touch", "head",
    "tail", "grep", "wc", "sort", "uniq", "uptime", "ps", "kill", "free", "whoami"
}
