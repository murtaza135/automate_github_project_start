from project_creator import ProjectCreator
import tkinter as tk
import tkinter.ttk as ttk
import tk_widgets as tkw
import tk_styles as tks
from tk_styles import Colour, MyTkinterStyle, MyTtkStyle
from tk_tools import TkTools
import tkinter.messagebox as tkpopup
import tkinter.filedialog as tkfile


class TkApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.initialise_tk(*args, **kwargs)
        self.initialise_controller()
        self.create_widget_frame()

    def initialise_tk(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Automate Github Project Start")
        # self.iconbitmap("../images/icon.ico")
        self.iconbitmap("images/icon.ico")
        self.geometry("575x740") # "575x685"
        self.minsize(575, 685)

    def initialise_controller(self):
        self.project = ProjectCreator()
        self.style = MyTtkStyle("clam")
        self.style.create_all_premade_styles()

    def create_widget_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.widget_frame = WidgetFrame(container=self, controller=self)
        self.widget_frame.grid(row=0, column=0, sticky="nsew")


class WidgetFrame(tk.Frame):
    
    def __init__(self, container, controller):
        super().__init__(container)
        self.containter = container
        self.controller = controller

        self.create_widgets()

    
    def create_widgets(self):
        self.config(**MyTkinterStyle.FRAME)

        self.widget_frame = tkw.ScrollableFrame(self, scrollbar_container=self.containter, canvas_width=410)
        self.widget_frame.config(**MyTkinterStyle.FRAME)
        self.widget_frame.pack(side="left", fill="y", expand=True)
        self.widget_frame.canvas.pack(side="top", fill="both", expand=True)
        self.widget_frame.scrollbar.grid(row=0, column=1, sticky="ns")

        # self.img = TkTools.get_image_tk_resized("../images/main logo with text - clear background.png")
        self.img = TkTools.get_image_tk_resized("images/main logo with text - clear background.png", width=385, height=162)
        self.logo = tk.Label(self.widget_frame.scrollable_frame, image=self.img)
        self.logo.config(**MyTkinterStyle.IMAGE)
        self.logo.pack(padx=10, pady=(30, 0))

        self.local_directory_path_frame = tk.Frame(self.widget_frame.scrollable_frame)
        self.local_directory_path_frame.config(**MyTkinterStyle.FRAME)
        self.local_directory_path_frame.pack(padx=10, pady=(40, 0), anchor="w", fill="x", expand=True)
        self.local_directory_path_frame.grid_columnconfigure(0, weight=1)

        self.local_directory_path_label = tk.Label(self.local_directory_path_frame, text="Path to Directory")
        self.local_directory_path_label.config(**MyTkinterStyle.LABEL)
        self.local_directory_path_label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.local_directory_path_entry = tk.Entry(self.local_directory_path_frame, state="readonly")
        self.local_directory_path_entry.config(**MyTkinterStyle.ENTRY)
        # self.local_directory_path_entry.xview_moveto(1)
        self.local_directory_path_entry.grid(row=1, column=0, pady=(5, 0), sticky="we")

        self.local_directory_path_dialog_box_button = tk.Button(self.local_directory_path_frame, text="...")
        self.local_directory_path_dialog_box_button.config(**MyTkinterStyle.BUTTON)
        self.local_directory_path_dialog_box_button.grid(row=1, column=1, padx=(12, 0), pady=(5, 0), sticky="w")

        self.local_repo_only_var = tk.IntVar()
        self.local_repo_only_var.set(False)
        self.local_repo_only_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.local_repo_only_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.local_repo_only_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.local_repo_only_var)
        self.local_repo_only_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Local Repository Only?")
        self.local_repo_only_checkbutton.pack(padx=10, pady=(30, 0), anchor="w")

        self.repository_name_label = tk.Label(self.widget_frame.scrollable_frame, text="Repository Name")
        self.repository_name_label.config(**MyTkinterStyle.LABEL)
        self.repository_name_label.pack(padx=10, pady=(7, 0), anchor="w")

        self.repository_name_entry = tk.Entry(self.widget_frame.scrollable_frame)
        self.repository_name_entry.config(**MyTkinterStyle.ENTRY)
        self.repository_name_entry.pack(padx=10, pady=(5, 0), anchor="w", fill="x", expand=True)

        self.gitignore_combobox_label = tk.Label(self.widget_frame.scrollable_frame, text=".gitignore File")
        self.gitignore_combobox_label.config(**MyTkinterStyle.LABEL)
        self.gitignore_combobox_label.pack(padx=10, pady=(30, 0), anchor="w")

        self.gitignore_combobox_options = ("None",) + ("Python", "C", "C++")
        self.gitignore_combobox = ttk.Combobox(self.widget_frame.scrollable_frame, value=self.gitignore_combobox_options, width=30, style="General.TCombobox", state="readonly")
        self.gitignore_combobox.option_add("*TCombobox*Listbox*Background", Colour.DARK_3)
        self.gitignore_combobox.option_add("*TCombobox*Listbox.foreground", Colour.BLUE_2)
        self.gitignore_combobox.set(self.gitignore_combobox_options[0])
        self.gitignore_combobox.pack(padx=10, pady=(5, 0), anchor="w", fill="x", expand=True)

        self.create_project_button_1 = tk.Button(self.widget_frame.scrollable_frame, text="Create Project")
        self.create_project_button_1.config(**MyTkinterStyle.BUTTON)
        self.create_project_button_1.config(font=("Verdana", 16), bg=Colour.BLUE_4, fg=Colour.BLUE_1)
        self.create_project_button_1.pack(padx=10, pady=(50, 0), fill="x", expand=True)

        self.separator_1 = ttk.Separator(self.widget_frame.scrollable_frame, orient="horizontal", style="General.Horizontal.TSeparator")
        self.separator_1.pack(padx=10, pady=(30, 0), fill="x", expand=True)

        self.extra_options_label = tk.Label(self.widget_frame.scrollable_frame, text="Extra Options:")
        self.extra_options_label.config(**MyTkinterStyle.LABEL)
        self.extra_options_label.pack(padx=10, pady=(50, 0), anchor="w")

        self.venv_var = tk.IntVar()
        self.venv_var.set(True)
        self.venv_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.venv_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.venv_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.venv_var)
        self.venv_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create venv?")
        self.venv_checkbutton.pack(padx=20, pady=(20, 0), anchor="w")

        self.docs_var = tk.IntVar()
        self.docs_var.set(True)
        self.docs_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.docs_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.docs_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.docs_var)
        self.docs_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a docs directory?")
        self.docs_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.logs_var = tk.IntVar()
        self.logs_var.set(True)
        self.logs_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.logs_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.logs_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.logs_var)
        self.logs_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a logs directory?")
        self.logs_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.notes_var = tk.IntVar()
        self.notes_var.set(True)
        self.notes_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.notes_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.notes_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.notes_var)
        self.notes_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a notes directory?")
        self.notes_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.src_var = tk.IntVar()
        self.src_var.set(True)
        self.src_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.src_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.src_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.src_var)
        self.src_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a src directory?")
        self.src_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.tests_var = tk.IntVar()
        self.tests_var.set(True)
        self.tests_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.tests_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.tests_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.tests_var)
        self.tests_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a tests directory?")
        self.tests_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.images_var = tk.IntVar()
        self.images_var.set(True)
        self.images_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.images_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.images_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.images_var)
        self.images_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create an images directory?")
        self.images_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.requirements_var = tk.IntVar()
        self.requirements_var.set(True)
        self.requirements_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.requirements_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.requirements_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.requirements_var)
        self.requirements_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a requirements.txt file?")
        self.requirements_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.open_vscode_var = tk.IntVar()
        self.open_vscode_var.set(True)
        self.open_vscode_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.open_vscode_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.open_vscode_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.open_vscode_var)
        self.open_vscode_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Open vscode?")
        self.open_vscode_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.create_project_button_2 = tk.Button(self.widget_frame.scrollable_frame, text="Create Project")
        self.create_project_button_2.config(**MyTkinterStyle.BUTTON)
        self.create_project_button_2.config(font=("Verdana", 16), bg=Colour.BLUE_4, fg=Colour.BLUE_1)
        self.create_project_button_2.pack(padx=10, pady=(50, 30), fill="x", expand=True)