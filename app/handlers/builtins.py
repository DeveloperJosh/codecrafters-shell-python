import os
import sys
from utils.system_info import get_cpu_name, get_size
from datetime import datetime
import platform
import psutil
from utils.path_utils import get_type
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML

def handle_builtin_command(user_command: str, user_args: list) -> None:
    try:
        commands = {
            "exit": sys.exit,
            "echo": lambda: print(" ".join(user_args)),
            "type": lambda: [get_type(cmd) for cmd in user_args],
            "cd": lambda: change_directory(user_args),
            "ls": lambda: list_directory(user_args),
            "clear": lambda: os.system("cls" if os.name == "nt" else "clear"),
            "help": show_help,
            "sysinfo": show_sysinfo,
            "pwd": lambda: print(os.getcwd()),
            "cat": lambda: [print_file_content(file) for file in user_args],
            "mkdir": lambda: [make_directory(dir) for dir in user_args],
            "rmdir": lambda: [remove_directory(dir) for dir in user_args],
            "mv": lambda: move_file(user_args),
            "cp": lambda: copy_file(user_args),
            "touch": lambda: [touch_file(file) for file in user_args],
            "head": lambda: [print_head(file) for file in user_args],
            "tail": lambda: [print_tail(file) for file in user_args],
            "grep": lambda: grep_pattern(user_args),
            "wc": lambda: [word_count(file) for file in user_args],
            "sort": lambda: [sort_file(file) for file in user_args],
            "uniq": lambda: [unique_lines(file) for file in user_args],
            "uptime": show_uptime,
            "ps": show_processes,
            "kill": lambda: [kill_process(pid) for pid in user_args],
            "free": show_memory,
            "whoami": lambda: print(os.getlogin()),
        }
        commands.get(user_command, lambda: print(f"{user_command}: command not found"))()
    except Exception as e:
        print(f"An error occurred: {e}")

def change_directory(args):
    target_directory = args[0] if args else os.path.expanduser("~")
    try:
        os.chdir(target_directory)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"cd: {e}")

def list_directory(args):
    targets = args if args else ["."]
    for arg in targets:
        try:
            for file in os.listdir(arg):
                print(file)
        except FileNotFoundError:
            print(f"ls: cannot access '{arg}': No such file or directory")

def show_help():
    print_formatted_text(HTML('<ansiyellow>Available Commands</ansiyellow>\n\n'))
    commands = {
        "exit": "Exit the shell",
        "echo": "Print arguments to the standard output",
        "type": "Display information about command type",
        "cd": "Change the shell working directory",
        "ls": "List directory contents",
        "clear": "Clear the terminal screen",
        "help": "Display information about builtin commands",
        "sysinfo": "Display system information",
        "pwd": "Print the current working directory",
        "cat": "Concatenate files and print on the standard output",
        "mkdir": "Create directories",
        "rmdir": "Remove directories",
        "mv": "Move files",
        "cp": "Copy files",
        "touch": "Create empty files",
        "head": "Output the first part of files",
        "tail": "Output the last part of files",
        "grep": "Print lines matching a pattern",
        "wc": "Print newline, word, and byte counts for each file",
        "sort": "Sort lines of text files",
        "uniq": "Report or omit repeated lines",
        "uptime": "Tell how long the system has been running",
        "ps": "Report a snapshot of the current processes",
        "kill": "Send signals to processes",
        "free": "Display amount of free and used memory in the system",
        "whoami": "Print the effective user ID",
    }
    for cmd, desc in commands.items():
        print(f"{cmd}: {desc}")

def show_sysinfo():
    print_formatted_text(HTML('<ansiyellow>System Information</ansiyellow>\n\nPlease Hold\n'))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = platform.uname()
    cpu_name = get_cpu_name()
    cpu_usage = psutil.cpu_percent(interval=1)
    svmem = psutil.virtual_memory()

    print_formatted_text(HTML(f'<ansigreen>Current Time:</ansigreen> {current_time}'))
    print_formatted_text(HTML(f'<ansigreen>OS:</ansigreen> {os_info.system} {os_info.release} {os_info.version}'))
    print_formatted_text(HTML(f'<ansigreen>CPU:</ansigreen> {cpu_name}'))
    print_formatted_text(HTML(f'<ansigreen>CPU Cores:</ansigreen> {psutil.cpu_count(logical=False)}'))
    print_formatted_text(HTML(f'<ansigreen>CPU Usage:</ansigreen> {cpu_usage}%'))
    print_formatted_text(HTML(f'<ansigreen>RAM:</ansigreen> {get_size(svmem.total)}'))
    print_formatted_text(HTML(f'<ansigreen>Memory Used:</ansigreen> {get_size(svmem.used)} / {get_size(svmem.total)}'))

def print_file_content(file):
    try:
        with open(file, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"cat: {file}: No such file or directory")

def make_directory(directory):
    try:
        os.mkdir(directory)
    except FileExistsError:
        print(f"mkdir: cannot create directory '{directory}': File exists")

def remove_directory(directory):
    try:
        os.rmdir(directory)
    except FileNotFoundError:
        print(f"rmdir: failed to remove '{directory}': No such file or directory")

def move_file(args):
    if len(args) != 2:
        print("mv: missing file operand")
    else:
        src, dest = args
        try:
            os.rename(src, dest)
        except FileNotFoundError:
            print(f"mv: cannot move '{src}': No such file or directory")

def copy_file(args):
    if len(args) != 2:
        print("cp: missing file operand")
    else:
        src, dest = args
        try:
            with open(src, "rb") as f:
                with open(dest, "wb") as new_f:
                    new_f.write(f.read())
        except FileNotFoundError:
            print(f"cp: cannot copy '{src}': No such file or directory")

def touch_file(file):
    with open(file, "w"):
        pass

def print_head(file):
    try:
        with open(file, "r") as f:
            for _ in range(10):
                print(f.readline().strip())
    except FileNotFoundError:
        print(f"head: cannot open '{file}' for reading: No such file or directory")

def print_tail(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(line.strip())
    except FileNotFoundError:
        print(f"tail: cannot open '{file}' for reading: No such file or directory")

def grep_pattern(args):
    if not args:
        print("grep: missing search pattern")
    search_pattern = args[0]
    for file in args[1:]:
        try:
            with open(file, "r") as f:
                for line in f:
                    if search_pattern in line:
                        print(line.strip())
        except FileNotFoundError:
            print(f"grep: {file}: No such file or directory")

def word_count(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            print(f"{len(lines)} {file}")
    except FileNotFoundError:
        print(f"wc: {file}: No such file or directory")

def sort_file(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in sorted(lines):
                print(line.strip())
    except FileNotFoundError:
        print(f"sort: {file}: No such file or directory")

def unique_lines(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in set(lines):
                print(line.strip())
    except FileNotFoundError:
        print(f"uniq: {file}: No such file or directory")

def show_uptime():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    print(f"up {uptime}")

def show_processes():
    for process in psutil.process_iter(['pid', 'name', 'username']):
        print(f"{process.info['pid']} {process.info['name']} {process.info['username']}")

def kill_process(pid):
    try:
        os.kill(int(pid), 9)
    except ProcessLookupError:
        print(f"kill: {pid}: No such process")

def show_memory():
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Free: {get_size(svmem.free)}")
