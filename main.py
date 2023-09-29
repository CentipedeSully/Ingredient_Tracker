import Utilities as Utils


def main():
    print("Ingredient Tracker Application Started. Welcome!")
    is_application_running = True
    while is_application_running:
        main_menu_input = Utils.get_main_menu_selection()
        if main_menu_input == 'q':
            is_application_running = False
            continue
        elif main_menu_input == '1':
            Utils.run_save_file_path_configuration()
        elif main_menu_input == '2':
            Utils.run_ingredient_tracking()
        else:
            print('Option \'' + main_menu_input + '\' isn\'t a valid selection')

    print("Ingredient Tracker Application Closing. Thank you!")


main()
