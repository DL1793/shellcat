import time
import curses
from game.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Engine:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.running = True
        self.frameDuration = 0.5

        # Screen Colors
        self.color = 1
        self.colors = [1, 2, 3, 4]

        # Router definition
        self.screens = {}
        self.current_screen = None

        # System settings
        curses.curs_set(0) # Hide cursor
        self.stdscr.timeout(300) # Non-blocking input check
        self._init_colors()

        # Window Size
        self.HEIGHT = SCREEN_HEIGHT
        self.WIDTH = SCREEN_WIDTH

        height, width = self.stdscr.getmaxyx()

        self.viewport_window = None

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()

        if curses.can_change_color():
            curses.init_color(10,82,86,118) # Terminal - 10
            curses.init_color(11,310,310,310) # Dark Gray - 11
            curses.init_color(12,659,659,659) # Light Gray - 12
            curses.init_color(13, 847, 333, 333) # Light Red - 13
            curses.init_color(14, 467, 824, 855) # Light Cyan - 14
            curses.init_color(15, 843, 894, 400) # Light Yellow - 15

        curses.init_pair(2, curses.COLOR_WHITE, 10)
        curses.init_pair(3, 13, 10)
        curses.init_pair(4, 14, 10)
        curses.init_pair(1, 15, 10)

    def register_screen(self, key, screen):
        self.screens[key] = screen

    def change_screen(self, key):
        self.current_screen = self.screens[key]
    
    def run(self):

        viewport_pad = curses.newpad(self.HEIGHT,self.WIDTH)
        updateFrameTime = time.time()
        
        while self.running:

            # Get Input
            key = self.stdscr.getch()
            

            # Handle Resize
            if key == curses.KEY_RESIZE:
                curses.update_lines_cols()

            height, width = self.stdscr.getmaxyx()

            if height <= self.HEIGHT or width <= self.WIDTH:
                self.stdscr.erase()
                warning = f"Window too small. Resize to {self.HEIGHT}/{self.WIDTH} H:{height}W:{width}"
                try:
                    self.stdscr.addstr(height // 2 - 1, (width - len(warning)) // 2, warning)
                except curses.error:
                    pass
                self.stdscr.refresh()
                continue
            else:
                start_y = (height - self.HEIGHT) // 2
                start_x = (width - self.WIDTH) // 2
                self.viewport_window = curses.newwin(self.HEIGHT, self.WIDTH, start_y, start_x)

                self.viewport_window.keypad(True)


            # Handle Input
            if self.current_screen and key != -1:
                    self.current_screen.ui.handle_input(key)
                    
            # Update Foreground Sprite
            if self.current_screen and self.current_screen.foreground:
                    if time.time() >= updateFrameTime:
                        self.current_screen.foreground.update()
                        updateFrameTime = time.time() + self.frameDuration

            # Render new frame
            self.stdscr.erase()

            self.viewport_window.bkgd(' ', curses.color_pair(self.colors[self.color]))

            if self.current_screen:
                        self.current_screen.render(self.viewport_window)            

            self.stdscr.noutrefresh()
            self.viewport_window.noutrefresh()

            curses.doupdate()