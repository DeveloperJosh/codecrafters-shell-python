# src/commands/type.py

class TypeCommand:
    def execute(self, args):
        if not args:
            print("Usage: type <filename>")
            return

        filename = args[0]
        try:
            with open(filename, 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
