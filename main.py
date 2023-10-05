from Utilities import *
from gui_window import *


def old_main():
    print("Ingredient Tracker Application Started. Welcome!")
    print("displaying gui window")

    print("Initializing ingredient data...")
    ingredient_set = set()
    is_application_running = True
    while is_application_running:
        main_menu_input = get_main_menu_selection()
        if main_menu_input == 'q':
            is_application_running = False
            continue
        elif main_menu_input == '1':
            control_ingredient_interface(ingredient_set)
        else:
            print('Option \'' + main_menu_input + '\' isn\'t a valid selection')

    print("Ingredient Tracker Application Closing. Thank you!")


def main():
    root = Tk()
    title_str = "Ingredient Tracker"
    window_width = 920
    window_height = 700

    window = gui_window(root, title_str, window_width, window_height)


main()
