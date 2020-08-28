import tkinter as tk
from tkinter import ttk

from widget_creator_classes import ButtonCreator

#Hello 
HOVER_BG = "#ffffe0"
HEADER_BG = "#00004d"
FONT_BG = "#FFFFFF"
MAIN_BG = "#0066cc"
FONT_COL = "#FFFFFF"
ERROR_FONT = "red"

LARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 14)
SMALL_FONT = ("Verdana", 10)

#Class that creates a topLevel window above the program. Used for configuring settings or setting new tags etc
#This toplevel window works in the program by calling the wait() method after the class instance is called. Then a result is passed to the var when the window is closed. Nothing runs until the window is closed.
class TopLevelWin:
    def __init__(self, title, bg_col, parent_window):
        self.win = tk.Toplevel() #creates the toplevel win
        self.bg_col = bg_col #sets the background colour
        self.win['background'] = self.bg_col #& then sets it
        self.win.grab_set() #only allow one version of win #https://stackoverflow.com/questions/39689046/tkinter-only-allow-one-toplevel-window-instance
        self.win.title(title) #sets the title of the window
        self.win.lift() #https://stackoverflow.com/questions/45214662/tkinter-toplevel-always-in-front #lifts it above any other windows
        self.win.resizable(0, 0) #https://www.geeksforgeeks.org/resizable-method-in-tkinter-python/ #so it cannot be resized

        self.parent_window = parent_window #parent window of the toplevel
        self.buttons = None

        self.window_layout = WindowLayout(self.win)


    #add the header, same standard for all toplevel windows
    def create_header(self, header_col, font, font_col, title):
        self.header = self.window_layout.create_header(title, "top", font)

        # header_frame = tk.Frame(self.win, bg=header_col)
        # header_frame.pack(side="top", fill="x", expand=True) #fill the x only and top
        #
        # label = tk.Label(header_frame, text=title + ":", font=font, bg=header_col, fg=font_col) #header title of the window, may not be title of window itself so kept seperate
        # label.pack(side="top", fill="x", padx=10, pady=10, expand=True)

    #allows the main frame to be customised per class
    def create_main(self, background_col):
        self.main = self.window_layout.create_main()
        return self.main

        # main = tk.Frame(self.win, bg=background_col) #use background colour that is passed through not self.background_col of window
        # main.pack(fill="x", expand=True)
        # return main #return main frame to have contents added on by parent class

        #adds a cancel & confirm button

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

    def create_header(self, title, side, font):
        #header container
        self.header = tk.Frame(master=self.parent, bg=HEADER_BG)
        self.header.pack(side="top", fill="x")

        page_title = tk.Label(self.header, text=title, font=font, foreground=FONT_COL, bg=HEADER_BG)      # Store this as an instance variable
        page_title.pack(side=side, pady=20, padx=20) #20 is not used much in the program but gives a little more space

        return self.header

    def create_main(self):
        self.main = tk.Frame(master=self.parent, bg=MAIN_BG)
        self.main.pack(side="bottom", fill="both", expand=True)
        return self.main

    def get_header(self):
        return self.header

    def get_main(self):
        return self.main


class ResizingCanvas(tk.Canvas):
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
