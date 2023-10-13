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

        self._number_of_chemical_entries = 3
        self._max_number_of_chemicals = 16
        self._input_cell_width = 5
        self._input_cell_height = 5

        self._table_content_dict = dict()


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
        self.rebuild_chemical_entries(self._number_of_chemical_entries)

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
                                                  textvariable= self._quantity_min_variable_list[row],
                                                  validate='key', validatecommand= self._check_num_wrapper)

            self._max_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'], width=5,
                                                  textvariable= self._quantity_max_variable_list[row],
                                                  validate='key', validatecommand= self._check_num_wrapper)



            self._chem_entry_dict[row].grid(row=row, column=0, columnspan=6, sticky='nesw')
            self._min_entry_dict[row].grid(row=row, column=6, sticky='nesw')
            self._max_entry_dict[row].grid(row=row, column=7, sticky='nesw')

            if self._context == "search":
                self._max_entry_dict[row]['state'] = '!disabled'
            else:
                self._max_entry_dict[row]['state'] = 'disabled'

        # update utils
        self._number_of_chemical_entries = number_of_desired_entries

    def increment_chemical_entries(self, event):
        if self._number_of_chemical_entries < self._max_number_of_chemicals:
            self.rebuild_chemical_entries(self._number_of_chemical_entries + 1)

    def decrement_chemical_entries(self, event):
        if self._number_of_chemical_entries > 0:
            self.rebuild_chemical_entries(self._number_of_chemical_entries - 1)

    def clear_entries(self, event):
        pass

    def submit_query(self, event):
        pass

    def search_entry(self, search_tuple: tuple):
        pass

    def add_entry(self, add_tuple: tuple):
        pass

    def remove_entry(self, remove_tuple: tuple):
        pass


    def build_ingredient_to_query(self) -> Ingredient.Ingredient:
        # get ingredient input & create ingredient
        ingredient_name = self._ent_dict['ingredient'].get()

        if ingredient_name != '':
            new_ingredient = Ingredient.Ingredient(ingredient_name)

            # get chemical inputs, after validating the ingrdient input
            if self._number_of_chemical_entries > 0:
                for index in range(0, self._number_of_chemical_entries):
                    chem_name = self._chem_entry_dict[index].get()
                    chem_min_quantity = self._min_entry_dict[index].get()
                    chem_max_quantity = self._max_entry_dict[index].get()

                    if chem_name != '':
                        pass
                        #new_ingredient.composition_dict[chem_name]




    def populate_display_with_entries(self, ingredient_entry_list: list):
        # entry format -> First element: (ingredient name, [empty string], [empty string])
        #                 Next elemnt:   ([empty string], chem name, chem quantity)
        #                 Next elemnts:  ([empty string], chem name, chem quantity)
        #                 ...

        # insert ingredient name first
        table_id = ingredient_entry_list[0]
        self._treeview_table.insert(parent='', index=tk.END, id=table_id, values=ingredient_entry_list[0])

        # keep a record of this ingredient's table id and list of chemical ids
        chem_id_list = list()
        self._table_content_dict[table_id] = chem_id_list


        # insert next entries as children of the first
        if len(ingredient_entry_list) > 1:
            for index in range(1, len(ingredient_entry_list)):
                chemical_name = ingredient_entry_list[index][1]     # ('', CHEM_NAME, quantity)
                self._treeview_table.insert(parent=table_id, index=tk.END, id=chemical_name, values= ingredient_entry_list[index])
                chem_id_list.append(chemical_name)



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
                chem_names_list.append(chemical)
            chem_names_list.sort()

            # add each chemical to the return list in the sorted order
            for chemical in chem_names_list:
                entry_list.append(('', chemical, ingredient.composition_dict[chemical]))
            return entry_list


def _check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 3

