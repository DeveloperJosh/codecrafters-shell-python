import os
import re
import sys
from utils.system_info import get_cpu_name, get_size
from datetime import datetime
import platform
import psutil
from utils.path_utils import get_type
from prompt_toolkit import print_formatted_text, PromptSession
from prompt_toolkit.formatted_text import HTML
import glob
import stat
import time
import concurrent.futures

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
    if not args:
        os.chdir(os.path.expanduser("~"))
    else:
        new_dir = args[0]
        try:
            os.chdir(new_dir)
        except FileNotFoundError:
            print(f"cd: {new_dir}: No such file or directory")
        except PermissionError:
            print(f"cd: {new_dir}: Permission denied")
        except Exception as e:
            print(f"cd: An error occurred: {e}")

def get_mode(file_stat):
    is_dir = 'd' if stat.S_ISDIR(file_stat.st_mode) else '-'
    owner_perm = 'r' if file_stat.st_mode & stat.S_IRUSR else '-'
    owner_perm += 'w' if file_stat.st_mode & stat.S_IWUSR else '-'
    owner_perm += 'x' if file_stat.st_mode & stat.S_IXUSR else '-'
    group_perm = 'r' if file_stat.st_mode & stat.S_IRGRP else '-'
    group_perm += 'w' if file_stat.st_mode & stat.S_IWGRP else '-'
    group_perm += 'x' if file_stat.st_mode & stat.S_IXGRP else '-'
    other_perm = 'r' if file_stat.st_mode & stat.S_IROTH else '-'
    other_perm += 'w' if file_stat.st_mode & stat.S_IWOTH else '-'
    other_perm += 'x' if file_stat.st_mode & stat.S_IXOTH else '-'
    return f'{is_dir}{owner_perm}{group_perm}{other_perm}'

def format_time(epoch_time):
    return time.strftime('%Y-%m-%d %I:%M %p', time.localtime(epoch_time))

def list_directory(args):
    targets = args if args else ["."]
    exclude_patterns = [
        re.compile(r'^NTUSER\.DAT'),
        re.compile(r'^ntuser\.dat\.LOG\d+'),
        re.compile(r'^NTUSER\.DAT\{[a-f0-9-]+\}\.TM\.blf$'),
        re.compile(r'^NTUSER\.DAT\{[a-f0-9-]+\}\.TMContainer\d+\.regtrans-ms$'),
        re.compile(r'^ntuser\.ini$')
    ]

    for target in targets:
        try:
            pattern = os.path.join(target, '*')  # Matches all files except hidden ones
            files = glob.glob(pattern)
            print(f"Directory: {os.path.abspath(target)}")
            print("Mode                 LastWriteTime         Length Name")
            print("----                 -------------         ------ ----")
            for file in files:
                base_name = os.path.basename(file)
                if not base_name.startswith(".") and not any(pat.match(base_name) for pat in exclude_patterns):
                    try:
                        file_stat = os.stat(file)
                        mode = get_mode(file_stat)
                        last_write_time = format_time(file_stat.st_mtime)
                        length = file_stat.st_size if not stat.S_ISDIR(file_stat.st_mode) else ''
                        print(f'{mode:<20} {last_write_time:<20} {length:<6} {base_name}')
                    except FileNotFoundError:
                        print(f"ls: cannot access '{file}': No such file or directory")
                    except PermissionError:
                        print(f"ls: cannot access '{file}': Permission denied")
        except FileNotFoundError:
            print(f"ls: cannot access '{target}': No such file or directory")
        except PermissionError:
            print(f"ls: cannot access '{target}': Permission denied")

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
        
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_info():
    return psutil.virtual_memory()

