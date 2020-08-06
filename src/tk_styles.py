import tkinter.ttk as ttk


class Colour:
    DARK_1 = "black"
    DARK_2 = "#282828"
    DARK_3 = "#2f3437"

    GREY_1 = "#474c50"
    GREY_2 = "#54585B"
    GREY_3 = "#8f9295"

    BLUE_1 = "#ceeef1"
    BLUE_2 = "#41c1c8"
    BLUE_3 = "#329aa1"
    BLUE_4 = "#1f6064"

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
        "font": ("Verdana", 12),
        "height": 1,
        "anchor": "w",
        "padx": 0,
        "bg": Colour.DARK_3,
        "fg": Colour.BLUE_2,
        "relief": "flat"
    }

    ENTRY = {
        "font": ("Verdana", 18),
        "bg": Colour.DARK_3,
        "readonlybackground": Colour.DARK_3,
        "disabledbackground": Colour.GREY_2,
        "fg": Colour.BLUE_2,
        "highlightcolor": Colour.BLUE_2,
        "highlightbackground": Colour.BLUE_2,
        "highlightthickness": 2,
        "relief": "flat"
    }

    BUTTON = {
        "font": ("Verdana", 13),
        "height": 1,
        "anchor": "center",
        "padx": 10,
        "bg": Colour.GREY_1,
        "fg": Colour.BLUE_2,
        "relief": "raised"
    }

    CHECKBUTTON = {
        "font": ("Verdana", 12),
        "bg": Colour.DARK_3,
        "fg": Colour.BLUE_2
    }

    IMAGE = {
        "bg": Colour.DARK_3
    }


class MyTtkStyle(ttk.Style):
        
    def __init__(self, theme):
        super().__init__()
        self.theme_use(theme)

    def create_all_premade_styles(self):
        self.create_style_general_tcombobox()
        self.create_style_general_tseparator()
        self.create_style_general_tprogressbar()

    def create_style_general_tcombobox(self):
        self.configure("General.TCombobox",
            background=Colour.DARK_3,
            foreground=Colour.BLUE_2,
            bordercolor=Colour.BLUE_2,
            padding=(7, 8, 0, 8)
        )
        self.map("General.TCombobox",
            focusfill=[("readonly", Colour.DARK_3)],
            selectforeground=[("readonly", Colour.BLUE_2)],
            foreground=[('disabled', 'SystemGrayText'), ('readonly', Colour.BLUE_2)],
            selectbackground=[("readonly", Colour.DARK_3)],
            fieldbackground=[("readonly", Colour.DARK_3)],
            background=[("readonly", Colour.DARK_3)],
            bordercolor=[("readonly", Colour.BLUE_2)]
        )

    def create_style_general_tseparator(self):
        self.configure("General.Horizontal.TSeparator",
            background=Colour.BLUE_2,
            foreground=Colour.BLUE_2,
        )

    def create_style_general_tprogressbar(self):
        self.configure("General.Horizontal.TProgressbar",
            troughcolor=Colour.DARK_3,
            background=Colour.BLUE_2,
            lightcolor=Colour.BLUE_2,
            darkcolor=Colour.BLUE_2
        )