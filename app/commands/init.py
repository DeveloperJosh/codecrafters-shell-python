# src/commands/init.py

from .echo import EchoCommand
from .type import TypeCommand
from .sysinfo import SysInfoCommand
from .help import HelpCommand
from .clear import ClearCommand
from .ps import Ps
from .code import CodeCommand
from .builtin import LsCommand, PwdCommand, KillCommand, ExitCommand, CdCommand, CatCommand

# Command registry
command_registry = {
    "echo": EchoCommand(),
    "type": TypeCommand(),
    "sysinfo": SysInfoCommand(),
    "help": HelpCommand(),
    "clear": ClearCommand(),
    "ls": LsCommand(),
    "pwd": PwdCommand(),
    "kill": KillCommand(),
    "exit": ExitCommand(),
    "cd": CdCommand(),
    "ps": Ps(),
    "code": CodeCommand(),
    "cat": CatCommand()
}

def get_command(command_name):
    return command_registry.get(command_name)