def show_sysinfo():
    try:
        print_formatted_text(HTML('<ansiyellow>System Information</ansiyellow>\n\nPlease Hold\n'))
        
        # Start concurrent tasks
        with concurrent.futures.ThreadPoolExecutor() as executor:
            cpu_usage_future = executor.submit(get_cpu_usage)
            memory_info_future = executor.submit(get_memory_info)
            
            # Main thread retrieves other information
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os_info = platform.uname()
            cpu_name = get_cpu_name()
            cpu_cores = psutil.cpu_count(logical=False)
        
            # Wait for concurrent tasks to complete
            cpu_usage = cpu_usage_future.result()
            svmem = memory_info_future.result()

        # Print system information
        print_formatted_text(HTML(f'<ansigreen>Current Time:</ansigreen> {current_time}'))
        print_formatted_text(HTML(f'<ansigreen>OS:</ansigreen> {os_info.system} {os_info.release} {os_info.version}'))
        print_formatted_text(HTML(f'<ansigreen>CPU:</ansigreen> {cpu_name}'))
        print_formatted_text(HTML(f'<ansigreen>CPU Cores:</ansigreen> {cpu_cores}'))
        print_formatted_text(HTML(f'<ansigreen>CPU Usage:</ansigreen> {cpu_usage}%'))
        print_formatted_text(HTML(f'<ansigreen>RAM:</ansigreen> {get_size(svmem.total)}'))
        print_formatted_text(HTML(f'<ansigreen>Memory Used:</ansigreen> {get_size(svmem.used)} / {get_size(svmem.total)}'))
    except Exception as e:
        print(f"sysinfo: An error occurred: {e}")

def print_file_content(file):
    try:
        with open(file, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"cat: {file}: No such file or directory")
    except PermissionError:
        print(f"cat: {file}: Permission denied")
    except Exception as e:
        print(f"cat: An error occurred: {e}")

def make_directory(directory):
    try:
        os.mkdir(directory)
    except FileExistsError:
        print(f"mkdir: cannot create directory '{directory}': File exists")
    except PermissionError:
        print(f"mkdir: cannot create directory '{directory}': Permission denied")
    except Exception as e:
        print(f"mkdir: An error occurred: {e}")

def remove_directory(directory):
    try:
        os.rmdir(directory)
    except FileNotFoundError:
        print(f"rmdir: failed to remove '{directory}': No such file or directory")
    except PermissionError:
        print(f"rmdir: failed to remove '{directory}': Permission denied")
    except OSError:
        print(f"rmdir: failed to remove '{directory}': Directory not empty")
    except Exception as e:
        print(f"rmdir: An error occurred: {e}")

def move_file(args):
    if len(args) != 2:
        print("mv: missing file operand")
    else:
        src, dest = args
        try:
            os.rename(src, dest)
        except FileNotFoundError:
            print(f"mv: cannot move '{src}': No such file or directory")
        except PermissionError:
            print(f"mv: cannot move '{src}': Permission denied")
        except Exception as e:
            print(f"mv: An error occurred: {e}")

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
        except PermissionError:
            print(f"cp: cannot copy '{src}': Permission denied")
        except Exception as e:
            print(f"cp: An error occurred: {e}")

def touch_file(file):
    try:
        with open(file, "w"):
            pass
    except PermissionError:
        print(f"touch: cannot touch '{file}': Permission denied")
    except Exception as e:
        print(f"touch: An error occurred: {e}")

def print_head(file):
    try:
        with open(file, "r") as f:
            for _ in range(10):
                print(f.readline().strip())
    except FileNotFoundError:
        print(f"head: cannot open '{file}' for reading: No such file or directory")
    except PermissionError:
        print(f"head: cannot open '{file}' for reading: Permission denied")
    except Exception as e:
        print(f"head: An error occurred: {e}")

