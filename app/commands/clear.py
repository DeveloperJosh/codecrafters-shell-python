# src/commands/clear.py

import os

class ClearCommand:
    def execute(self, args):
        os.system('cls' if os.name == 'nt' else 'clear')
