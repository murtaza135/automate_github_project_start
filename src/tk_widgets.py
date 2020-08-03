import tkinter as tk


class ScrollableFrame(tk.Frame):

    def __init__(self, frame_container, scrollbar_container=None, bg="white", canvas_width=300, scrollbar_geometry_manager="grid", *args, **kwargs):
        super().__init__(frame_container, *args, **kwargs)
        self.config(bg=bg)
        self.frame_container = frame_container
        self.root_controller = root_controller

        if scrollbar_container == None: self.scrollbar_container = frame_container
        elif scrollbar_container == "scrollable_frame": self.scrollbar_container = self
        else: self.scrollbar_container = scrollbar_container
    
        self.canvas = tk.Canvas(self, bg=bg, width=canvas_width, confine=0, bd=0, highlightthickness=0)
        self.scrollbar = AutohideScrollbar(self.scrollbar_container, geometry_manager=scrollbar_geometry_manager, orient="vertical")
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.scrollable_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all"))) # make sure canvas scroll region covers the entire scrollable_frame even when its size changes
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.canvas.yview)
        self.scrollbar.bind_mousewheel_y(self.canvas)
    

    def pack_frame(self, frame_side="left", canvas_side="top", scrollbar_side="right", frame_fill="y"):
        self.pack(side=frame_side, fill=frame_fill, expand=True)
        self.canvas.pack(side=canvas_side, fill="both", expand=True)
        self.scrollbar.pack(side=scrollbar_side, fill="y", expand=False)

    def grid_frame(self, **kwargs):
        raise tk.TclError("cannot use grid with this widget, you may choose to manually grid each element within ScrollableFrame")

    def place_frame(self, **kwargs):
        raise tk.TclError("cannot use place with this widget")


class AutohideScrollbar(tk.Scrollbar):

    def __init__(self, container, geometry_manager="grid", cnf={}, **kwargs):
        super().__init__(container, cnf, **kwargs)
        self.container = container

        if geometry_manager != "pack" and geometry_manager != "grid":
            raise tk.TclError("AutohideScrollbar can only be used with pack or grid")
        self.geometry_manager = geometry_manager


    def set(self, low, high):
        if self.geometry_manager == "pack":
            self.set_pack(low, high)
        elif self.geometry_manager == "grid":
            self.set_grid(low, high)

        tk.Scrollbar.set(self, low, high)

    def set_pack(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.pack_forget()
        else:
            if self.cget("orient") == "horizontal":
                self.pack(fill="x", side="bottom")
            else:
                self.pack(fill="y", side="right")

    def set_grid(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()


    def pack(self, **kwargs):
        if self.geometry_manager == "pack":
            tk.Scrollbar.pack(self, **kwargs)
        else:
            raise tk.TclError("geometry manager is not set to 'pack' upon initialisation of AutohideScrollbar")

    def grid(self, **kwargs):
        if self.geometry_manager == "grid":
            tk.Scrollbar.grid(self, **kwargs)
        else:
            raise tk.TclError("geometry manager is not set to 'grid' upon initialisation of AutohideScrollbar")

    def place(self, **kwargs):
        raise tk.TclError("cannot use 'place' with this widget")


    def bind_mousewheel_y(self, scrolled_widget):
        self.container.bind("<Enter>", lambda event: scrolled_widget.bind_all("<MouseWheel>", lambda event: self.on_mousewheel_y(event, scrolled_widget)))
        self.container.bind("<Leave>", lambda event: scrolled_widget.unbind_all("<MouseWheel>"))

    def on_mousewheel_y(self, event, scrolled_widget):
        # BUG: for some reason, when the mouse pointer is on the scrollbar itself
        # and the user scrolls the bar using the mouse scroll wheel,
        # the scrollbar does not remain within its min and max values

        low = float(scrolled_widget.yview()[0])
        high = float(scrolled_widget.yview()[1])
        units = int(-1*(event.delta/120))

        # if lowest point of scrollbar is at the bottom, and highest point of scrollbar is NOT at the top
        # and user is scrolling up (ie. units > 0)
        if (low <= 0 and high < 1) and units > 0:
            scrolled_widget.yview_scroll(units, "units")

        # if highest point of scrollbar is at the top, and the lowest point of scrollbar is NOT at the bottom
        # and user is scrolling down (ie. units < 0)
        elif (low > 0 and high >= 1.0) and units < 0:
            scrolled_widget.yview_scroll(units, "units")

        # if neither the lowest point of the scrollbar is at the bottom nor the highest is at the top
        elif low > 0 and high < 1:
            scrolled_widget.yview_scroll(units, "units")