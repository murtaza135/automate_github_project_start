from project_creator import ProjectCreator
import tkinter as tk
import tkinter.ttk as ttk
import tk_widgets as tkw
import tk_styles as tks
from tk_styles import Colour, MyTkinterStyle, MyTtkStyle
from tk_tools import TkTools
import tkinter.messagebox as tkpopup
import tkinter.filedialog as tkfile
from github import Github
from my_github import MyGithub
from my_gui_options import MyGuiOptions
import configparser
import os
import concurrent.futures


class TkApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.initialise_paths()
        self.initialise_controller()
        self.initialise_tk(*args, **kwargs)
        self.initialise_styles()
        self.create_widget_frame()

    def initialise_paths(self):
        # self.ICON = "../images/icon.ico"
        self.ICON = "images/icon.ico"
        # self.GITIGNORE_TEMPLATES_FILE = "../config/gitignore_templates.txt"
        self.GITIGNORE_TEMPLATES_FILE = "config/gitignore_templates.txt"

    def initialise_controller(self):
        self.project = ProjectCreator()
        self.gui_options = MyGuiOptions()

    def initialise_tk(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Automate Github Project Start")
        self.iconbitmap(self.ICON)
        self.geometry("575x760")
        self.minsize(575, 760)

    def initialise_styles(self):
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

        self.controller.gui_options.get_default_options_from_config_file()
        self.default_options = self.controller.gui_options.default_options
        self.create_widgets()


    def create_widgets(self):
        self.config(**MyTkinterStyle.FRAME)

        self.widget_frame = tkw.ScrollableFrame(self, scrollbar_container=self.containter, canvas_width=410)
        self.widget_frame.config(**MyTkinterStyle.FRAME)
        self.widget_frame.bind_mousewheel(self)
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

        self.local_directory_path_entry = tk.Entry(self.local_directory_path_frame)
        self.local_directory_path_entry.config(**MyTkinterStyle.ENTRY, state="readonly")
        self.local_directory_path_entry.grid(row=1, column=0, pady=(5, 0), sticky="we")

        self.local_directory_path_dialog_box_button = tk.Button(self.local_directory_path_frame, text="...")
        self.local_directory_path_dialog_box_button.config(**MyTkinterStyle.BUTTON, command=self.get_local_directory_path_and_auto_set_repository_name)
        self.local_directory_path_dialog_box_button.grid(row=1, column=1, padx=(12, 0), pady=(5, 0), sticky="w")

        self.local_repo_only_var = tk.IntVar()
        self.local_repo_only_var.set(self.default_options["local_repo_only"])
        self.local_repo_only_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.local_repo_only_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.local_repo_only_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.local_repo_only_var)
        self.local_repo_only_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Local Repository Only?")
        self.local_repo_only_checkbutton.bind_command(self.activate_deactivate_repository_name_entry)
        self.local_repo_only_checkbutton.pack(padx=10, pady=(30, 0), anchor="w")

        self.repository_name_label = tk.Label(self.widget_frame.scrollable_frame, text="Remote Repository Name")
        self.repository_name_label.config(**MyTkinterStyle.LABEL)
        self.repository_name_label.pack(padx=10, pady=(7, 0), anchor="w")

        self.repository_name_entry = tk.Entry(self.widget_frame.scrollable_frame)
        self.repository_name_entry.config(**MyTkinterStyle.ENTRY)
        self.activate_deactivate_repository_name_entry()
        self.repository_name_entry.pack(padx=10, pady=(5, 0), anchor="w", fill="x", expand=True)

        self.gitignore_combobox_label = tk.Label(self.widget_frame.scrollable_frame, text=".gitignore File")
        self.gitignore_combobox_label.config(**MyTkinterStyle.LABEL)
        self.gitignore_combobox_label.pack(padx=10, pady=(30, 0), anchor="w")

        self.gitignore_combobox_options = self.get_gitiginore_templates_and_save_if_possible()
        self.gitignore_combobox = ttk.Combobox(self.widget_frame.scrollable_frame, value=self.gitignore_combobox_options, width=30, style="General.TCombobox", state="readonly")
        self.gitignore_combobox.option_add("*TCombobox*Listbox*Background", Colour.DARK_3)
        self.gitignore_combobox.option_add("*TCombobox*Listbox.foreground", Colour.BLUE_2)
        self.gitignore_combobox.set(self.default_options["gitignore"])
        self.gitignore_combobox.pack(padx=10, pady=(5, 0), anchor="w", fill="x", expand=True)

        self.create_project_button_1 = tk.Button(self.widget_frame.scrollable_frame, text="Create Project")
        self.create_project_button_1.config(**MyTkinterStyle.BUTTON, command=self.create_project_in_thread)
        self.create_project_button_1.config(font=("Verdana", 16), bg=Colour.BLUE_4, fg=Colour.BLUE_1)
        self.create_project_button_1.pack(padx=10, pady=(50, 0), fill="x", expand=True)

        self.separator_1 = ttk.Separator(self.widget_frame.scrollable_frame, orient="horizontal", style="General.Horizontal.TSeparator")
        self.separator_1.pack(padx=10, pady=(30, 0), fill="x", expand=True)

        self.additional_options_label = tk.Label(self.widget_frame.scrollable_frame, text="Show Additional Options")
        self.additional_options_label.config(**MyTkinterStyle.LABEL)
        self.additional_options_label.config(font=("Verdana", 12, "bold"))
        self.additional_options_label.bind("<Button-1>", lambda event: self.show_additional_options())
        self.additional_options_label.pack(padx=10, pady=(30, 20), anchor="w")

        self.venv_var = tk.IntVar()
        self.venv_var.set(self.default_options["venv"])
        self.venv_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.venv_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.venv_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.venv_var)
        self.venv_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create venv?")

        self.docs_var = tk.IntVar()
        self.docs_var.set(self.default_options["docs"])
        self.docs_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.docs_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.docs_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.docs_var)
        self.docs_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a docs directory?")

        self.logs_var = tk.IntVar()
        self.logs_var.set(self.default_options["logs"])
        self.logs_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.logs_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.logs_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.logs_var)
        self.logs_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a logs directory?")

        self.notes_var = tk.IntVar()
        self.notes_var.set(self.default_options["notes"])
        self.notes_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.notes_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.notes_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.notes_var)
        self.notes_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a notes directory?")

        self.src_var = tk.IntVar()
        self.src_var.set(self.default_options["src"])
        self.src_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.src_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.src_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.src_var)
        self.src_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a src directory?")

        self.tests_var = tk.IntVar()
        self.tests_var.set(self.default_options["tests"])
        self.tests_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.tests_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.tests_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.tests_var)
        self.tests_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a tests directory?")

        self.images_var = tk.IntVar()
        self.images_var.set(self.default_options["images"])
        self.images_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.images_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.images_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.images_var)
        self.images_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create an images directory?")

        self.config_var = tk.IntVar()
        self.config_var.set(self.default_options["config"])
        self.config_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.config_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.config_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.config_var)
        self.config_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a config directory?")

        self.requirements_var = tk.IntVar()
        self.requirements_var.set(self.default_options["requirements"])
        self.requirements_checkbutton = tkw.TextSeparatedCheckbutton(self.widget_frame.scrollable_frame)
        self.requirements_checkbutton.config_frame(**MyTkinterStyle.FRAME)
        self.requirements_checkbutton.config_checkbutton(bg=Colour.DARK_3, variable=self.requirements_var)
        self.requirements_checkbutton.config_text_label(**MyTkinterStyle.LABEL, text="Create a requirements.txt file?")

        self.create_project_button_2 = tk.Button(self.widget_frame.scrollable_frame, text="Create Project")
        self.create_project_button_2.config(**MyTkinterStyle.BUTTON, command=self.create_project_in_thread)
        self.create_project_button_2.config(font=("Verdana", 16), bg=Colour.BLUE_4, fg=Colour.BLUE_1)

        self.progress_bar = ttk.Progressbar(self.widget_frame.scrollable_frame, orient="horizontal", mode='indeterminate', style="General.Horizontal.TProgressbar")

        self.progress_label = tk.Label(self.widget_frame.scrollable_frame, text="Creating Project... Please Wait")
        self.progress_label.config(**MyTkinterStyle.LABEL)
        self.progress_label.config(anchor="center")

        self.open_vscode_button = tk.Button(self.widget_frame.scrollable_frame, text="Open VS Code")
        self.open_vscode_button.config(**MyTkinterStyle.BUTTON, command=self.open_vscode_and_close_program)
        self.open_vscode_button.config(font=("Verdana", 16), bg=Colour.BLUE_4, fg=Colour.BLUE_1)

    def get_local_directory_path_and_auto_set_repository_name(self):
        self.get_local_directory_path()
        self.set_repository_name_based_upon_directory_name()

    def get_local_directory_path(self):
        directory_path = tkfile.askdirectory(title="Choose Project Path")
        if directory_path == "": return
        self.local_directory_path_entry.config(state="normal")
        self.local_directory_path_entry.delete(0, "end")
        self.local_directory_path_entry.insert("end", directory_path.strip())
        self.local_directory_path_entry.xview_moveto(1)
        self.local_directory_path_entry.config(state="readonly")

    def set_repository_name_based_upon_directory_name(self):
        parent_directory_folder_name = os.path.basename(self.local_directory_path_entry.get())
        parent_directory_folder_name = parent_directory_folder_name.lower().replace(" ", "_")
        self.repository_name_entry.config(state="normal")
        self.repository_name_entry.delete(0, "end")
        self.repository_name_entry.insert("end", parent_directory_folder_name)
        self.activate_deactivate_repository_name_entry()

    def activate_deactivate_repository_name_entry(self):
        if self.local_repo_only_var.get() == True:
            self.repository_name_entry.config(state="disabled")
        else:
            self.repository_name_entry.config(state="normal")

    def get_gitiginore_templates_and_save_if_possible(self):
        try:
            gitignore_templates = MyGithub.get_all_gitignore_templates()
            self.write_gitignore_templates_to_file(gitignore_templates)
        except:
            tkpopup.showerror("Error", "Could not retrieve .gitignore templates from Github. Loading cached .gitignore templates instead (which may be out of date).")
            gitignore_templates = self.read_gitignore_templates_from_file()
        
        gitignore_templates.insert(0, "None")
        return gitignore_templates

    def write_gitignore_templates_to_file(self, gitignore_templates):
        with open(self.controller.GITIGNORE_TEMPLATES_FILE, "w") as f:
            f.writelines([f"{template}\n" for template in gitignore_templates[:-1]])
            f.write(gitignore_templates[-1])

    def read_gitignore_templates_from_file(self):
        with open(self.controller.GITIGNORE_TEMPLATES_FILE, "r") as f:
            gitignore_templates = f.read() # returns templates in a giant STRING, not in a list
            gitignore_templates = [template for template in gitignore_templates.split("\n")] # templates separated out into a list
        
        return gitignore_templates

    def show_additional_options(self):
        self.additional_options_label.config(text="Additional Options:", font=("Verdana", 12))
        
        self.venv_checkbutton.pack(padx=20, pady=(0, 0), anchor="w")
        self.docs_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")
        self.logs_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")
        self.notes_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")
        self.src_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")
        self.tests_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")
        self.images_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")
        self.config_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")
        self.requirements_checkbutton.pack(padx=20, pady=(15, 0), anchor="w")

        self.create_project_button_2.pack(padx=10, pady=(50, 30), fill="x", expand=True)

    def create_project_in_thread(self):
        self.open_vscode_button.pack_forget()
        self.progress_bar.pack(pady=(0, 5), fill="x", expand=True)
        self.progress_label.pack(pady=(0, 30))
        self.progress_bar.start()

        self.change_state_of_all_children_widgets(state="disabled")
        self.revert_state_of_specific_widgets_in_disabled()
        self.remove_all_binds()

        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.executor.submit(self.create_project_and_show_errors)

    def finish_create_project_thread(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
        self.open_vscode_button.pack(padx=10, pady=(30, 30), fill="x", expand=True)
        
        self.change_state_of_all_children_widgets(state="normal")
        self.revert_state_of_specific_widgets_in_normal()
        self.re_add_all_binds()

        self.executor.shutdown(wait=True)

    def create_project_and_show_errors(self):
        self.controller.project.set_all_options(
            local_repo_only=self.local_repo_only_var.get(),
            repository_name=self.repository_name_entry.get() if self.repository_name_entry.get() != "" else None,
            local_directory_path=self.local_directory_path_entry.get() if self.local_directory_path_entry.get() != "" else None,
            venv=self.venv_var.get(),
            docs=self.docs_var.get(),
            logs=self.logs_var.get(),
            notes=self.notes_var.get(),
            src=self.src_var.get(),
            tests=self.tests_var.get(),
            images=self.images_var.get(),
            config=self.config_var.get(),
            requirements=self.requirements_var.get(),
            gitignore=self.gitignore_combobox.get()
        )

        try:
            self.controller.project.create_project()
        except Exception as e:
            tkpopup.showerror("Error", e)

        if len(self.controller.project.errors) == 1:
            tkpopup.showwarning("Warning", "An error has occurred in the creation of your project. Please check the 'agps_errors.txt' file.")
        elif len(self.controller.project.errors) > 1:
            tkpopup.showwarning("Warning", "Multiple errors have occurred in the creation of your project. Please check the 'agps_errors.txt' file.")
        else:
            tkpopup.showinfo("Project Created", "Project has been created!")

        self.finish_create_project_thread()

    def change_state_of_all_children_widgets(self, state):
        # adapted from https://stackoverflow.com/questions/51902451/how-to-enable-and-disable-frame-instead-of-individual-widgets-in-python-tkinter/52152773
        # and from https://stackoverflow.com/questions/24942760/is-there-a-way-to-gray-out-disable-a-tkinter-frame

        WIDGETS_WITHOUT_STATE = ("Frame","Labelframe", "TSeparator", "TProgressbar")

        def change_state_of_children(widget):
            if widget.winfo_children():
                for child in widget.winfo_children():
                    if child.winfo_class() not in WIDGETS_WITHOUT_STATE:
                        child.config(state=state)
                    change_state_of_children(child)

        change_state_of_children(self)

    def revert_state_of_specific_widgets_in_disabled(self):
        self.logo.config(state="normal")
        self.progress_label.config(state="normal")

    def revert_state_of_specific_widgets_in_normal(self):
        self.local_directory_path_entry.config(state="readonly")
        self.gitignore_combobox.config(state="readonly")
        self.activate_deactivate_repository_name_entry()

    def remove_all_binds(self):
        self.local_repo_only_checkbutton.unbind_command()
        self.additional_options_label.unbind("<Button 1>")

    def re_add_all_binds(self):
        self.local_repo_only_checkbutton.bind_command(self.activate_deactivate_repository_name_entry)
        self.additional_options_label.bind("<Button-1>", lambda event: self.show_additional_options())

    def open_vscode_and_close_program(self):
        if self.controller.project.local_directory_path != None:
            import os
            os.system(f'code "{self.controller.project.local_directory_path}"')
            self.controller.destroy()