from project_creator import ProjectCreator
import tkinter as tk
import tkinter.ttk as ttk
import tk_widgets as wtk
import tkinter.messagebox as tk_popup
import tkinter.filedialog as tk_file
from PIL import Image, ImageTk


class TkApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.initialise_controller()
        self.initialise_tk(*args, **kwargs)
        self.create_widget_frame()

    def initialise_controller(self):
        self.project = ProjectCreator()

    def initialise_tk(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Automate Github Project Start")
        self.iconbitmap("")
        self.geometry("1024x768")
        self.minsize(1024, 768)

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
        self.widget_frame = wtk.ScrollableFrame(self, scrollbar_container=self.containter, bg="black", canvas_width=400)
        self.widget_frame.pack(side="left", fill="y", expand=True)
        self.widget_frame.canvas.pack(side="top", fill="both", expand=True)
        self.widget_frame.scrollbar.grid(row=0, column=1, sticky="ns")

        self.img = ImageTk.PhotoImage(Image.open("..\\images\\pinterest_profile_image.png"))
        self.logo = tk.Label(self.widget_frame.scrollable_frame, image=self.img)
        self.logo.pack(padx=10, pady=(30, 0))

        