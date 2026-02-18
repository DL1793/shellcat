import time
import curses

class Sprite:
    def __init__(self, states, animations):
        self.anim_states = dict(zip(states, animations))
        self.current_state = states[0]
        self.frame_index = 0
        
        #Transition Logic
        self.default_state = states[0]
        self.state_expiry = 0

    def set_state(self, state_name, duration=0.0):
        if state_name in self.anim_states:
            self.current_state = state_name
            self.frame_index = 0
        
        if duration > 0:
            self.state_expiry = time.time() + duration
        else:
            self.state_expiry = 0.0

    def update(self):
        if self.state_expiry > 0 and time.time() > self.state_expiry:
            self.current_state = self.default_state
            self.state_expiry = 0.0
            self.frame_index = 0

        frames = self.anim_states[self.current_state]
        self.frame_index = (self.frame_index + 1) % len(frames)

    def get_current_frame(self):
        return self.anim_states[self.current_state][self.frame_index]
    
    def draw(self, stdscr, y, x):
        frame = self.anim_states[self.current_state]
        frame_lines = frame.split('\n')
        for i in range(len(frame_lines)):
            stdscr.addstr(y + i, x, frame_lines[i])

class Ui_frame:
    def __init__(self, buttons):
        self.buttons = buttons
        self.current_index = 0
        self.selected_button = buttons[self.current_index]

    def handle_input(self, key):
        match key:
            case curses.KEY_ENTER:
                self.selected_button.action()
            case curses.KEY_LEFT:
                self.current_index = (self.current_index - 1) % len(self.buttons)
            case curses.KEY_RIGHT:
                self.current_index = (self.current_index + 1) % len(self.buttons)
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

class Slider(Button):
    def __init__(self, text, up, down):
        super().__init__(text)
        self.action = None
        self.up = up
        self.down = down

class Screen():
    def __init__(self, ui, background=None, foreground=None,):
        self.background = background
        self.foreground = foreground
        self.ui = ui

    def render(self, stdscr):
        if self.background:
            self.background.draw(stdscr, 0, 0)
        
        if self.foreground:
            self.foreground.draw(stdscr, 10, 10)

        BUTTON_HEIGHT = 40
        spacing = 2
        current_x = 10
        
        for index, button in enumerate(self.ui.buttons):

            # Associate buttons with button index, true for the selected button
            is_selected = (index == self.ui.current_index)

            text = f"> {button.text} <" if is_selected else f" {button.text} "

            # Apply inverse attribute to selected button
            attr = curses.A_REVERSE if is_selected else curses.A_NORMAL
            stdscr.addstr(BUTTON_HEIGHT, current_x, text, attr)

            current_x += len(text) + spacing
