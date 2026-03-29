import time
import curses
from game.settings import UI_HEIGHT, BUTTON_SPACING

class Sprite:
    def __init__(self, animations):
        self.anim_states = animations
        self.current_state = next(iter(animations)) # First entry in dict
        self.frame_index = 0
        
        #Transition Logic
        self.default_state = next(iter(animations)) # First entry in dict
        self.state_expiry = 0

    def set_default_state(self, state):
        self.default_state = state
        self.frame_index = 0

    def set_state(self, state_name, duration=0.0):
        if self.current_state == state_name:
            return False

        if state_name in self.anim_states:
            self.current_state = state_name
            self.frame_index = 0
        
        if duration > 0:
            self.state_expiry = time.time() + duration
        else:
            self.state_expiry = 0.0
        return True

    def update(self):
        if self.state_expiry > 0 and time.time() > self.state_expiry:
            self.current_state = self.default_state
            self.state_expiry = 0.0
            self.frame_index = 0

        frames = self.anim_states[self.current_state]["Frames"]


        self.frame_index = (self.frame_index + 1) % len(frames)

    def get_current_frame(self):
        return self.anim_states[self.current_state]["Frames"][self.frame_index]
    
    def get_clip_position(self):
        return self.anim_states[self.current_state]["Position"]
    
    def draw(self, stdscr):
        frame = self.get_current_frame()

        y, x = self.get_clip_position()

        for i, line in enumerate(frame):
            for j, char in enumerate(line):
                try:
                    if char != " ":
                        stdscr.addstr(y + i, x + j, char)
                except curses.error:
                    # Escape in case we draw out of bounds
                    pass

class Ui_frame:
    def __init__(self, buttons):
        self.buttons = buttons
        self.current_index = 0
        
        

        self.buttons_len = 0
        for button in buttons:
            button_len = len(button.text) + 4
            self.buttons_len += button_len
        
        self.buttons_len += 2 * (len(buttons) - 1)

    @property
    def selected_button(self):
        return self.buttons[self.current_index]       

    def handle_input(self, key):
        match key:
            case 10 | 13 | curses.KEY_ENTER:
                if type(self.selected_button) is Button:
                    self.selected_button.action()
            case curses.KEY_LEFT:
                self.current_index = (self.current_index - 1) % len(self.buttons)
                #self.selected_button = self.buttons[self.current_index]
            case curses.KEY_RIGHT:
                self.current_index = (self.current_index + 1) % len(self.buttons)
                #self.selected_button = self.buttons[self.current_index]
            case curses.KEY_UP:
                if isinstance(self.selected_button, Slider):
                    self.selected_button.up()
            case curses.KEY_DOWN:
                if isinstance(self.selected_button, Slider):
                    self.selected_button.down()





class Button:
    def __init__(self, text, action):
        self.text = text
        self.action = action

class Slider():
    def __init__(self, text, up, down):
        self.text = text
        self.up = up
        self.down = down

class Screen():
    def __init__(self, ui, background=None, foreground=None, bgCoord=None, fgCoord=None):
        self.background = background
        self.foreground = foreground
        self.bgCoord = bgCoord
        self.fgCoord = fgCoord
        self.ui = ui

    def render(self, window):
        
        if self.background:
            self.background.draw(window)
        
        if self.foreground:
            self.foreground.draw(window)

        BUTTON_HEIGHT = UI_HEIGHT
        spacing = BUTTON_SPACING
        _, width = window.getmaxyx()
        current_x = width - self.ui.buttons_len - (width - self.ui.buttons_len) // 2
        
        for index, button in enumerate(self.ui.buttons):

            # Associate buttons with button index, true for the selected button
            is_selected = (index == self.ui.current_index)

            text = f"> {button.text} <" if is_selected else f"  {button.text}  "

            # Apply inverse attribute to selected button
            attr = curses.A_REVERSE if is_selected else curses.A_NORMAL
            window.addstr(BUTTON_HEIGHT, current_x, text, attr)

            current_x += len(text) + spacing