def print_tail(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(line.strip())
    except FileNotFoundError:
        print(f"tail: cannot open '{file}' for reading: No such file or directory")
    except PermissionError:
        print(f"tail: cannot open '{file}' for reading: Permission denied")
    except Exception as e:
        print(f"tail: An error occurred: {e}")

def grep_pattern(args):
    if not args:
        print("grep: missing search pattern")
        return
    search_pattern = args[0]
    for file in args[1:]:
        try:
            with open(file, "r") as f:
                for line in f:
                    if search_pattern in line:
                        print(line.strip())
        except FileNotFoundError:
            print(f"grep: {file}: No such file or directory")
        except PermissionError:
            print(f"grep: {file}: Permission denied")
        except Exception as e:
            print(f"grep: An error occurred: {e}")

def word_count(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            print(f"{len(lines)} {file}")
    except FileNotFoundError:
        print(f"wc: {file}: No such file or directory")
    except PermissionError:
        print(f"wc: {file}: Permission denied")
    except Exception as e:
        print(f"wc: An error occurred: {e}")

def sort_file(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in sorted(lines):
                print(line.strip())
    except FileNotFoundError:
        print(f"sort: {file}: No such file or directory")
    except PermissionError:
        print(f"sort: {file}: Permission denied")
    except Exception as e:
        print(f"sort: An error occurred: {e}")

def unique_lines(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            for line in set(lines):
                print(line.strip())
    except FileNotFoundError:
        print(f"uniq: {file}: No such file or directory")
    except PermissionError:
        print(f"uniq: {file}: Permission denied")
    except Exception as e:
        print(f"uniq: An error occurred: {e}")

def show_uptime():
    try:
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        print(f"up {uptime}")
    except Exception as e:
        print(f"uptime: An error occurred: {e}")


def show_processes():
    try:
        processes = list(psutil.process_iter(attrs=[
            'pid', 'name', 'username', 'cpu_percent', 'memory_percent', 
            'memory_info', 'status', 'create_time'
        ]))
        
        # Sort processes by name to group them
        processes.sort(key=lambda p: p.info['name'])
        
        print(f"{'USER':<20} {'PID':<5} {'%CPU':<4} {'%MEM':<4} {'VSZ':<8} {'RSS':<8} {'TTY':<7} {'STAT':<7} {'START':<8} {'TIME':<12} {'COMMAND'}")
        
        for proc in processes:
            try:
                pinfo = proc.info
                if not pinfo['username']:
                    continue
                username = pinfo['username']
                pid = pinfo['pid']
                cpu_percent = pinfo['cpu_percent']
                memory_percent = pinfo['memory_percent']
                vms = get_size(pinfo['memory_info'].vms) if pinfo['memory_info'] else '0B'
                rss = get_size(pinfo['memory_info'].rss) if pinfo['memory_info'] else '0B'
                status = pinfo['status'] if pinfo['status'] else 'N/A'
                create_time = datetime.fromtimestamp(pinfo['create_time']) if pinfo['create_time'] else datetime.now()
                start_time = create_time.strftime('%H:%M:%S')
                run_time = str(datetime.now() - create_time).split('.')[0]  # format to remove microseconds
                
                name = pinfo['name']
                # Append PID to name if there are duplicates
                same_name_count = len([p for p in processes if p.info['name'] == pinfo['name']])
                if same_name_count > 1:
                    name = f"{pinfo['name']}[{pid}]"
                
                print(f"{username:<20} {pid:<5} {cpu_percent:<4.1f} {memory_percent:<4.1f} {vms:<8} {rss:<8} {'?':<7} {status:<7} {start_time:<8} {run_time:<12} {name}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"ps: An error occurred: {e}")

def kill_process(pid):
    try:
        os.kill(int(pid), 9)
    except ProcessLookupError:
        print(f"kill: {pid}: No such process")
    except PermissionError:
        print(f"kill: {pid}: Permission denied")
    except Exception as e:
        print(f"kill: An error occurred: {e}")

def show_memory():
    try:
        svmem = psutil.virtual_memory()
        print(f"Total: {get_size(svmem.total)}")
        print(f"Used: {get_size(svmem.used)}")
        print(f"Free: {get_size(svmem.free)}")
    except Exception as e:
        print(f"free: An error occurred: {e}")