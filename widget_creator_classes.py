import tkinter as tk
from tkinter import ttk
import time, datetime, re

#Class for creating a dynamic textbox
class TextBox:
    def __init__(self, parent_frame, height, width, note):
        self.notebox = tk.Text(parent_frame, height=height, width=width, background="white", foreground="black")
        self.notebox.insert(tk.END, note) #note is already pre-inserted
        self.notebox.pack(fill="x", expand=True, padx=10, pady=10)

    def change_notebox_padding(self, padx, pady):
        self.notebox.pack_forget()
        self.notebox.pack(fill="x", expand=True, padx=padx, pady=pady)

    def clear_notebox(self):
        self.notebox.delete(1.0, tk.END)

    def disable_notebox(self):
        #http://effbot.org/tkinterbook/text.htm
        self.notebox['state'] = 'disabled'
        self.notebox['background'] = 'gray'
        self.notebox['foreground'] = 'white'

    def enable_notebox(self):
        self.notebox['state'] = 'normal'
        self.notebox['background'] = "white"
        self.notebox['foreground'] = "black"

    def replace_text(self, text):
        self.clear_notebox()
        self.notebox.delete("insert linestart", "insert lineend")
        self.notebox.insert(tk.END, text)

    def read_contents(self):
        contents = self.notebox.get(1.0, tk.END)
        return contents

    def bind_click(self, function):
        self.notebox.bind("<Button-1>", lambda e: function())
        #https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

#Class for a box of information with labels & dynamic updates
class InformationBox:
    def __init__(self, parent_frame, pack_side, rows, header, info, background_col, font_col, automatic):
        self.parent_frame = parent_frame #parent frame of the label frame
        self.pack_side = pack_side #uses packing as default
        self.padding = 10 #padding set centrally
        self.rows = rows #number of rows wanted by user
        self.header = header #title of the label frame
        self.info = info #information through dict format to be contained
        self.background_col = background_col #background col of label frame
        self.font_col = font_col #font col of the label frame

        self.dict = [] #this dict is used to store the information from intialisation

        #parent label frame box for contents: I have created the label frame inside the class rather than outside as containing frames is less likely than just labels
        self.content_frame = tk.LabelFrame(self.parent_frame, text = self.header.capitalize() + " :  ", foreground=self.font_col, bg=self.background_col, pady=self.padding, padx=self.padding)
        self.content_frame.pack(side=self.pack_side, pady=self.padding, padx=self.padding)

        #if no frames are to be contained inside then it can be created as the frame does not need to be passed out again
        if automatic:
            self.create_insides(self.info)

    #pass out the frame to be the parent of inner frames that are then created outside
    def get_parent_label_frame(self):
        return self.content_frame

    #create labels and info labels - can either be done through init or not
    def create_insides(self, info):
        row = 0
        column = 0
        padx = (0, 0)
        for key, value in info.items():
            label_header = tk.Label(self.content_frame, text=key.capitalize() + ": ", foreground=self.font_col, bg=self.background_col).grid(row=row, column=column, sticky="W", padx=padx)
            #if a frame is passed through then add it in
            if (type(value) == tk.Frame):
                value.grid(row=row, column=column + 1, sticky="W")
                label_dict = {"name": key, "value": value, "widget": value, "type": "frame"}
            #else just stringify & add in as a label
            else:
                label = tk.Label(self.content_frame, text= str(value), foreground=self.font_col, bg=self.background_col)
                label.grid(row=row, column=column + 1, sticky="W")
                label_dict = {"name": key, "value": value, "widget": label, "type": "text"}
            self.dict.append(label_dict)

            if row != self.rows:
                row += 1
            if row == self.rows:
                column += 2
                row = 0
                padx = (25, 0)

    #reset the text labels created to not applicable, better than re-creating widget
    def reset_to_na(self):
        for line in self.dict:
            if line['type'] == "text":
                line['widget']['text'] = "n/a"
                line['value'] = "n/a"

    def present_no_value(self):
        for line in self.dict:
            if line['type'] == "text":
                line['widget']['text'] = ""
                line['value'] = ""

    #Takes in a dict of key value pairs for the current ones already installed & if label widgets, changes the text
    def refresh_information(self, information):
        for key, value in information.items():
            for line in self.dict:
                if ((line['name'] == key) and (line['type'] == "text")):
                    line['widget']['text'] = value
                    line['value'] = value

    #Pulls a detail from the dictionary
    def pull_detail(self, label):
        detail = None
        for line in self.dict:
            if ((line['name'] == label) and (line['type'] == "text")):
                detail = line['value']
        return detail #if returns None then not present

    #forgets the whole frame
    def make_box_go_walkies(self):
        self.content_frame.pack_forget()

    #Changes the formatting to grid for the frame
    def change_to_grid(self, row, col, sticky, columnspan):
        self.make_box_go_walkies()
        self.content_frame.grid(row=row, column=col, sticky=sticky, columnspan=columnspan, padx=self.padding, pady=self.padding)

