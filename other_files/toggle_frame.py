import tkinter as tk
from tkinter import ttk

#CLass for toggled frame, it initialises a frame
class ToggledFrame(tk.Frame):
    def __init__(self, parent_frame, title, sub_frame_color, parent):
        tk.Frame.__init__(self, parent_frame, relief="raised", borderwidth=1)     #create the frame
        self.title = title #title
        self.parent = parent

        #Variable for opening/closing 1 or 0
        self.show = tk.IntVar()
        self.show.set(0) #set as closed

        #the frame for the label (title) & + or - btn
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        #label for that frame
        ttk.Label(self.title_frame, text=self.title).pack(side="left", fill="x", expand=1)

        #toggle button for opening title frame
        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text=' +', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        #sub frame
        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1, bg=sub_frame_color)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text=' -')
            self.parent.tab_toggle_open(self.title) #call parent & look to close all other toggles
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text=' +')

    def open(self): #to see if the toggle is open
        return self.show.get()

    def close(self): #to see if the toggle is closed 
        self.sub_frame.forget()
        self.toggle_button.configure(text=' +')

    def get_sub_frame(self):
        return self.sub_frame
