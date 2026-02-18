import time
import curses

class Engine:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.running = True

        # Screen Colors
        self.color = 1
        self.colors = [1, 2, 3, 4]

        # Router definition
        self.screens = {}
        self.current_screen = None

        # System settings
        curses.curs_set(0) # Hide cursor
        self.stdscr.timeout(100) # Non-blocking input check
        self._init_colors()

    def _init_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    def register_screen(self, key, screen):
        self.screens[key] = screen

    def change_screen(self, key):
        self.current_screen = self.screens[key]
    
    def run(self):
        while self.running:

            # Get Input
            key = self.stdscr.getch()

            # Handle Resize
            if key == curses.KEY_RESIZE:
                curses.update_lines_cols()

            # Handle Input
            if self.current_screen and key != -1:
                self.current_screen.ui.handle_input(key)

            # Render new frame
            self.stdscr.erase()

            self.stdscr.bkgd(' ', curses.color_pair(self.colors[self.color]))

            if self.current_screen:
                self.current_screen.render(self.stdscr)
            
            self.stdscr.refresh()