#Class for creating buttons
class ButtonCreator:
    def __init__(self, parent_frame, dict):
        self.parent_frame = parent_frame
        self.buttons = dict
        self.create_buttons()

    def create_buttons(self):
        for btn in self.buttons:
            button = ttk.Button(self.parent_frame, text=btn['name'].capitalize(), command= lambda function=btn['command']: function(), state=btn['default_state'], width=btn['width'])
            button.pack(side=btn['side'], padx=10, pady=10)
            btn['widget'] = button

    def disable_all_btns(self):
        for btn in self.buttons:
            btn['widget']['state'] = 'disabled'

    def enable_all_btns(self):
        for btn in self.buttons:
            btn['widget']['state'] = 'normal'

    def change_to_default_states(self):
        for btn in self.buttons:
            btn['widget']['state'] = btn['default_state']

    def disable_btn(self, button):
        for btn in self.buttons:
            if btn['name'] == button:
                btn['widget']['state'] = 'disabled'

    def enable_btn(self, button):
        for btn in self.buttons:
            if btn['name'] == button:
                btn['widget']['state'] = 'normal'

    def forget_btns(self):
        for btn in self.buttons:
            btn['widget'].pack_forget()

    def pack_btns(self, padx, pady):
        for btn in self.buttons:
            btn['widget'].pack(side=btn['side'], padx=padx, pady=pady)

#Class for a tab & tab pane
class Tab:
    def __init__(self, tab_pane, background_col):
        self.tab_pane = tab_pane
        self.background_col = background_col

        self.text = None
        self.frame = None

    def add_tab(self, text):
        frame = tk.Frame(self.tab_pane, background=self.background_col)
        self.frame = frame
        self.text = text
        self.tab_pane.add(self.frame, text = text) #takes in a dict of key value pairs to be split by pipe
        self.tab_pane.select(self.frame) #show selected tab  #https://stackoverflow.com/questions/27730509/how-to-change-the-tab-of-ttk-notebook
        return self.frame

    #This doesn't work as cannot change parent frame
    def change_notebook(self, new_notebook):
        self.tab_pane = new_notebook
        self.tab_pane.add(self.frame, text= self.text)
        self.tab_pane.select(self.frame)

##TOOLTIP Methods & Classes
# #A function that creates the tooltip
# def CreateToolTip(widget, text, hover_background, small_font):
#     #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
#     toolTip = ToolTip(widget, hover_background, small_font)
#     def enter(event): #to show tooltip
#         toolTip.showtip(text) #call showtip
#     def leave(event):
#         toolTip.hidetip() #hide tooltip
#     widget.bind('<Enter>', enter) #upon entry of mouse
#     widget.bind('<Leave>', leave) #upon leave of mouse
#
# #Custom Tooltip to match the other Matplotlib toolbar buttons
# class ToolTip:
#     #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
#     def __init__(self, widget, hover_background, hover_font_size):
#         self.widget = widget
#         self.text, self.tipwindow = None, None
#         self.hover_background = hover_background
#         self.hover_font_size = hover_font_size
#
#     def showtip(self, text):
#         self.text = text
#         x, y, cx, cy = self.widget.bbox("insert") #All 0 at this stage
#         x = x + self.widget.winfo_rootx() + 26 #root of the widget on the x axis, 0 = left
#         y = y + cy + self.widget.winfo_rooty() + 0 #root of the widget on the y axis, 0 = top
#         self.tipwindow = tk.Toplevel(self.widget) #create toplevel widget
#         self.tipwindow.wm_overrideredirect(1) #cannot be overrided = https://effbot.org/tkinterbook/wm.htm#wm.Wm.wm_overrideredirect-method
#         self.tipwindow.wm_geometry("+%d+%d" % (x, y)) #geometry of toplevel widget
#         label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
#                     background=self.hover_background, relief=tk.SOLID, borderwidth=1,
#                     font=self.hover_font_size) #styling
#         label.pack(ipadx=3) #padding
#
#     def hidetip(self):
#             self.tipwindow.destroy()

