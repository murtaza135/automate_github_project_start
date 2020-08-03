from project_creator import ProjectCreator
import tkinter as tk
import tkinter.ttk as ttk
import tk_widgets as wtk
import tkinter.messagebox as tk_popup
import tkinter.filedialog as tk_file


class MyGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.initialise_controller()
        self.initialise_tk(*args, **kwargs)

    def initialise_controller(self):
        project = ProjectCreator()

    def initialise_tk(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Automate Github Project Start")
        self.iconbitmap("")
        self.geometry("1024x768")
        self.minsize(1024, 768)

    def create_widget_frame(self):
        self.widget_frame = frame_type(parent=self.container, controller=self)
        self.widget_frame.grid(row=0, column=0, sticky="nsew")


class WidgetFrame(tk.Frame):
    
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.create_widgets()

    
    def create_widgets(self):
        pass



if __name__ == "__main__":
    app = MyGUI()
    app.mainloop()