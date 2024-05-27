# src/commands/builtin.py

import os
import glob
import re
import stat
import time

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

class LsCommand:
    
    def execute(self, args):
     targets = args if args else ["."]
     exclude_patterns = [
        re.compile(r'^NTUSER\.DAT'),
        re.compile(r'^ntuser\.dat\.LOG\d+'),
        re.compile(r'^NTUSER\.DAT\{[a-f0-9-]+\}\.TM\.blf$'),
        re.compile(r'^NTUSER\.DAT\{[a-f0-9-]+\}\.TMContainer\d+\.regtrans-ms$'),
        re.compile(r'^ntuser\.ini$'),
        # remove files with @ and $ in the name
        re.compile(r'@'),
        re.compile(r'\$')
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

class PwdCommand:
    def execute(self, args):
        print(os.getcwd())
        
class KillCommand:
    def execute(self, args):
        if not args:
            print("kill: missing operand")
            return
        try:
            pid = int(args[0])
            os.kill(pid, 9)
        except ValueError:
            print(f"kill: {args[0]}: invalid pid")
        except ProcessLookupError:
            print(f"kill: {args[0]}: no such process")
        except PermissionError:
            print(f"kill: {args[0]}: permission denied")
            
class ExitCommand:
    def execute(self, args=None):
        raise SystemExit()
    
class CdCommand:
    def execute(self, args):
        if not args:
            print("cd: missing operand")
            return
        path = args[0]
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")
        except NotADirectoryError:
            print(f"cd: {path}: Not a directory")
        except PermissionError:
            print(f"cd: {path}: Permission denied")
            
class CatCommand:
    def execute(self, args):
        if not args:
            print("cat: missing operand")
            return
        try:
            with open(args[0], 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print(f"cat: {args[0]}: No such file or directory")
        except IsADirectoryError:
            print(f"cat: {args[0]}: Is a directory")
        except PermissionError:
            print(f"cat: {args[0]}: Permission denied")