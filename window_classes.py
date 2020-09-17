#Contains classes regarding creating a frame or display
#Follows compartmentalisation design pattern. Classes include TopLevelWin, WindowLayout, ResizingCanvas

import tkinter as tk
from tkinter import ttk

from widget_creator_classes import ButtonCreator #Button creator is used for the controls in the TopLevelWin for standard cancel, confirm controls
from styles import colour_scheme, fonts

#Class that creates a topLevel window above the program. Used for configuring settings or setting new tags etc
#This toplevel window works in the program by calling the wait() method after the class instance is called. Then a result is passed to the var when the window is closed. Nothing runs until the window is closed.
class TopLevelWin:
    def __init__(self, title, bg_col, parent_window):
        self.win = tk.Toplevel() #creates the toplevel win
        self.bg_col = bg_col #sets the background colour
        self.win['background'] = self.bg_col #& then sets it
        self.win.grab_set() #only allow one version of win # Source: Vlijm, J. (2016) Tkinter: Only allow one TopLevel window instance [Online]. Available at: https://stackoverflow.com/questions/39689046/tkinter-only-allow-one-toplevel-window-instance [Accessed: 02 August 2020]
        self.win.title(title) #sets the title of the window
        self.win.lift() #lifts it above any other windows, Source: Norris, R. (2017) Tkinter Toplevel always in front [Online]. Available at: https://stackoverflow.com/questions/45214662/tkinter-toplevel-always-in-front [Accessed: 02 August 2020]
        self.win.resizable(0, 0) #so it cannot be resized, Source: GeeksforGeeks, resizable() method in Tkinter | Python [Online]. Available at: https://www.geeksforgeeks.org/resizable-method-in-tkinter-python/ [Accessed: 02 August 2020]

        self.parent_window = parent_window #parent window of the toplevel
        self.buttons = None

        self.window_layout = WindowLayout(self.win) #uses the standard window layout class


    #add the header, same standard for all toplevel windows
    def create_header(self, header_col, font, font_col, title):
        self.header = self.window_layout.create_header(title, "top", font)

    #allows the main frame to be customised per class
    def create_main(self, background_col):
        self.main = self.window_layout.create_main()
        return self.main

    #create controls of window, cancel & confirm, same for all toplevel windows  - Uses ButtonCreator
    def add_controls(self):
        buttons_frame = tk.Frame(self.main, bg=self.bg_col)
        buttons_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        button_dict = [{"name": "cancel", "command": lambda: self.cancel_btn(), "side":"left", "default_state": "normal", "width":10}, #creates the dict
                    {"name": "confirm", "command": lambda: self.confirm_btn(),"side":"right", "default_state": "normal", "width":10}]

        self.buttons = ButtonCreator(buttons_frame, button_dict)

    #close the window, used by cancel & cofirm selection methods that are required in parent class
    def close_window(self):
        self.win.destroy() #just destroys the window

    #there needs to be a method of cancel_selection in parent class, certain operations may need to be done when the window is cancelled
    def cancel_btn(self):
        try:
            self.parent_window.cancel_selection()
        except:
            print("ERROR occured when trying to close window.")

    #there needs to be a method of confirm_selection in parent class, certain operations may need to be done when the window is confirmed
    def confirm_btn(self):
        try:
            self.parent_window.confirm_selection()
        except:
            print("ERROR occured when trying to close window.")

    #When the confirm btn needs to be disabled, by parent class
    def disable_confirm_btn(self):
        self.buttons.disable_btn("confirm")

    #For when the confirm can be enabled, by parent class
    def enable_confirm_btn(self):
        self.buttons.enable_btn("confirm")

    #Wait to see if the window closes down. This is called when class is called to only pass a message once this window has been closed down.
    def wait(self):
        self.win.deiconify()
        self.win.wait_window()

    #To see if the window exists
    def window_exists(self):
        if self.win.winfo_exists() == 1:
            return True
        else:
            return False

#A class to create a window formatting w/ header & title and main section. I want to put scrolling in here and therefore have scrollers for all windows if needed
class WindowLayout:
    def __init__(self, parent):
        self.parent = parent
        self.header, self.main = None, None

    #Function to create a header container
    def create_header(self, title, side, font):
        self.header = tk.Frame(master=self.parent, bg=colour_scheme['header_bg'])
        self.header.pack(side="top", fill="x")

        page_title = tk.Label(self.header, text=title, font=font, foreground=colour_scheme['font_col'], bg=colour_scheme['header_bg'])      # Store this as an instance variable
        page_title.pack(side=side, pady=20, padx=20) #20 is not used much in the program but gives a little more space
        return self.header

    #Function to create a Main Container
    def create_main(self):
        self.main = tk.Frame(master=self.parent, bg=colour_scheme['main_bg'])
        self.main.pack(side="bottom", fill="both", expand=True)
        return self.main

    #Function to add scrollbars to a frame & have them change dyanmically changing widths & heights
    def add_scrollbars(self, scrollable_frame):
        #I have largelly manipulated multiple examples from online and played around with this for some time. Main used sources:
        #ebarr. (2014) How to get tkinter canvas to dynamically resize to window width [Online]. Available at: https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width [Accessed: 18 August 2020]
        #Gonzo. (2013) Tkinter scrollbar for frame [Online]. Available at: https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame [Accessed: 18 August 2020]

        vscrollbarframe = tk.Frame(scrollable_frame) #vertical scrollbar frame (contains the scrollbar ) - Need the frame as it seems to appear better, if just put scrollbar doesn't work as not it's own frame
        vscrollbarframe.pack(side="right", expand=False, fill="y")

        xscrollbarframe = tk.Frame(scrollable_frame) #horrizontal scrollbar frame (contains the scrollbar)
        xscrollbarframe.pack(side="bottom", expand=False, fill="x")

        # create a canvas object and a vertical scrollbar for scrolling it
        canvas = tk.Canvas(scrollable_frame, bd=0, highlightthickness=0, bg=colour_scheme['main_bg'])
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor="nw")

        vscrollbar = tk.Scrollbar(vscrollbarframe, orient=tk.VERTICAL) #vertical scrollbar
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

        xscrollbar = tk.Scrollbar(xscrollbarframe, orient=tk.HORIZONTAL) #horrizinal scrollbar
        xscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

        xscrollbar.config(command=canvas.xview)
        vscrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vscrollbar.set)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

            # track changes to the canvas and frame width and sync them,
            # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        return self.interior #this is what the contents for that frame is packed onto.

    #get the header frame
    def get_header(self):
        return self.header

    #get the main frame
    def get_main(self):
        return self.main

#*BELOW IS NOT USED BUT KEPT FOR FUTURE USE IF NEEDED*
#A class that is used for dynamic resizing of frame so the scrollbars adjust
class ResizingCanvas(tk.Canvas):
    #Source: ebarr (2014) How to get tkinter canvas to dynamically resize to window width [Online]. Available at: https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width [Accessed: 18 August 2020]
    def __init__(self,parent,**kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)
