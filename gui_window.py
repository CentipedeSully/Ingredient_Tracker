import tkinter as tk
from tkinter import ttk
import Ingredient_Class as ingredientClass


class GuiWindow:
    def __init__(self, root_window, title_str, window_width, window_height):
        # INITIALIZE:
        self.root = root_window
        self.title = title_str
        self._width = window_width
        self._height = window_height

        self.root.title(title_str)

        self._chem_entry_starting_row = 5
        self._number_of_chemical_entries = 3

        self._input_cell_width= 5
        self._input_cell_height= 5



        # HEADER AND BODY: create & configure
        _frame_header = tk.Frame(master=self.root, bg="grey",
                              width=window_width, height=27)

        _frame_body = tk.Frame(master=self.root, bd=10, bg="white",
                            width=window_width, height=window_height - 27)

        _frame_header.pack(fill=tk.X)
        _frame_body.pack(fill=tk.BOTH, expand=True)

        _frame_body.columnconfigure(index=1, weight=1)
        _frame_body.rowconfigure(index=[1,2,3], weight= 1)



        # INPUT AND DISPLAY: create & configure
        _frame_input = ttk.Frame(master=_frame_body, width=100, height=100, borderwidth=10)
        _frame_display = ttk.Frame(master=_frame_body, width=10, height=10)

        _frame_input.grid(row=1, column=0, sticky='nw')
        _frame_display.grid(row=0, rowspan=3, column=1, sticky='news')

        input_row_indexes = list(range(0, self._chem_entry_starting_row + self._number_of_chemical_entries + 1))
        input_column_indexes = list(range(0, 9))
        _frame_input.rowconfigure(index=input_row_indexes, weight=1, minsize= self._input_cell_height)
        _frame_input.columnconfigure(index=input_column_indexes, weight=1, minsize= self._input_cell_width)



        # DISPLAY CONTENTS:
        columns = ('ingredient', 'chemical', 'quantity')
        _treeview_table = ttk.Treeview(master=_frame_display, columns=columns, show='headings')
        _treeview_table.heading("ingredient", text='Ingredient')
        _treeview_table.heading('chemical', text="Chemical")
        _treeview_table.heading('quantity', text="Qty")

        _treeview_table.column('ingredient', stretch=tk.YES, anchor= 'w')
        _treeview_table.column('chemical', stretch=tk.YES, anchor= 'w')
        _treeview_table.column('quantity', width=50, stretch= tk.NO,anchor= 'e')

        _treeview_table.grid(row=0, column=0, sticky='news')



        # INPUT CONTENTS:
        self._context = "no context selected"
        self._btn_dict = dict()
        self._lbl_dict = dict()
        self._ent_dict = dict()

        # contextual buttons
        self._btn_dict["search"] = ttk.Button(master=_frame_input, text='Find')
        self._btn_dict["add"] = ttk.Button(master=_frame_input, text='+')
        self._btn_dict['remove'] = ttk.Button(master=_frame_input, text='-')

        self._btn_dict["search"].grid(row=0, column=0, columnspan=2, sticky='esw')
        self._btn_dict["add"].grid(row=0, column=2, columnspan=2, sticky='esw')
        self._btn_dict['remove'].grid(row=0, column=4, columnspan=2, sticky='esw')

        self._btn_dict["search"].bind('<Button-1>', self.enter_search_context)
        self._btn_dict["add"].bind('<Button-1>', self.enter_add_context)
        self._btn_dict['remove'].bind('<Button-1>', self.enter_remove_context)

        # labels
        self._lbl_dict['ingredient'] = ttk.Label(master=_frame_input, text="Ingredient:", anchor='sw')
        self._lbl_dict['chemical'] = ttk.Label(master=_frame_input, text="Chemicals:", anchor='sw')
        self._lbl_dict['quantity'] = ttk.Label(master=_frame_input, text="Qty:", anchor='sw')

        self._lbl_dict['ingredient'].grid(row=1, column=0, columnspan=8, sticky='ensw')
        self._lbl_dict['chemical'].grid(row=4, column=0, columnspan=6, sticky='ensw')
        self._lbl_dict['quantity'].grid(row=4, column=6, columnspan=2, sticky='ensw')

        # entries
        self._ent_dict['ingredient'] = ttk.Entry(master=_frame_input)
        self._ent_dict['ingredient'].grid(row=2, column=0, columnspan=8, sticky='ensw')

        self._chem_entry_dict = dict()
        self._min_entry_dict = dict()
        self._max_entry_dict = dict()

        for row in range(0, self._number_of_chemical_entries):
            self._chem_entry_dict[row] = ttk.Entry(master=_frame_input)
            self._min_entry_dict[row] = ttk.Entry(master=_frame_input, width=5)
            self._max_entry_dict[row] = ttk.Entry(master=_frame_input, width=5)

            self._chem_entry_dict[row].grid(row=self._chem_entry_starting_row + row, column=0, columnspan=6, sticky='ensw')
            self._min_entry_dict[row].grid(row=self._chem_entry_starting_row + row, column=6, sticky='ensw')
            self._max_entry_dict[row].grid(row=self._chem_entry_starting_row + row, column=7, sticky='ensw')

        # edit chemical entries buttons
        self._btn_dict["increase_capacity"] = ttk.Button(master=_frame_input, text='+')
        self._btn_dict["decrease_capacity"] = ttk.Button(master=_frame_input, text='-')

        self._btn_dict["increase_capacity"].grid(row=self._chem_entry_starting_row + self._number_of_chemical_entries,
                                                 column=0, sticky='ew')
        self._btn_dict["decrease_capacity"].grid(row=self._chem_entry_starting_row + self._number_of_chemical_entries,
                                                 column=1, sticky='ew')

        # Submission Buttons
        self._btn_dict["submit"] = ttk.Button(master=_frame_input, text='>>')
        self._btn_dict["clear"] = ttk.Button(master=_frame_input, text='C')

        offset = self._chem_entry_starting_row + self._number_of_chemical_entries + 1
        self._btn_dict["clear"].grid(row=offset, column=6, sticky='senw')
        self._btn_dict["submit"].grid(row=offset, column=7, sticky='snwe')


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


    def increment_chemical_entries(self, event):
        pass


    def decrement_chemical_entries(self, event):
        pass

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

    def convert_ingredient_to_tuple(self, ingredient: ingredientClass.Ingredient):
        pass