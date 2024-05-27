# src/commands/init.py

from .echo import EchoCommand
from .type import TypeCommand
from .sysinfo import SysInfoCommand
from .help import HelpCommand
from .clear import ClearCommand
from .builtin import LsCommand, PwdCommand, KillCommand, ExitCommand, CdCommand

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
    "cd": CdCommand()
}

def get_command(command_name):
    return command_registry.get(command_name)
