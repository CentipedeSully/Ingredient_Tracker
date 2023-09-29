import Ingredient_Class


def get_main_menu_selection():
    print("What do you need?")
    print("[1] Configure Save File Path")
    print("[2] Access Ingredient Data")
    print("[Q] Close Application")
    raw_input = input('Please select an option: ')
    return cleanse_input(raw_input)


def get_ingredient_menu_selection():
    print("Ingredient Data: What are you looking for?")
    print("[1] Display All Ingredients")
    print("[2] Find Ingredient")
    print("[3] Find Chemical")
    print("[4] Add Ingredient")
    print("[5] Edit Ingredient")
    print("[6] Remove Ingredient")
    print("[q] Back to Main Menu")
    return cleanse_input(input("Select an option"))


def cleanse_input(user_input):
    user_input = str(user_input).lower().strip()
    return user_input


def display_ingredients(ingredients_set, filter_str):
    if filter_str == '':
        print("Displaying all ingredients...")
    else:
        print("Displaying ingredients based on filter: '" + filter_str + "'...")

    for ingredient_obj in ingredients_set:
        if filter_str in ingredient_obj.name_str:
            ingredient_obj.display_analysis()

    print("All found ingredients listed")



def run_save_file_path_configuration():
    pass


def run_ingredient_tracking():
    pass


def control_ingredient_interface(ingredients_set):
    is_manipulating_ingredient_data = True
    while is_manipulating_ingredient_data:
        ingredient_input = get_ingredient_menu_selection()

        match ingredient_input:
            case "1":
                # show all ingredients
                display_ingredients(ingredients_set, '')


            case "2":
                # run Search via Ingredient Name
                ingredient_name = cleanse_input(input("Input ingredient name: "))
                display_ingredients(ingredients_set, ingredient_name)

            case "3":
                pass
                # run Search via Chemicals

            case "4":
                pass
                # Add ingredient to set

            case "5":
                pass
                # Edit ingredient

            case "6":
                pass
                # Remove ingredient from set

            case "q":
                # return to main menu
                is_manipulating_ingredient_data = False
                continue