#Custom Tooltip to match the other Matplotlib toolbar buttons
class HoverToolTip:
    #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
    def __init__(self, widget, hover_background, hover_font_size, text):
        self.widget = widget
        self.text, self.tipwindow = None, None
        self.hover_background = hover_background
        self.hover_font_size = hover_font_size
        self.text = text

        self.create_tip()

    def create_tip(self):
        self.widget.bind('<Enter>', self.enter_mouse) #upon entry of mouse
        self.widget.bind('<Leave>', self.leave_mouse) #upon leave of mouse

    def enter_mouse(self, event):
        self.showtip(self.text) #call showtip

    def leave_mouse(self, event):
        self.hidetip() #hide tooltip

    def showtip(self, text):
        self.text = text
        x, y, cx, cy = self.widget.bbox("insert") #All 0 at this stage
        x = x + self.widget.winfo_rootx() + 26 #root of the widget on the x axis, 0 = left (Matplotlib tb btns have +26)
        y = y + cy + self.widget.winfo_rooty() + 0 #root of the widget on the y axis, 0 = top
        self.tipwindow = tk.Toplevel(self.widget) #create toplevel widget
        self.tipwindow.wm_overrideredirect(1) #cannot be overrided = https://effbot.org/tkinterbook/wm.htm#wm.Wm.wm_overrideredirect-method
        self.tipwindow.wm_geometry("+%d+%d" % (x, y)) #geometry of toplevel widget
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                    background=self.hover_background, relief=tk.SOLID, borderwidth=1,
                    font=self.hover_font_size) #styling
        label.pack(ipadx=3) #padding

    def hidetip(self):
        self.tipwindow.destroy()

    def change_hover_text(self, new_text):
        self.text = new_text

