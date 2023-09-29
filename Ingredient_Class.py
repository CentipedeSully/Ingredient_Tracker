class Ingredient:

    def __init__(self, name):
        self.name_str = name
        self.composition_dict = dict()

    def add_chemical(self, chem_name, chem_concentration):
        self.composition_dict[chem_name] = chem_concentration
        print(chem_name + " added to ingredient: " + self.name_str)

    def remove_chemical(self, chem_name):
        if self.composition_dict.__contains__(chem_name):
            self.composition_dict.pop(chem_name)
            print(chem_name + ' removed from ingredient: ' + self.name_str)

    def display_analysis(self):
        ingredient_name = "Ingredient: " + self.name_str + '\n'
        indentation = "    "
        composition_breakdown = "Chemical Composition:" + "\n"

        for chemical in self.composition_dict:
            composition_breakdown += indentation
            composition_breakdown += chemical + ": " + self.composition_dict[chemical] + "\n"

        border = "----------------------------------------------"
        print(ingredient_name + composition_breakdown + border)

    def does_chemical_exist(self, chem_name):
        if self.composition_dict.__contains__(chem_name):
            return True
        else:
            return False

    def get_chemical_info(self, chem_name):
        if self.does_chemical_exist(chem_name):
            return self.composition_dict[chem_name]
        else:
            return False

