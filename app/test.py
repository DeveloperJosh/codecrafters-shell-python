import curses
import logging

class CodeCommand:
    def __init__(self):
        # Setup logging
        logging.basicConfig(filename='key_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
        self.mode = 'COMMAND'
        self.command = ""

    def log_key(self, key):
        logging.info(f'Key pressed: {key} ({chr(key) if 32 <= key <= 126 else ""})')

    def execute(self, args):
        filename = args[0] if args else None
        curses.wrapper(self.main, filename)

    def main(self, stdscr, filename):
        curses.curs_set(1)
        stdscr.clear()
        
        # Load file content if filename is provided
        if filename:
            with open(filename, 'r') as f:
                lines = f.readlines()
        else:
            lines = [""]

        # Ensure there's always at least one line
        if not lines:
            lines = [""]

        # Initialize cursor position
        cursor_x = 0
        cursor_y = 0
        
        # Edit loop
        while True:
            stdscr.clear()
            
            # Display mode, command, and file content
            stdscr.addstr(0, 0, f'-- {self.mode} -- {self.command}')
            for idx, line in enumerate(lines):
                stdscr.addstr(idx + 1, 0, line.rstrip())
            
            stdscr.move(cursor_y + 1, cursor_x)
            stdscr.refresh()
            
            key = stdscr.getch()
            self.log_key(key)

            if self.mode == 'COMMAND':
                if key == ord(':'):
                    self.command = ':'
                elif self.command and key in (curses.KEY_ENTER, 10, 13):
                    if self.command == ':wq':
                        # Save and quit
                        if filename:
                            with open(filename, 'w') as f:
                                f.write("".join(lines))
                        break
                    self.command = ""
                elif self.command:
                    self.command += chr(key)
                elif key == ord('i'):
                    self.mode = 'INSERT'
                elif key == ord('h'):
                    cursor_x = max(0, cursor_x - 1)
                elif key == ord('j'):
                    cursor_y = min(len(lines) - 1, cursor_y + 1)
                elif key == ord('k'):
                    cursor_y = max(0, cursor_y - 1)
                elif key == ord('l'):
                    cursor_x = min(len(lines[cursor_y]), cursor_x + 1)
                elif key == ord('x') or key == 8:  # DEL key in COMMAND mode
                    if cursor_x < len(lines[cursor_y]):
                        lines[cursor_y] = lines[cursor_y][:cursor_x] + lines[cursor_y][cursor_x + 1:]
                    elif cursor_y < len(lines) - 1:
                        lines[cursor_y] += lines[cursor_y + 1]
                        del lines[cursor_y + 1]
                elif key == 27:  # Escape key
                    break
            elif self.mode == 'INSERT':
                if key == curses.KEY_UP:
                    cursor_y = max(0, cursor_y - 1)
                    cursor_x = min(cursor_x, len(lines[cursor_y]))
                elif key == curses.KEY_DOWN:
                    cursor_y = min(len(lines) - 1, cursor_y + 1)
                    cursor_x = min(cursor_x, len(lines[cursor_y]))
                elif key == curses.KEY_LEFT:
                    cursor_x = max(0, cursor_x - 1)
                elif key == curses.KEY_RIGHT:
                    cursor_x = min(len(lines[cursor_y]), cursor_x + 1)
                elif key == curses.KEY_BACKSPACE or key == 127:
                    if cursor_x > 0:
                        lines[cursor_y] = lines[cursor_y][:cursor_x - 1] + lines[cursor_y][cursor_x:]
                        cursor_x -= 1
                    elif cursor_y > 0:
                        cursor_x = len(lines[cursor_y - 1])
                        lines[cursor_y - 1] += lines[cursor_y]
                        del lines[cursor_y]
                        cursor_y -= 1
                elif key == 8:  # DEL key in INSERT mode
                    if cursor_x < len(lines[cursor_y]):
                        lines[cursor_y] = lines[cursor_y][:cursor_x] + lines[cursor_y][cursor_x + 1:]
                    elif cursor_y < len(lines) - 1:
                        lines[cursor_y] += lines[cursor_y + 1]
                        del lines[cursor_y + 1]
                elif key == 10:  # Enter key
                    lines.insert(cursor_y + 1, lines[cursor_y][cursor_x:])
                    lines[cursor_y] = lines[cursor_y][:cursor_x]
                    cursor_y += 1
                    cursor_x = 0
                elif key == 27:  # Escape key to switch to Command mode
                    self.mode = 'COMMAND'
                else:
                    if cursor_y >= len(lines):
                        lines.append("")
                    if cursor_x < len(lines[cursor_y]):
                        lines[cursor_y] = lines[cursor_y][:cursor_x] + chr(key) + lines[cursor_y][cursor_x:]
                    else:
                        lines[cursor_y] += chr(key)
                    cursor_x += 1

        # Save file content if filename is provided and command was to save
        if filename and self.command == ':wq':
            with open(filename, 'w') as f:
                f.write("\n".join(lines) + "\n")
