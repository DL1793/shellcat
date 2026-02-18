from widgets import Ui_frame, Button, Slider, Screen

def create_main_menu(engine):

    def open_settings_action():
        engine.change_screen("SETTINGS")
    
    def feed_shellcat_action():
        engine.current_screen.foreground.set_state("SHELLCAT_FEED", 2)

    def play_shellcat_action():
        engine.current_screen.foreground.set_state("SHELLCAT_PLAY", 2)

    def exit_game_action():
        engine.running = False
    
    buttons = [
        Button(" [ PLAY WITH SHELLCAT ]", play_shellcat_action),
        Button(" [ FEED SHELLCAT ] ", feed_shellcat_action),
        Button(" [ SETTINGS ] ", open_settings_action),
        Button(" [ EXIT ] ", exit_game_action)
    ]

    return Screen(ui=Ui_frame(buttons))

def create_settings_menu(engine):

    def inc_color_action():
        engine.color += 1 % len(engine.colors)
    
    def dec_color_action():
        engine.color -= 1 % len(engine.colors)
    
    def open_main_action():
        engine.change_scene("MAIN")

    buttons = [
        Slider(" [ COLOR ] ", inc_color_action, dec_color_action),
        Button(" [ EXIT ] ", open_main_action)
    ]

    return Screen(ui=Ui_frame(buttons))