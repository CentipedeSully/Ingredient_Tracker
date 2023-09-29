import Ingredient_Class


def get_main_menu_selection():
    print("What do you need?")
    print("[1] Configure Save File Path")
    print("[2] Access Ingredient Data")
    print("[Q] Close Application")
    raw_input = input('Input an option: ')
    return cleanse_input(raw_input)


def get_ingredient_menu_selection():
    print("Ingredient Data: What are you looking for?")
    print("[1] Display All Ingredients")
    print("[2] Find Ingredient")
    print("[3] Find Chemical")
    print("[4] Add Ingredient")
    print("[5] Edit Ingredient")
    print("[6] Remove Ingredient")
    print("[Q] Back to Main Menu")
    return cleanse_input(input("Input an option: "))


def cleanse_input(user_input):
    user_input = str(user_input).lower().strip()
    return user_input


def is_input_integer(input_str):
    try:
        integer_value = int(input_str)
        return True

    except ValueError:
        return False


def is_ingredient_in_set(ingredient_name, ingredient_collection):
    if len(ingredient_collection) < 1:
        return False
    else:
        for ingredient in ingredient_collection:
            if ingredient_name == ingredient.name_str:
                return True

        return False


def get_ingredient_from_collection(ingredient_name, ingredient_collection):
    for ingredient in ingredient_collection:
        if ingredient_name == ingredient.name_str:
            return ingredient

    return None


def display_ingredient_collection(ingredient_collection):
    if len(ingredient_collection) == 0:
        print("No matches found.")
        return
    else:
        print("Showing '" + str(len(ingredient_collection)) + "'matches...")
        for ingredient in ingredient_collection:
            ingredient.display_analysis()
        print("Completed showing matches.")


def fetch_ingredients_by_name(ingredients_set, filter_str=''):
    matches_list = list()
    for ingredient_obj in ingredients_set:
        if filter_str in ingredient_obj.name_str:
            matches_list.__add__(ingredient_obj)

    matches_list.sort()
    if filter_str != '':
        print("Displaying ingredients based on filter: '" + filter_str + "'...")

    display_ingredient_collection(matches_list)


def fetch_ingredients_by_chemical(ingredient_set, chem_name, min_concentration_int=1, max_concentration_int=9):
    matches_list = list()

    for ingredient in ingredient_set:
        if chem_name in ingredient.composition_dict:
            if min_concentration_int < ingredient.composition_dict[chem_name] < max_concentration_int:
                matches_list.__add__(ingredient)

    matches_list.sort()     # sorted alphabetically
    matches_sorted_by_concentration_list = list()
    max_iterations = len(matches_list)

    for i in range(0, max_iterations):
        largest_concentration_ingredient = None
        for ingredient in matches_list:
            if largest_concentration_ingredient is None:
                largest_concentration_ingredient = ingredient
            elif ingredient.composition_dict[chem_name] > largest_concentration_ingredient.composition_dict[chem_name]:
                largest_concentration_ingredient = ingredient

        matches_sorted_by_concentration_list.__add__(largest_concentration_ingredient)
        matches_list.remove(largest_concentration_ingredient)

    filter_str = "'" + chem_name + "', concentration range(" + str(min_concentration_int) + ", " + str(max_concentration_int) +")"
    print("Displaying ingredients based on filter: " + filter_str)
    display_ingredient_collection(matches_sorted_by_concentration_list)


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
                fetch_ingredients_by_name(ingredients_set)


            case "2":
                # run Search via Ingredient Name
                ingredient_name = cleanse_input(input("Input ingredient name: "))
                fetch_ingredients_by_name(ingredients_set, ingredient_name)


            case "3":
                # run Search via Chemicals
                chem_search = cleanse_input(input("Input 'chemical_name', 'min_value', 'max_value' [range optional]: "))
                input_list = chem_search.split(",")
                chem_name = ''
                min_concentration = 0
                max_concentration = 999

                for index in range(0, len(input_list)):
                    input_list[index] = cleanse_input(input_list[index])
                    if index == 0:
                        chem_name = input_list[index]
                    elif index == 1:
                        if is_input_integer(input_list[index]):
                            min_concentration = int(input_list[index])
                    elif index == 2:
                        if is_input_integer(input_list[index]):
                            max_concentration = int(input_list[index])

                fetch_ingredients_by_chemical(chem_name, min_concentration, max_concentration)


            case "4":
                # Add ingredient to set
                ingredient_name = cleanse_input(input("Input new ingredient name: "))
                if ingredient_name in ingredients_set:
                    print(ingredient_name + " already exists in database: ")
                else:
                    new_ingredient = Ingredient_Class.Ingredient(ingredient_name)
                    ingredients_set.add(new_ingredient)
                    print(ingredient_name + " added to database")


            case "5":
                pass
                # Edit ingredient: Add/Remove/update chemical (or back)


            case "6":
                # Remove ingredient from set
                ingredient_name = cleanse_input(input("Input ingredient to remove: "))
                if is_ingredient_in_set(ingredient_name, ingredients_set):
                    confirm_removal = cleanse_input(input("Ingredient '" + ingredient_name + "' data will be deleted. Are you sure? (y/n)"))

                    if confirm_removal == 'y' or confirm_removal == 'yes':
                        ingredient_match = get_ingredient_from_collection(ingredient_name, ingredients_set)
                        ingredients_set.remove(ingredient_match)
                        print(ingredient_name + "removed from database")
                    else:
                        print("Removal aborted")
                else:
                    print("Ingredient '" + ingredient_name + "'  doesn't exist in database")


            case "q":
                # return to main menu
                is_manipulating_ingredient_data = False
                continue
