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