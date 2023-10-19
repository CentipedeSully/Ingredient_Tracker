import tkinter as tk
from tkinter import ttk
import Ingredient_Class as Ingredient
import re


# noinspection PyTypeChecker,PyUnusedLocal,SpellCheckingInspection
class GuiWindow:
    def __init__(self, root_window, title_str, window_width, window_height):
        # INITIALIZE:
        self.root = root_window
        self.title = title_str
        self._width = window_width
        self._height = window_height

        self.root.title(title_str)

        self._number_of_chemical_entries = 0
        self._starting_chemical_entries = 3
        self._max_number_of_chemicals = 16
        self._input_cell_width = 5
        self._input_cell_height = 5

        self._table_content_dict = dict()
        self._ingredient_data_dict = dict()

        # used to keep the chemical quantites valid
        self._check_num_wrapper = (self.root.register(_check_num), "%P")
        self._quantity_min_variable_list = list()
        self._quantity_max_variable_list = list()

        # HEADER AND BODY: create & configure
        self._frame_dict = dict()
        self._frame_dict['header'] = tk.Frame(master=self.root, bg="grey",
                                              width=window_width, height=27)

        self._frame_dict['body'] = tk.Frame(master=self.root, bd=10, bg="white",
                                            width=window_width, height=window_height - 27)

        self._frame_dict['header'].pack(fill=tk.X)
        self._frame_dict['body'].pack(fill=tk.BOTH, expand=True)

        self._frame_dict['body'].columnconfigure(index=1, weight=1)
        self._frame_dict['body'].rowconfigure(index=[1, 2, 3], weight=1)

        # INPUT AND DISPLAY: create & configure
        self._frame_dict['input'] = ttk.Frame(master=self._frame_dict['body'], width=100, height=100, borderwidth=10)
        self._frame_dict['table'] = ttk.Frame(master=self._frame_dict['body'], width=10, height=10)

        self._frame_dict['input'].grid(row=1, column=0, sticky='nw')
        self._frame_dict['table'].grid(row=0, rowspan=3, column=1, sticky='news')

        self._input_row_indexes = list(range(0, 8))
        self._input_column_indexes = list(range(0, 9))
        self._frame_dict['input'].rowconfigure(index=self._input_row_indexes, weight=1, minsize=self._input_cell_height)
        self._frame_dict['input'].columnconfigure(index=self._input_column_indexes, weight=1,
                                                  minsize=self._input_cell_width)

        # row index
        # 0: Context Buttons
        # 1: Ingredient Name Label
        # 2: Ingredient Entry
        # 3: Space
        # 4: Chemicals Label
        # 5: Chemical Entries Frame
        # 6: Add/Remove entry Buttons
        # 7: Clear/Submit buttons

        # DISPLAY CONTENTS:
        self._columns = ('ingredient', 'chemical', 'quantity')
        self._treeview_table = ttk.Treeview(master=self._frame_dict['table'], columns=self._columns, show='headings')
        self._treeview_table.heading("ingredient", text='Ingredient')
        self._treeview_table.heading('chemical', text="Chemical")
        self._treeview_table.heading('quantity', text="Qty")

        self._treeview_table.column('ingredient', stretch=tk.YES, anchor='w')
        self._treeview_table.column('chemical', stretch=tk.YES, anchor='w')
        self._treeview_table.column('quantity', width=50, stretch=tk.NO, anchor='e')

        self._treeview_table.grid(row=0, column=0, sticky='nesw')

        # INPUT CONTENTS:
        self._context = "no context selected"
        self._btn_dict = dict()
        self._lbl_dict = dict()
        self._ent_dict = dict()

        # contextual buttons
        self._btn_dict["search"] = ttk.Button(master=self._frame_dict['input'], text='Find')
        self._btn_dict["add"] = ttk.Button(master=self._frame_dict['input'], text='+')
        self._btn_dict['remove'] = ttk.Button(master=self._frame_dict['input'], text='-')

        self._btn_dict["search"].grid(row=0, column=0, columnspan=2, sticky='esw')
        self._btn_dict["add"].grid(row=0, column=2, columnspan=2, sticky='esw')
        self._btn_dict['remove'].grid(row=0, column=4, columnspan=2, sticky='esw')

        self._btn_dict["search"].bind('<Button-1>', self.enter_search_context)
        self._btn_dict["add"].bind('<Button-1>', self.enter_add_context)
        self._btn_dict['remove'].bind('<Button-1>', self.enter_remove_context)

        # labels
        self._lbl_dict['ingredient'] = ttk.Label(master=self._frame_dict['input'], text="Ingredient:", anchor='sw')
        self._lbl_dict['chemical'] = ttk.Label(master=self._frame_dict['input'], text="Chemicals:", anchor='sw')
        self._lbl_dict['min_quantity'] = ttk.Label(master=self._frame_dict['input'], text="Min", anchor='sw')
        self._lbl_dict['max_quantity'] = ttk.Label(master=self._frame_dict['input'], text="Max", anchor='sw')

        self._lbl_dict['ingredient'].grid(row=1, column=0, columnspan=8, sticky='nesw')
        self._lbl_dict['chemical'].grid(row=4, column=0, columnspan=6, sticky='nesw')
        self._lbl_dict['min_quantity'].grid(row=4, column=6, sticky='nesw')
        self._lbl_dict['max_quantity'].grid(row=4, column=7, sticky='nesw')

        # entries
        self._ent_dict['ingredient'] = ttk.Entry(master=self._frame_dict['input'])
        self._ent_dict['ingredient'].grid(row=2, column=0, columnspan=8, sticky='nesw')

        self._chem_entry_dict = dict()
        self._min_entry_dict = dict()
        self._max_entry_dict = dict()

        self._frame_dict['chemical_inputs'] = ttk.Frame(master=self._frame_dict['input'])
        self._frame_dict['chemical_inputs'].columnconfigure(index=self._input_column_indexes, weight=1,
                                                            minsize=self._input_cell_width)
        self._frame_dict['chemical_inputs'].grid(row=5, column=0, columnspan=8, sticky='nesw')
        for row in range(0, self._starting_chemical_entries):
            self.create_chemical_entry()

        # edit chemical entries buttons
        self._btn_dict["increase_capacity"] = ttk.Button(master=self._frame_dict['input'], text='+')
        self._btn_dict["decrease_capacity"] = ttk.Button(master=self._frame_dict['input'], text='-')

        self._btn_dict["increase_capacity"].grid(row=6, column=0, sticky='ew')
        self._btn_dict["decrease_capacity"].grid(row=6, column=1, sticky='ew')

        self._btn_dict["increase_capacity"].bind('<Button-1>', self.increment_chemical_entries)
        self._btn_dict["decrease_capacity"].bind('<Button-1>', self.decrement_chemical_entries)

        # Submission Buttons
        self._btn_dict["submit"] = ttk.Button(master=self._frame_dict['input'], text='>>')
        self._btn_dict["clear"] = ttk.Button(master=self._frame_dict['input'], text='C')

        self._btn_dict["clear"].grid(row=7, column=6, sticky='nesw')
        self._btn_dict["submit"].grid(row=7, column=7, sticky='nesw')

        self._btn_dict["clear"].bind('<Button-1>', self.clear_entries)
        self._btn_dict["submit"].bind('<Button-1>', self.submit_query)

        self.enter_search_context(None)
        self.root.mainloop()

    def enter_search_context(self, event):
        if self._context != 'search':
            self._context = 'search'
            self._btn_dict["search"].state(['disabled'])
            self._btn_dict["add"].state(['!disabled'])
            self._btn_dict["remove"].state(['!disabled'])

            # disable the entries thet're beyond this context
            for index in range(0, self._number_of_chemical_entries):
                self._max_entry_dict[index]['state'] = '!disabled'

    def enter_add_context(self, event):
        if self._context != 'add':
            self._context = 'add'
            self._btn_dict["search"].state(['!disabled'])
            self._btn_dict["add"].state(['disabled'])
            self._btn_dict["remove"].state(['!disabled'])

            # enable the necessary entries
            for index in range(0, self._number_of_chemical_entries):
                self._max_entry_dict[index]['state'] = 'disabled'

    def enter_remove_context(self, event):
        if self._context != 'remove':
            self._context = 'remove'
            self._btn_dict["search"].state(['!disabled'])
            self._btn_dict["add"].state(['!disabled'])
            self._btn_dict["remove"].state(['disabled'])

            # enable the necessary entries
            for index in range(0, self._number_of_chemical_entries):
                self._max_entry_dict[index]['state'] = 'disabled'

    def rebuild_chemical_entries(self, number_of_desired_entries: int):
        number_of_desired_entries = max(0, number_of_desired_entries)

        # remove current entries
        if len(self._chem_entry_dict) > 0:
            print("deleting " + str(len(self._chem_entry_dict)) + ' chem entries...')
            for row in range(0, len(self._chem_entry_dict)):
                self._chem_entry_dict[row].grid_forget()
                self._min_entry_dict[row].grid_forget()
                self._max_entry_dict[row].grid_forget()

                del (self._chem_entry_dict[row])
                del (self._min_entry_dict[row])
                del (self._max_entry_dict[row])

            print("old chemical entries deleted. Current chem_dict size: " + str(len(self._chem_entry_dict)))
            self._quantity_min_variable_list.clear()
            self._quantity_max_variable_list.clear()

        # reconfigure chem entry frame
        if number_of_desired_entries > 1:
            index_list = list(range(0, number_of_desired_entries))
            self._frame_dict['chemical_inputs'].rowconfigure(index=index_list, weight=1, minsize=self._input_cell_width)
        else:
            self._frame_dict['chemical_inputs'].rowconfigure(index=0, weight=1, minsize=self._input_cell_width)

        # create new entries
        for row in range(0, number_of_desired_entries):
            self._chem_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'])

            self._quantity_min_variable_list.append(tk.StringVar())
            self._quantity_max_variable_list.append(tk.StringVar())

            self._min_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'], width=5,
                                                  textvariable=self._quantity_min_variable_list[row],
                                                  validate='key', validatecommand=self._check_num_wrapper)

            self._max_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'], width=5,
                                                  textvariable=self._quantity_max_variable_list[row],
                                                  validate='key', validatecommand=self._check_num_wrapper)

            self._chem_entry_dict[row].grid(row=row, column=0, columnspan=6, sticky='nesw')
            self._min_entry_dict[row].grid(row=row, column=6, sticky='ew')
            self._max_entry_dict[row].grid(row=row, column=7, sticky='ew')

            if self._context == "search":
                self._max_entry_dict[row]['state'] = '!disabled'
            else:
                self._max_entry_dict[row]['state'] = 'disabled'

        # update utils
        self._number_of_chemical_entries = number_of_desired_entries

    def increment_chemical_entries(self, event):
        if self._number_of_chemical_entries < self._max_number_of_chemicals:
            self.create_chemical_entry()

    def decrement_chemical_entries(self, event):
        if self._number_of_chemical_entries > 0:
            self.remove_chemical_entry()

    def create_chemical_entry(self):
        # calculate new row index
        row = self._number_of_chemical_entries
        print("Creating row %s of chemcial entries..." % row)

        # configure grid
        self._frame_dict['chemical_inputs'].rowconfigure(index=row, weight=1, minsize=self._input_cell_width)

        # create new input validation variables
        self._quantity_min_variable_list.append(tk.StringVar())
        self._quantity_max_variable_list.append(tk.StringVar())

        # create new entries
        self._chem_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'])
        self._min_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'], width=5,
                                              textvariable=self._quantity_min_variable_list[row],
                                              validate='key', validatecommand=self._check_num_wrapper)
        self._max_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'], width=5,
                                              textvariable=self._quantity_max_variable_list[row],
                                              validate='key', validatecommand=self._check_num_wrapper)

        # grid the entries
        self._chem_entry_dict[row].grid(row=row, column=0, columnspan=6, sticky='ew')
        self._min_entry_dict[row].grid(row=row, column=6, sticky='ew')
        self._max_entry_dict[row].grid(row=row, column=7, sticky='ew')

        # reflect context selection
        if self._context == "search":
            self._max_entry_dict[row]['state'] = '!disabled'
        else:
            self._max_entry_dict[row]['state'] = 'disabled'

        # update number of chemical entries
        self._number_of_chemical_entries += 1

    def remove_chemical_entry(self):
        if self._number_of_chemical_entries > 0:

            # calculate row
            row = self._number_of_chemical_entries - 1
            print("Removing row %s of chemcial entries..." % row)

            # remove & delete latest entries
            self._chem_entry_dict[row].grid_forget()
            self._min_entry_dict[row].grid_forget()
            self._max_entry_dict[row].grid_forget()

            del (self._chem_entry_dict[row])
            del (self._min_entry_dict[row])
            del (self._max_entry_dict[row])

            # remove input validation variables
            self._quantity_min_variable_list.pop(row)
            self._quantity_max_variable_list.pop(row)

            # update number of chemical entries
            self._number_of_chemical_entries -= 1


    def clear_entries(self, event):
        for entry in self._ent_dict:
            self._ent_dict[entry].delete(0, tk.END)

        for entry in self._chem_entry_dict:
            self._chem_entry_dict[entry].delete(0, tk.END)

        for entry in self._min_entry_dict:
            self._min_entry_dict[entry].delete(0, tk.END)

        for entry in self._max_entry_dict:
            self._max_entry_dict[entry].delete(0, tk.END)

    def submit_query(self, event):
        # get the ingredient name
        name_str = self._ent_dict["ingredient"].get()

        # get the chemical entries
        chem_dict = dict()
        if self._number_of_chemical_entries > 0:
            for index in range(0, self._number_of_chemical_entries):
                # skip blank entries
                if self._chem_entry_dict[index].get() == '':
                    continue

                else:
                    if self._context == "search":
                        # create a tuple as a min,max range from the min/max entries
                        # these are gauranteed to be either integer strings or blank strings
                        # a binding on the min/max entries enforces these strings to be int compatible

                        min_value = self._min_entry_dict[index].get()
                        max_value = self._max_entry_dict[index].get()

                        if min_value == '':
                            min_value = 0
                        else:
                            min_value = int(min_value)

                        if max_value == '':
                            max_value = 1000
                        else:
                            max_value = int(max_value)

                        valid_min = min(min_value, max_value)
                        valid_max = max(min_value, max_value)
                        chem_dict[self._chem_entry_dict[index].get()] = (valid_min, valid_max)


                    elif self._context == 'add' or self._context == "remove":
                        # when adding to the database, we don't care about the max_value entry field
                        # the min entry field will default to 1 if no value is given

                        value = self._min_entry_dict[index].get()
                        if value == '':
                            value = 1
                        chem_dict[self._chem_entry_dict[index].get()] = value

        if self._context == 'search':
            self.search_entry(name_str, chem_dict)
        elif self._context == 'add':
            self.add_entry(name_str, chem_dict)
        elif self._context == 'remove':
            self.remove_entry(name_str, chem_dict)

    def search_entry(self, name_str: str, query_chem_dict: dict):
        # chem_dict format -> key= chemical_name, value= (int, int)

        # create mathes list for sorting later
        ingredient_matches_list = list()

        # enter search
        for ingredient in self._ingredient_data_dict:

            if name_str in ingredient:  # empty strings exist in all strings

                # record the matches by name alone if no chemicals were specified
                if len(query_chem_dict) < 1:
                    ingredient_matches_list.append(ingredient)

                else:
                    # only record the ingredient if it possesses a match to each chemical query
                    chemical_matches_found_int = 0

                    for query_chemical_str in query_chem_dict:
                        query_match_found = False
                        min_value = query_chem_dict[query_chemical_str][0]
                        max_value = query_chem_dict[query_chemical_str][1]

                        # find any occurances of the query within the keys of each ingredient's chem_dictionary
                        for found_chemical_str in self._ingredient_data_dict[ingredient].composition_dict.keys():
                            if query_chemical_str in found_chemical_str:
                                if min_value <= int(self._ingredient_data_dict[ingredient].composition_dict[
                                                        found_chemical_str]) <= max_value:
                                    query_match_found = True
                                    break

                        # if this single query was found, then increment the number of chem matches
                        if query_match_found:
                            chemical_matches_found_int += 1

                    # if we've found a match for each chemical query in this ingredient, then add this ingredient
                    if chemical_matches_found_int == len(query_chem_dict):
                        ingredient_matches_list.append(ingredient)

        # Matches have been recorded, if they exist. Now sort the matches list
        ingredient_matches_list.sort()

        # clear the table display before adding the new matches
        self.clear_display()

        # populate the table display with each match
        for ingredient in ingredient_matches_list:
            table_entry_list = self.convert_ingredient_to_entry_list(self._ingredient_data_dict[ingredient])
            self.populate_display_with_entries(table_entry_list)

        print("Search Completed. Matches found: %s" % len(ingredient_matches_list))

    def add_entry(self, name_str: str, chem_dict: dict):
        # create new ingredient and add it to the database if it doesn't exist
        if not self._ingredient_data_dict.__contains__(name_str):
            new_ingredient = Ingredient.Ingredient(name_str)

            for chemical in chem_dict:
                # print('Building new ingredient chemical data. New chemical: %s' % chemical)
                new_ingredient.composition_dict[chemical] = chem_dict[chemical]

            self._ingredient_data_dict[name_str] = new_ingredient
            print("Added Ingredient '%s'" % name_str)


        # update the ingredient with the new chemical data. DOESN'T DELETE ANY CHEMICALS
        else:
            for chemical in chem_dict:
                self._ingredient_data_dict[name_str].composition_dict[chemical] = chem_dict[chemical]

            print("Updated Ingredient '%s' with additional chemicals" % name_str)

    def remove_entry(self, name_str: str, chem_dict: dict):
        if self._ingredient_data_dict.__contains__(name_str):
            # remove the ingredient if no chemicals were specified
            if len(chem_dict) < 1:
                self._ingredient_data_dict.pop(name_str)
                print("Removed Ingredient '%s'" % name_str)

            # otherwise, only remove from the database the specified chemicals from the specified ingredient
            else:
                for chemical in chem_dict:
                    if self._ingredient_data_dict[name_str].composition_dict.__contains__(chemical):
                        self._ingredient_data_dict[name_str].composition_dict.pop(chemical)
                    print("Updated Ingredient '%s' by removing chemicals" % name_str)

    def clear_display(self):
        if len(self._table_content_dict) > 0:
            for ingredient_entry in self._table_content_dict:
                self._treeview_table.delete(ingredient_entry)

            self._table_content_dict.clear()

    def populate_display_with_entries(self, ingredient_entry_list: list):
        # entry format -> First element: (ingredient name, [empty string], [empty string])
        #                 Next elemnt:   ([empty string], chem name, chem quantity)
        #                 Next elemnts:  ([empty string], chem name, chem quantity)
        #                 ...

        # setup first element special condition & setup list of id's
        is_at_first_element = True
        ingredient_name = ''
        chem_id_list = list()

        for item in ingredient_entry_list:
            if is_at_first_element:
                is_at_first_element = False
                ingredient_name = item[0]
                # print(ingredient_name)
                self._treeview_table.insert(parent='', index=tk.END, iid=ingredient_name, values=item, open=True)
            else:
                chemical_name = item[1]
                # print(chemical_name)
                chem_id_list.append(self._treeview_table.insert(parent=ingredient_name, index=tk.END, values=item))

        self._table_content_dict[ingredient_name] = chem_id_list

    @staticmethod
    def convert_ingredient_to_entry_list(ingredient: Ingredient.Ingredient) -> list:
        # format -> (ingredient name, [nothing]    , [nothing]     )
        #           ([nothing]      , next chemical, chemical value)
        #           ([nothing]      , next chemical, chemical value)
        #           ...

        entry_list = list()
        entry_list.append((ingredient.name_str, '', ''))
        chem_names_list = list()

        if len(ingredient.composition_dict) < 1:
            return entry_list

        else:
            # collect the names for sorting
            for chemical in ingredient.composition_dict:
                print("Building entry list: chemical: " + str(chemical))
                chem_names_list.append(chemical)
            chem_names_list.sort()

            # add each chemical to the return list in the sorted order
            for chemical in chem_names_list:
                entry_list.append(('', chemical, ingredient.composition_dict[chemical]))
            return entry_list


def _check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 3
