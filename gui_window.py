import tkinter as tk
from tkinter import ttk
import Ingredient_Class as ingre


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
        self._input_cell_width= 5
        self._input_cell_height= 5



        # HEADER AND BODY: create & configure
        self._frame_dict = dict()
        self._frame_dict['header'] = tk.Frame(master=self.root, bg="grey",
                              width=window_width, height=27)

        self._frame_dict['body'] = tk.Frame(master=self.root, bd=10, bg="white",
                            width=window_width, height=window_height - 27)

        self._frame_dict['header'].pack(fill=tk.X)
        self._frame_dict['body'].pack(fill=tk.BOTH, expand=True)

        self._frame_dict['body'].columnconfigure(index=1, weight=1)
        self._frame_dict['body'].rowconfigure(index=[1,2,3], weight= 1)



        # INPUT AND DISPLAY: create & configure
        self._frame_dict['input'] = ttk.Frame(master=self._frame_dict['body'], width=100, height=100, borderwidth=10)
        self._frame_dict['table'] = ttk.Frame(master=self._frame_dict['body'], width=10, height=10)

        self._frame_dict['input'].grid(row=1, column=0, sticky='nw')
        self._frame_dict['table'].grid(row=0, rowspan=3, column=1, sticky='news')

        self._input_row_indexes = list(range(0, 8))
        self._input_column_indexes = list(range(0, 9))
        self._frame_dict['input'].rowconfigure(index=self._input_row_indexes, weight=1, minsize= self._input_cell_height)
        self._frame_dict['input'].columnconfigure(index=self._input_column_indexes, weight=1, minsize= self._input_cell_width)

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

        self._treeview_table.column('ingredient', stretch=tk.YES, anchor= 'w')
        self._treeview_table.column('chemical', stretch=tk.YES, anchor= 'w')
        self._treeview_table.column('quantity', width=50, stretch= tk.NO,anchor= 'e')

        self._treeview_table.grid(row=0, column=0, sticky='news')



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
        self._lbl_dict['quantity'] = ttk.Label(master=self._frame_dict['input'], text="Qty:", anchor='sw')

        self._lbl_dict['ingredient'].grid(row=1, column=0, columnspan=8, sticky='ensw')
        self._lbl_dict['chemical'].grid(row=4, column=0, columnspan=6, sticky='ensw')
        self._lbl_dict['quantity'].grid(row=4, column=6, columnspan=2, sticky='ensw')

        # entries
        self._ent_dict['ingredient'] = ttk.Entry(master=self._frame_dict['input'])
        self._ent_dict['ingredient'].grid(row=2, column=0, columnspan=8, sticky='ensw')

        self._chem_entry_dict = dict()
        self._min_entry_dict = dict()
        self._max_entry_dict = dict()

        self._frame_dict['chemical_inputs'] = ttk.Frame(master= self._frame_dict['input'])
        self._frame_dict['chemical_inputs'].columnconfigure(index=  self._input_column_indexes, weight=1, minsize= self._input_cell_width)
        self._frame_dict['chemical_inputs'].grid(row= 5, column=0, columnspan=7, sticky= 'nesw')
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

        self._btn_dict["clear"].grid(row=7, column=6, sticky='senw')
        self._btn_dict["submit"].grid(row=7, column=7, sticky='snwe')


        self.root.mainloop()





    def enter_search_context(self, event):
        if self._context != 'search':
            self._context = 'search'
            self._btn_dict["search"].state(['disabled'])
            self._btn_dict["add"].state(['!disabled'])
            self._btn_dict["remove"].state(['!disabled'])
            # print("context changed to " + self._context)


    def enter_add_context(self, event):
        if self._context != 'add':
            self._context = 'add'
            self._btn_dict["search"].state(['!disabled'])
            self._btn_dict["add"].state(['disabled'])
            self._btn_dict["remove"].state(['!disabled'])
            # print("context changed to " + self._context)


    def enter_remove_context(self, event):
        if self._context != 'remove':
            self._context = 'remove'
            self._btn_dict["search"].state(['!disabled'])
            self._btn_dict["add"].state(['!disabled'])
            self._btn_dict["remove"].state(['disabled'])
            # print("context changed to " + self._context)


    def rebuild_chemical_entries(self, number_of_desired_entries: int):
        number_of_desired_entries = max(0, number_of_desired_entries)

        # remove current entries
        if len(self._chem_entry_dict) > 0:
            print("deleting " + str(len(self._chem_entry_dict)) + ' chem entries...')
            for row in range(0, len(self._chem_entry_dict)):
                self._chem_entry_dict[row].grid_forget()
                self._min_entry_dict[row].grid_forget()
                self._max_entry_dict[row].grid_forget()

                del(self._chem_entry_dict[row])
                del(self._min_entry_dict[row])
                del(self._max_entry_dict[row])

            print("old chemical entries deleted. Current chem_dict size: " + str(len(self._chem_entry_dict)))

        # reconfigure chem entry frame
        if number_of_desired_entries > 1:
            index_list= list(range(0,number_of_desired_entries))
            self._frame_dict['chemical_inputs'].rowconfigure(index= index_list, weight=1, minsize=self._input_cell_width)
        else:
            self._frame_dict['chemical_inputs'].rowconfigure(index=0, weight=1, minsize=self._input_cell_width)

        # create new entries
        for row in range(0, number_of_desired_entries):
            self._chem_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'])
            self._min_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'], width=5)
            self._max_entry_dict[row] = ttk.Entry(master=self._frame_dict['chemical_inputs'], width=5)

            self._chem_entry_dict[row].grid(row=row, column=0, columnspan=6, sticky='ensw')
            self._min_entry_dict[row].grid(row=row, column=6, sticky='ensw')
            self._max_entry_dict[row].grid(row=row, column=7, sticky='ensw')


        # update utils
        self._number_of_chemical_entries = number_of_desired_entries




    def increment_chemical_entries(self, event):
        if self._number_of_chemical_entries < self._max_number_of_chemicals:
            self.rebuild_chemical_entries(self._number_of_chemical_entries + 1)


    def decrement_chemical_entries(self, event):
        if self._number_of_chemical_entries > 0:
            self.rebuild_chemical_entries(self._number_of_chemical_entries - 1)



    def clear_entries(self,event):
        pass

    def submit_query(self, event):
        pass

    def search_entry(self, search_tuple: tuple):
        pass

    def add_entry(self, add_tuple: tuple):
        pass

    def remove_entry(self, remove_tuple: tuple):
        pass

    def populate_display_with_entries(self, matches_list: list):
        pass


    def remove_widget_from_grid(self, widget):
        self._btn_dict['search'].grid_remove()

    @staticmethod
    def convert_ingredient_to_entry_list(ingredient: ingre.Ingredient) -> list:
        # format -> (ingredient name, chemical name, chemical value)
        #           ([nothing]      , next chemical, chemical value)
        #           ([nothing]      , next chemical, chemical value)

        entry_list = list()

        if len(ingredient.composition_dict) < 1:
            entry_list.append((ingredient.name_str, '', ''))
            return entry_list

        else:
            at_first_index = True
            for chemical in ingredient.composition_dict:
                if at_first_index:
                    at_first_index = False
                    entry_list.append((ingredient.name_str, chemical, ingredient.composition_dict[chemical]))
                else:
                    entry_list.append(('', chemical, ingredient.composition_dict[chemical]))

            return entry_list





