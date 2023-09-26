def get_main_menu_selection():
    print("What do you need?")
    print("[1] Configure Save File Path")
    print("[2] Access Ingredient Data")
    print("[Q] Close Application")
    return input('Please select an option: ')


def cleanse_input(user_input):
    user_input = str(user_input).lower().strip()
    return user_input


def run_save_file_path_configuration():
    pass


def run_ingredient_tracking():
    pass


def main():
    print("Ingredient Tracker Application Started. Welcome!")
    is_application_running = True
    while is_application_running:
        main_menu_input = get_main_menu_selection()
        main_menu_input = cleanse_input(main_menu_input)
        if main_menu_input == 'q':
            is_application_running = False
            continue
        elif main_menu_input == '1':
            run_save_file_path_configuration()
        elif main_menu_input == '2':
            run_ingredient_tracking()
        else:
            print('Option \'' + main_menu_input + '\' isn\'t a valid selection')

    print("Ingredient Tracker Application Closing. Thank you!")


main()
