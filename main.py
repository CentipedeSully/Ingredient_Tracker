from Utilities import *
from gui_window import *


def main():
    root = tk.Tk()
    title_str = "Ingredient Tracker"
    window_width = 1000
    window_height = 700
    window = GuiWindow(root, title_str, window_width, window_height)


main()

