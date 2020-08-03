

class ScrollableFrame(tk.Frame):
    def __init__(self, frame_container, scrollbar_container=None, root_controller=None, *args, **kwargs):
        # NOTE: if root_controller != None, then resizing canvas will be used
        
        # default options
        options = self.options = {
            "bg": "white",
            "canvas_resize": False,
            "canvas_width": 300,
            "canvas_min_width": None,
            "horizontal_scrollbar": False,
            "scrollbar_autohide": True,
            "scrollbar_geometry": "pack"
        }

        # change options based upon kwargs
        for option in options:
            if option in kwargs:
                options[option] = kwargs[option]
                del kwargs[option] # item must not remain in kwargs so that super().__init__ can use kwargs that it requires
        

        super().__init__(frame_container, *args, **kwargs)
        self.frame_container = frame_container
        self.root_controller = root_controller

        if scrollbar_container == None: self.scrollbar_container = frame_container
        elif scrollbar_container == "scrollable_frame": self.scrollbar_container = self
        else: self.scrollbar_container = scrollbar_container

        if self.root_controller != None:
            self.canvas = ResizingCanvas(self, self.root_controller, canvas_min_width=options["canvas_min_width"], width=options["canvas_width"], bg=options["bg"], confine=0, bd=0, highlightthickness=0)
        else:
            self.canvas = tk.Canvas(self, width=options["canvas_width"], bg=options["bg"], confine=0, bd=0, highlightthickness=0)
        
        self.scrollbar = AutohideScrollbar(self.scrollbar_container, autohide=options["scrollbar_autohide"], geometry=options["scrollbar_geometry"], orient="vertical", command=self.canvas.yview)
        if options["horizontal_scrollbar"] == True: self.horizontal_scrollbar = AutohideScrollbar(self.scrollbar_container, autohide=options["scrollbar_autohide"], geometry=options["scrollbar_geometry"], orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=options["bg"]) # widgets are added into this frame
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))) # adjust scroll region to be size of scrollable frame changes
        
        if options["canvas_min_width"] != None and self.canvas.winfo_reqwidth() < options["canvas_min_width"]: width = options["canvas_min_width"]
        else: width = self.canvas.winfo_reqwidth()
        self.window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=width) # keep size of scrollable frame the same as the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        if options["horizontal_scrollbar"] == True: self.canvas.configure(xscrollcommand=self.horizontal_scrollbar.set)
        self.scrollbar.bind_mousewheel_y(self.canvas)
    

    def pack_frame(self, frame_side="left", canvas_side="top", scrollbar_side="right", frame_fill="y"):
        if self.options["horizontal_scrollbar"] == True: self.horizontal_scrollbar.pack(side="bottom", fill="x", expand=False)
        self.pack(side=frame_side, fill=frame_fill, expand=True)
        self.canvas.pack(side=canvas_side, fill="both", expand=True)
        self.scrollbar.pack(side=scrollbar_side, fill="y", expand=False)

    def grid_frame(self, **kwargs):
        raise tk.TclError("cannot use grid with this widget, you may choose to manually grid each element within ScrollableFrame")

    def place_frame(self, **kwargs):
        raise tk.TclError("cannot use place with this widget")





class ResizingCanvas(tk.Canvas):

    WINDOW_TO_CANVAS_DELTA = 455
    binded_canvases = []

    def __init__(self, container, root_controller, canvas_min_width=None, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        bind_details = {
            "canvas": self,
            "container": container,
            "root_controller": root_controller,
            "tk_window_width": root_controller.winfo_width(),
            "my_width": root_controller.winfo_width() - ResizingCanvas.WINDOW_TO_CANVAS_DELTA,
            "canvas_min_width": canvas_min_width
        }

        self.config(width=bind_details["my_width"])
        ResizingCanvas.binded_canvases.append(bind_details)
        root_controller.bind("<Configure>", ResizingCanvas.on_resize)


    @staticmethod
    def on_resize(event):
        for canvas in ResizingCanvas.binded_canvases:
            try:
                if canvas["root_controller"].winfo_width() != canvas["tk_window_width"]:
                    canvas["tk_window_width"] = canvas["root_controller"].winfo_width()
                    canvas["my_width"] = canvas["tk_window_width"] - ResizingCanvas.WINDOW_TO_CANVAS_DELTA


                    if canvas["canvas_min_width"] != None and (canvas["my_width"] < canvas["canvas_min_width"]):
                        canvas["canvas"].itemconfigure(canvas["container"].window, width=canvas["canvas_min_width"])
                    else:
                        canvas["canvas"].itemconfigure(canvas["container"].window, width=canvas["my_width"])
                    canvas["canvas"].config(width=canvas["my_width"])
                    
                    
            except:
                print(canvas, "skipped")
                try: ResizingCanvas.binded_canvases.remove(canvas)
                except: pass





class AutohideScrollbar(tk.Scrollbar):

    def __init__(self, container, geometry="grid", cnf={}, **kwargs):
        super().__init__(container, cnf, **kwargs)
        if geometry != "pack" and geometry != "grid":
            raise tk.TclError("AutohideScrollbar can only be used with pack or grid")
        self.container = container
        self.geometry = geometry


    def set(self, low, high):
        if self.geometry == "pack":
            self.set_pack(low, high)
        elif self.geometry == "grid":
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
        if self.geometry == "pack":
            tk.Scrollbar.pack(self, **kwargs)
        else:
            raise tk.TclError("geometry is not set to 'pack' upon initialisation of AutohideScrollbar")

    def grid(self, **kwargs):
        if self.geometry == "grid":
            tk.Scrollbar.grid(self, **kwargs)
        else:
            raise tk.TclError("geometry is not set to 'grid' upon initialisation of AutohideScrollbar")

    def place(self, **kwargs):
        raise tk.TclError("cannot use 'place' with this widget")

    def bind_mousewheel_y(self, scrolled_widget):
        self.container.bind("<Enter>", lambda event: scrolled_widget.bind_all("<MouseWheel>", lambda event: self.on_mousewheel_y(event, scrolled_widget)))
        self.container.bind("<Leave>", lambda event: scrolled_widget.unbind_all("<MouseWheel>"))

    def on_mousewheel_y(self, event, scrolled_widget):
        # BUG: for some reason, when the mouse pointer is on the scrollbar itself
        # and the user scrolls the bar using the mouse scroll wheel,
        # the scrollbar goes out of bounds

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