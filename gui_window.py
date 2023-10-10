from tkinter import *


class GuiWindow:
    def __init__(self, root_window, title_str, window_width, window_height):

        # INITIALIZE:
        self.root = root_window
        self.title = title_str
        self.width = window_width
        self.height = window_height

        self.root.title(title_str)

        self.number_of_chemical_entries = 3



        # HEADER AND BODY: create & configure
        _frame_header = Frame(master = self.root, bg="grey",
                                    width = window_width, height= 27)

        _frame_body = Frame(master = self.root, bd=10, bg= "white",
                                 width = window_width, height = window_height - 27)

        _frame_header.pack(fill = X)
        _frame_body.pack(fill = BOTH, expand= True)

        _frame_body.columnconfigure(index = 0, weight = 30)
        _frame_body.columnconfigure(index = 1, weight = 70)

        _frame_body.rowconfigure(index = [0, 2], weight = 15)
        _frame_body.rowconfigure(index= 1, weight = 70)



        # INPUT AND DISPLAY: create & configure
        _frame_input = Frame(master = _frame_body, bg= "orange", width= 100, height= 100)
        _frame_display = Frame(master = _frame_body, bg= "yellow", width= 300, height= 100)

        _frame_input.grid(row= 1, column= 0, sticky= 'enw')
        _frame_display.grid(row= 0, rowspan=3, column= 1, sticky= 'nesw')

        row_indexes = list(range(0,10))
        column_indexes = list(range(0,9))
        _frame_input.rowconfigure(index = row_indexes, weight= 1)
        _frame_input.columnconfigure(index = column_indexes, weight =1)

        # cell_width= 40
        # cell_height= 40
        # row_spacers_dict= dict()
        # for row in range(0,7 + self.number_of_chemical_entries):
        #    for column in range(0, 8):
        #        row_spacers_dict[(row,column)] = Frame(master=_frame_input, width= cell_width, height= cell_height, bg = 'blue',
        #                                               borderwidth= 1, relief= 'solid')
        #        row_spacers_dict[(row,column)].grid(row= row, column= column)

        # INPUT CONTENTS:
        # contextual buttons
        _button_search = Button(master = _frame_input, text = 'Search')
        _button_add = Button(master = _frame_input, text = 'Add')
        _button_remove = Button(master = _frame_input, text = 'Remove')

        _button_search.grid(row = 0, column = 0, columnspan = 2, sticky= 'esw')
        _button_add.grid(row = 0, column = 2, columnspan = 2, sticky= 'esw')
        _button_remove.grid(row = 0, column = 4, columnspan= 2, sticky= 'esw')

        # labels
        _label_ingredent = Label(master=_frame_input, text= "Ingredient:", anchor= 'sw')
        _label_chemical = Label(master=_frame_input, text= "Chemicals:", anchor= 'sw')
        _label_quantity = Label(master=_frame_input, text= "Qty:", anchor= 'sw')

        _label_ingredent.grid(row=1, column=0, columnspan= 8, sticky= 'ensw', ipadx= 10)
        _label_chemical.grid(row=4, column=0, columnspan= 6, sticky= 'ensw', ipadx= 10)
        _label_quantity.grid(row=4, column=6, columnspan=2, sticky= 'ensw', ipadx= 10)

        #entries
        _entry_ingredient = Entry(master=_frame_input)
        _entry_ingredient.grid(row= 2, column= 0, columnspan = 8, sticky= 'ew')

        self.chem_entry_starting_row = 5
        chem_entry_dict= dict()
        min_entry_dict = dict()
        max_entry_dict = dict()

        for row in range(0,self.number_of_chemical_entries):
            chem_entry_dict[row] = Entry(master=_frame_input)
            min_entry_dict[row] = Entry(master=_frame_input, width= 5)
            max_entry_dict[row] = Entry(master=_frame_input, width= 5)

            chem_entry_dict[row].grid(row= self.chem_entry_starting_row + row, column= 0, columnspan=6, sticky='ew')
            min_entry_dict[row].grid(row= self.chem_entry_starting_row + row, column= 6, sticky='ew')
            max_entry_dict[row].grid(row= self.chem_entry_starting_row + row, column= 7, sticky='ew')

        # edit chemical entries buttons
        _button_add_chemical = Button(master= _frame_input, text='+')
        _button_remove_chemical = Button(master= _frame_input, text='-')

        _button_add_chemical.grid(row=self.chem_entry_starting_row + self.number_of_chemical_entries, column=0, sticky='ew')
        _button_remove_chemical.grid(row=self.chem_entry_starting_row + self.number_of_chemical_entries, column=1, sticky='ew')

        # Submission Buttons
        _button_confirm = Button(master= _frame_input, text= '>>')
        _button_clear = Button(master= _frame_input, text= 'C')

        offset= self.chem_entry_starting_row+ self.number_of_chemical_entries + 1
        _button_clear.grid(row= offset, column=6, sticky= 'senw')
        _button_confirm.grid(row= offset, column= 7, sticky= 'snwe')








        # labels



        # DISPLAY WINDOW
        mainloop()