#Class for the table construction
class NoteTable:
    #table construction: https://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter
    def __init__(self, parent_frame, col_settings, data, width, height, row_btns, background_col):
        self.parent_frame = parent_frame
        self.col_settings = col_settings
        self.data = data
        self.row_btns = row_btns
        self.background_col = background_col

        children = self.parent_frame.winfo_children()
        if len(children) > 0:
            self.clear_table(self.parent_frame)

        if len(self.data) > 4:
            #use scroller
            table = self.create_table(self.parent_frame, self.col_settings, self.data, True, width, height)
        elif len(self.data) < 5:
            #do not use scroll
            table = self.create_table(self.parent_frame, self.col_settings, self.data, False, width, height)

    #function for creating a table
    def create_table(self, parent_frame, col_settings, data, scroll, width, height):
                wider_frame = tk.Frame(parent_frame)
                wider_frame.pack(side="top", padx=10, pady=10)

                #canvas is on the left hand side & scrollbar on the right
                canvas = tk.Canvas(wider_frame, height=height, width=width, bg=self.background_col, borderwidth=0, highlightthickness=0)  #create a canvas, canvas has the scrollbar functionality
                #frame is the scrollable area
                frame = tk.Frame(canvas, bg="black")
                if scroll:
                    scrollbar = ttk.Scrollbar(wider_frame, orient="vertical", command=canvas.yview) #add the scrollbar to the container

                    frame.bind( #function for ensuring the scrolling capacity is for all the text
                        "<Configure>",
                        lambda e: canvas.configure(
                            scrollregion=canvas.bbox("all")
                        )
                    )

                #create the table
                num_cols = len(col_settings)
                col = 0
                for column in col_settings:
                    label = tk.Label(frame, bg="grey", fg="white", text=column['column'].capitalize(), borderwidth=0, width=column['width'])
                    label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
                    col += 1
                #configure the size of the table to ensure that spacing is provided equally and is not dependent on contents
                for column in range(num_cols):
                    frame.grid_columnconfigure(column, weight=1)

                #extra column for buttons
                buttons = ['adjust'] #title for column which contains the buttons
                btn_col_width = 0
                for btn in self.row_btns:
                    btn_col_width += btn['width']

                for column in buttons:
                    label = tk.Label(frame, bg="grey", fg="white", text=column.capitalize(), borderwidth=0, width=btn_col_width)
                    label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1, columnspan=2)

                #to ensure that the button column is dependent on size of the buttons
                frame.grid_columnconfigure(col, weight=0)

                #add the notes to the table

                row = 1
                print("data", data)
                for entry in data:
                    print(entry)
                    col = 0
                    for key, value in entry.items():
                        inner_cell_frame = tk.Frame(frame, borderwidth=0)
                        label = tk.Label(inner_cell_frame, text=value, borderwidth=0, wraplength=self.get_setting(key, col_settings, "wraplength"))
                        label.pack(side="left", padx=2, pady=2)
                        inner_cell_frame.grid(row=row, column=col, sticky="nswe", padx=1, pady=1)

                        if key == col_settings[col]['column']:
                            if col_settings[col]['fill']: #if this is true, it means the value is a colour
                                inner_cell_frame['background'] = value
                                label['background'] = value
                            else:
                                inner_cell_frame['background'] = "white"
                                label['background'] = "white"
                            #wraplength: https://stackoverflow.com/questions/16761726/label-break-line-if-string-is-too-big
                        col += 1
                    row += 1
                    #add the btns per row
                    for btn in self.row_btns:
                        inner_cell_frame = tk.Frame(frame, bg="white", borderwidth=0)
                        inner_cell_frame.grid(row=row - 1, column=col, sticky="nswe", padx=1, pady=1)
                        data = []
                        # print("ENTRY", len(entry))
                        # print(entry)
                        # for key, value in entry:
                        # for column in col_settings:
                        #     data.append(column['column'])
                        data.append(entry)

                        # data.append(entry[col_settings[0]['column']])
                        # data.append(entry[col_settings[1]['column']])
                        # data.append(entry[col_settings[2]['column']])
                        # data.append(entry[col_settings[3]['column']])
                        # print(btn['function'])
                        button = tk.Button(inner_cell_frame, text=btn['text'], width=btn['width'], command = lambda data=data, function=btn['function']: function(data))
                        #https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda
                        button.pack(side="left", padx=1, pady=1)
                        col += 1

                canvas.create_window((0, 0), window=frame, anchor="nw") #position the canvas

                canvas.pack(side="left", fill="both", expand=True) #put the text frame on the left
                if scroll:
                    canvas.configure(yscrollcommand=scrollbar.set) #so it scroll only for canvas area
                    scrollbar.pack(side="right", fill="y") #put the scroller on the right hand side

        #function for getting a setting from col_settings

    def get_setting(self, key, col_settings, setting):
        for column in col_settings:
            if key == column['column']:
                return column[setting]

        #function for printing a note

    def action_note(self, btn, note):
        print(btn)
        if btn['name'] == "edit":
            print("This note is to be edited", note)
            val = btn['function']
        if btn['name'] == "remove":
            print("This note is to be removed", note)
            val = btn['function']

    def clear_table(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    def destroy(self):
        self.clear_table(self.parent_frame)

#This class creates a frame with a text label & colour square next to it, it is used throughout the program
class ColourSquare:
    def __init__(self, parent_frame, row, column, start_col):
        self.parent_frame = parent_frame
        self.row = row
        self.column = column
        self.start_col = start_col
        self.frame = None

        if self.start_col != None:
            self.create_frame()
            self.set_colour(self.start_col)

    def create_frame(self):
        self.frame = tk.Frame(self.parent_frame, width=15, height=15)
        self.frame.grid(row=self.row, column=self.column, sticky="W", padx=(10, 0))

    def set_colour(self, colour):
        if self.frame != None:
            if self.frame.winfo_exists() == 1:
                self.frame['background'] = colour
        else:
            self.create_frame() #frame has been destroyed or not created
            self.frame['background'] = colour

    def remove(self):
        if self.frame != None:
            self.frame.destroy()
        else:
            print("Frame has not been created.")

# # #A function that calulcates the date stamp
# def get_time_stamp():
#     #https://timestamp.online/article/how-to-get-current-timestamp-in-python
#     #https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
#     ts = time.time()
#     readable = datetime.datetime.fromtimestamp(ts).isoformat()
#
#     date_time = re.split("T", readable)
#     date_stamp = date_time[0]
#     time_stamp = date_time[1][:5]
#
#     day = date_stamp[8:]
#     month = date_stamp[5:7]
#     year = date_stamp[:4]
#     date_stamp_adjust = day + "-" + month + "-" + year
#
#     final_stamp = date_stamp_adjust + " " + time_stamp
#     return final_stamp

#CLass for toggled frame, it initialises a frame
class ToggledFrame(tk.Frame):
    #https://stackoverflow.com/questions/13141259/expandable-and-contracting-frame-in-tkinter
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

class LoginFrame:
    def __init__(self, parent, parent_frame, background_col, font_col, password):
        self.parent = parent
        self.parent_frame = parent_frame
        self.background_col = background_col
        self.font_col = font_col
        self.password = password

        #login labelFrame
        self.login_frame = tk.LabelFrame(self.parent_frame, text="  Login:  ", padx=10, pady=10, bg=self.background_col, fg=self.font_col)
        self.login_frame.grid(row=0, column=1, pady=10, padx=10)

        #create a grid in main so login frame is positioned centrally.
        for j in range(3):
            self.parent_frame.rowconfigure(j, weight=1)
            self.parent_frame.columnconfigure(j, weight=1)

        #if incorrect details provided
        self.error_label = tk.Label(self.login_frame, text="", font=8, fg="red", bg=self.background_col)

        #For the entry of the username
        self.entries = [{"name": "name", "type": "entry", "width": 30, "password": False},
                        {"name": "password", "type": "entry", "width": 30, "password": True}
                        ]

        self.label_entry_boxes = tk.Frame(self.login_frame, bg=self.background_col)
        self.label_entry_boxes.grid(row=0, column=0, sticky="NSWE", padx=0, pady=0)
        row, col, parent_frame = 0, 0, self.label_entry_boxes
        for entry in self.entries:
            label = tk.Label(parent_frame, text=entry['name'].capitalize() + ": ", font=("Verdana", 10), fg=self.font_col, bg=self.background_col)
            label.grid(row=row, column=col, pady=10, padx=10, sticky="w")
            if entry['type'] == "entry":
                entry_box = tk.Entry(parent_frame, width=entry['width'])
                entry_box.grid(row=row, column=col + 1, pady=10, padx=10)
                if entry['password']:
                    entry_box['show'] = "*"
                entry['widget'] = entry_box
            row += 1

        self.enter_btn = ttk.Button(self.login_frame, text="Enter", command=lambda: self.get_login_details(), width=45) #click enter to then call the login method - I am looking to pass through the username
        self.enter_btn.grid(row=2, column=0, pady=10, padx=10, columnspan=2)

    #function for the login details to pull those from the entry boxes
    def get_login_details(self):
        username, password = None, None
        for item in self.entries:
            if item['name'] == 'name':
                username = item['widget'].get()
            if item['name'] == 'password':
                password = item['widget'].get()

        self.login(username, password)

        #function for logging in, checks if the values are correct, not None etc

    #Trys to login. This is not very dynamic I know but it is not the main focus of the program
    def login(self, username, password):
        if password == self.password and len(username) > 0:
            # self.controller.show_frame(PageOne, username) #Username can be passed to parent, then PageOne, here for current session info
            self.parent.pass_through_login_frame(username)

        elif (len(username) == 0) or username == None: #username is required
            self.error_label.grid(row=0, column=0)
            self.error_label['text'] = "Please enter a username"
            self.label_entry_boxes.grid(row=1, column=0)

        elif (len(username) > 0 and (password != self.password or password == None)): #password is incorrect
            self.label_entry_boxes.grid(row=1, column=0)
            self.error_label.grid(row=0, column=0,  columnspan=2)
            self.error_label['text'] = "Incorrect Password"

    #Function that resets the login widgets that are used above - the entry widgets
    def reset_login_widgets(self):
        for item in self.entries:
            if item['name'] == 'name':
                item['widget'].delete(0, tk.END) #clear entry box for username upon return to StartPage once closed session
