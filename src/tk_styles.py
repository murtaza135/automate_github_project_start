import tkinter.ttk as ttk

class MyTtkStyle(ttk.Style):
        
    def __init__(self, theme):
        super().__init__()
        self.theme_use(theme)

    def create_all_premade_styles(self):
        self.create_style_general_tcombobox()

    def create_style_general_tcombobox(self):
        self.configure("General.TCombobox",
            background="white",
            foreground="black",
        )
        self.map("General.TCombobox",
            padding=[("readonly", (7, 8, 0, 8))],
            focusfill=[("readonly", "white")],
            selectforeground=[("readonly", "black")],
            foreground=[('disabled', 'SystemGrayText'), ('readonly', "black")],
            selectbackground=[("readonly", "white")],
            fieldbackground=[("readonly", "white")],
            background=[("readonly", "white")],
        )


class Colour:
    DARK_1 = "black"
    DARK_2 = "#282828"
    DARK_3 = "#2f3437"

    GREY_1 = "#474c50"
    GREY_2 = "#54585B"
    GREY_3 = "#8f9295"

    BLUE_1 = "#41c1c8"

    WHITE_1 = "white"
    WHITE_2 = "#f8f8f8"

    ERROR_1 = "red"
    ERROR_2 = "#FF4D4D"
    WARNING = "yellow"


class MyTkinterStyle:

    FRAME = {
        "bg": Colour.DARK_3
    }

    LABEL = {
        "font": ("Verdana", 14),
        "height": 1,
        "anchor": "w",
        "padx": 10,
        "bg": Colour.DARK_3,
        "fg": Colour.BLUE_1,
        "relief": "flat"
    }

    ENTRY = {
        "font": ("Verdana", 14),
        # "width": 30,
        "bg": Colour.DARK_3,
        "fg": Colour.BLUE_1,
        "highlightcolor": Colour.BLUE_1,
        "highlightbackground": Colour.BLUE_1,
        "highlightthickness": 2,
        "relief": "flat"
    }

    BUTTON = {
        "font": ("Verdana", 14),
        # "width": 35,
        "height": 1,
        "anchor": "center",
        "padx": 10,
        "bg": Colour.DARK_2,
        "fg": Colour.BLUE_1,
        "relief": "raised"
    }

    CHECKBUTTON = {
        "font": ("Verdana", 14),
        "bg": Colour.DARK_3,
        "fg": Colour.BLUE_1
    }

    IMAGE = {
        "bg": Colour.DARK_3
    }