import curses
from engine.core import Engine
from ui.screens import create_main_menu, create_settings_menu

def main(stdscr):
    engine = Engine(stdscr)
    main_menu = create_main_menu(engine)
    settings_menu = create_settings_menu(engine)
    engine.register_screen("MAIN", main_menu)
    engine.register_screen("SETTINGS", settings_menu)
    engine.current_screen = main_menu
    engine.run()

if __name__ == "__main__":
    curses.wrapper(main)