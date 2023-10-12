class Ingredient:

    def __init__(self, name):
        self.name_str = name
        self.composition_dict = dict()

    def add_chemical(self, chem_name, chem_concentration_int):
        self.composition_dict[chem_name] = int(chem_concentration_int)
        print(chem_name + " added to ingredient: " + self.name_str)

    def remove_chemical(self, chem_name):
        if self.composition_dict.__contains__(chem_name):
            self.composition_dict.pop(chem_name)
            print(chem_name + ' removed from ingredient: ' + self.name_str)

    def print_analysis(self):
        border = "----------------------------------------------" + '\n'
        indentation = "    "
        ingredient_name = self.name_str + '\n'
        composition_breakdown = ''

        if len(self.composition_dict) < 1:
            composition_breakdown += indentation + "NO DATA\n"

        else:
            for chemical in self.composition_dict:
                composition_breakdown += indentation
                composition_breakdown += chemical + ": " + str(self.composition_dict[chemical]) + "\n"


        print(border + ingredient_name + composition_breakdown + border)

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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name_str == other.name_str
        else:
            return False


    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name_str)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.name_str < other.name_str
        else:
            return False

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.name_str <= other.name_str
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.name_str > other.name_str
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.name_str >= other.name_str
        else:
            return False
