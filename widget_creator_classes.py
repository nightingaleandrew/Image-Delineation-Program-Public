#Contains classes regarding creating a widget
#Follows compartmentalisation design pattern. Classes include creating a loginframe, InformationBox, Tab or Hover Tooltip

import tkinter as tk
from tkinter import ttk
import re

#Class for creating a dynamic textbox. This is used for the adding of notes or the editing of notes. It is different to the standard entry frames
class TextBox:
    def __init__(self, parent_frame, height, width, note):
        self.notebox = tk.Text(parent_frame, height=height, width=width, background="white", foreground="black") #create the textbox, black background with white forefront for positive text readability
        self.notebox.insert(tk.END, note) #note is already pre-inserted - eg. Select Option or previous note to be edited
        self.notebox.pack(fill="x", expand=True, padx=10, pady=10) #10 is standard default padding

    #If the notebox requires different padding to what is default
    def change_notebox_padding(self, padx, pady):
        self.notebox.pack_forget()
        self.notebox.pack(fill="x", expand=True, padx=padx, pady=pady)

    #clear the contents of the notebox
    def clear_notebox(self):
        self.notebox.delete(1.0, tk.END)

    #Disable the notebox
    def disable_notebox(self):
        #effbot.org. The Tkinter Text Widget [Online]. Available at: http://effbot.org/tkinterbook/text.htm [Accessed: 06 July 2020]
        self.notebox['state'] = 'disabled'
        self.notebox['background'] = 'gray' #gray looks good to show disabled
        self.notebox['foreground'] = 'white'

    #Enable the notebox for action
    def enable_notebox(self):
        self.notebox['state'] = 'normal'
        self.notebox['background'] = "white" #default background colour
        self.notebox['foreground'] = "black" #default foreground colour

    #Replace text of notebox with something else
    def replace_text(self, text):
        self.clear_notebox()
        self.notebox.delete("insert linestart", "insert lineend") #ensure that all is removed
        self.notebox.insert(tk.END, text) #insert the text that is passed through into the method into the textbox

    #Read the contents of the notebox
    def read_contents(self):
        contents = self.notebox.get(1.0, tk.END) #read all notebox
        return contents

    #Bind the notebox to a functon if clicked. Eg. if click on the textbox clears placeholder text that say introduces the user to the notebox
    def bind_click(self, function):
        #effbot.org. Events and Bindings [Online]. Available at: https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm [Accessed: 06 July 2020]
        self.notebox.bind("<Button-1>", lambda e: function())

#Class for a box of information with labels & dynamic updates. This is used throughout the program such as for SessionData, or Polygon Data or Slice Data
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
    #Structures the information values into the number of rows and columns given
    def create_insides(self, info):
        row = 0
        column = 0
        padx = (0, 0) #padding is set to first column and left hand side. Changed when moves to next col
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

            #Below are calculations for rows & cols depending on what is provided
            if row != self.rows: #if the row number is not the total number of rows then continue as still filling in downwards in col
                row += 1
            if row == self.rows: #if row does equal number of rows passed in then pass to next column & reset row
                column += 2
                row = 0
                padx = (25, 0)  #so the padding seperates between two columns rather than left side & first column

    #reset the text labels to not applicable or n/a, better than re-creating widget
    def reset_to_na(self):
        for line in self.dict:
            if line['type'] == "text": #type would have to be text
                line['widget']['text'] = "n/a"
                line['value'] = "n/a"

    #Given no label to the text values in the box.
    def present_no_value(self):
        for line in self.dict:
            if line['type'] == "text": #type would have to be text
                line['widget']['text'] = ""
                line['value'] = ""

    #Takes in a dict of key value pairs for the current ones already installed & if label widgets, changes the text
    def refresh_information(self, information):
        for key, value in information.items():
            for line in self.dict:
                if ((line['name'] == key) and (line['type'] == "text")):
                    line['widget']['text'] = value
                    line['value'] = value

    #Pulls a detail from the dictionary to show or use elsewhere
    def pull_detail(self, label):
        detail = None
        for line in self.dict:
            if ((line['name'] == label) and (line['type'] == "text")):
                detail = line['value']
        return detail #if returns None then not present

    #forgets the whole frame
    def make_box_go_walkies(self):
        self.content_frame.pack_forget()

    #Changes the formatting to grid for the frame. Packing is default but therefore can have it within grid if needed too.
    def change_to_grid(self, row, col, sticky, columnspan):
        self.make_box_go_walkies()
        self.content_frame.grid(row=row, column=col, sticky=sticky, columnspan=columnspan, padx=self.padding, pady=self.padding)

#Class for creating buttons. I have standardised the creation of these as buttons are created in sets multiple times such as Cancel, Confirm
class ButtonCreator:
    def __init__(self, parent_frame, dict):
        self.parent_frame = parent_frame
        self.buttons = dict
        self.create_buttons() #create the buttons

    #Create buttons
    def create_buttons(self):
        for btn in self.buttons:
            button = ttk.Button(self.parent_frame, text=btn['name'].capitalize(), command= lambda function=btn['command']: function(), state=btn['default_state'], width=btn['width']) #create button with ttk, state, width, function, label
            button.pack(side=btn['side'], padx=10, pady=10) #packing side is provided
            btn['widget'] = button #add the button back in the dict so it can be manipulated

    #Function to disable all the buttons within the set
    def disable_all_btns(self):
        for btn in self.buttons:
            btn['widget']['state'] = 'disabled'

    #Function to enable all the buttons within the set
    def enable_all_btns(self):
        for btn in self.buttons:
            btn['widget']['state'] = 'normal'

    #Change all buttons in dict to their default states
    def change_to_default_states(self):
        for btn in self.buttons:
            btn['widget']['state'] = btn['default_state']

    #Disable a particular button
    def disable_btn(self, button):
        for btn in self.buttons:
            if btn['name'] == button:
                btn['widget']['state'] = 'disabled'

    #Enable a particular button
    def enable_btn(self, button):
        for btn in self.buttons:
            if btn['name'] == button:
                btn['widget']['state'] = 'normal'

    #Forget buttons in the set (for instance the arrow buttons for changing tabs)
    def forget_btns(self):
        for btn in self.buttons:
            btn['widget'].pack_forget()

    #Pack the buttons (they may have been forgotten - say the arrow tab buttons)
    def pack_btns(self, padx, pady):
        for btn in self.buttons:
            btn['widget'].pack(side=btn['side'], padx=padx, pady=pady)

#Class for a tab in the tab pane. Creates the tab & the tab object can then be stored.
class Tab:
    def __init__(self, tab_pane, background_col):
        self.tab_pane = tab_pane #let the tab know which tab pane or notebook it is apart of
        self.background_col = background_col #set the background colour of the tab

        self.text = None #this is the title of the tab in the tab header which may change eg. in the notebok polygon notes where polygon Notes is changed to polygon information
        self.frame = None #method add tab creates the frame

    def add_tab(self, text):
        frame = tk.Frame(self.tab_pane, background=self.background_col)
        self.frame = frame
        self.text = text
        self.tab_pane.add(self.frame, text = text) #takes in a dict of key value pairs to be split by pipe from the class in other.py
        self.tab_pane.select(self.frame) #show selected tab  #Kent, J. (2015) How to change the tab of ttk.Notebook Available at: https://stackoverflow.com/questions/27730509/how-to-change-the-tab-of-ttk-notebook [Accessed: 11 July 2020]
        return self.frame

    #*NOT USED*
    #This doesn't work as cannot change parent frame. NEED TO RETHINK THIS
    def change_notebook(self, new_notebook):
        self.tab_pane = new_notebook
        self.tab_pane.add(self.frame, text= self.text)
        self.tab_pane.select(self.frame)

#Custom Tooltip to match the other Matplotlib toolbar buttons hover tips. I used this across the program for instance on the syncrhonise button
class HoverToolTip:
    #I have manipulated the below structure to work for this program & make it more class based. Added further methods
    #SquareRoot17 (2016) Display message when hovering over something with mouse cursor in Python [Online]. Available at: https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python [Accessed: 09 July 2020]
    def __init__(self, widget, hover_background, hover_font_size, text):
        self.widget = widget
        self.tipwindow = None
        self.hover_background = hover_background
        self.hover_font_size = hover_font_size
        self.text = text

        self.create_tip() #create the tooltip when the class is instantiated

    #Method for creating the tooltip for a button in the program
    def create_tip(self):
        self.widget.bind('<Enter>', self.enter_mouse) #upon entry of mouse show the tip
        self.widget.bind('<Leave>', self.leave_mouse) #upon leave of mouse hide the tip

    def enter_mouse(self, event):
        self.showtip(self.text) #call showtip

    def leave_mouse(self, event):
        self.hidetip() #hide tooltip

    #Function to show the tooltip
    def showtip(self, text):
        self.text = text
        x, y, cx, cy = self.widget.bbox("insert") #All 0 at this stage
        x = x + self.widget.winfo_rootx() + 26 #root of the widget on the x axis, 0 = left (Matplotlib tb btns have +26)
        y = y + cy + self.widget.winfo_rooty() + 0 #root of the widget on the y axis, 0 = top
        self.tipwindow = tk.Toplevel(self.widget) #create toplevel widget
        self.tipwindow.wm_overrideredirect(1) #cannot be overrided effbot.org. Toplevel Window Methods [Online]. Available at: https://effbot.org/tkinterbook/wm.htm#wm.Wm.wm_overrideredirect-method [Accessed: 09 July 2020]
        self.tipwindow.wm_geometry("+%d+%d" % (x, y)) #geometry of toplevel widget
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                    background=self.hover_background, relief=tk.SOLID, borderwidth=1,
                    font=self.hover_font_size) #styling
        label.pack(ipadx=3) #padding

    #Function to hide the tip
    def hidetip(self):
        self.tipwindow.destroy() #simple destroy of the frame

    #Function to change the hover text of the tooltip eg. when syncrhonise button changes if clicked
    def change_hover_text(self, new_text):
        self.text = new_text

#Class for the table construction that is used for notes and for tags. I have modified it slightly eg. by passing the functions through & buttons for each row
#In phase 2 I would be looking to develop this class to trim it down & make it more dynamic
class NoteTable:
    #Oakley, B. (2012) Creating a table look-a-like Tkinter [Online]. Available at: https://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter [Accessed: 12 July 2020]
    def __init__(self, parent_frame, col_settings, data, width, height, row_btns, background_col):
        self.parent_frame = parent_frame
        self.col_settings = col_settings
        self.data = data
        self.row_btns = row_btns
        self.background_col = background_col

        self.table_frame_background_col = "black"
        self.table_cell_background_col = "grey"
        self.table_cell_foreground_col = "white"

        children = self.parent_frame.winfo_children() #if the table is present then clear it, if update is needed etc
        if len(children) > 0:
            self.clear_table(self.parent_frame)

        #If the length of the data is > 4 rows then make scrollable True i.e use the scroller
        if len(self.data) > 4:
            #use scroller
            table = self.create_table(self.parent_frame, self.col_settings, self.data, True, width, height)

        #If the length of the data is < 5 rows then make scrollable False. i.e do not use the scroller
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
                frame = tk.Frame(canvas, bg=self.table_frame_background_col) #background of frame behind row/col frames. This makes it look like there are border lines for each cell. it is set to black above
                if scroll:
                    scrollbar = ttk.Scrollbar(wider_frame, orient="vertical", command=canvas.yview) #add the scrollbar to the container
                    #function for ensuring the scrolling capacity is for all the text
                    #teclado. Scrollable Frames in Tkinter Available at: #https://blog.tecladocode.com/tkinter-scrollable-frames/ [Accessed: 12 July 2020]
                    frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                #TABLE CREATION
                #create header columns & rows
                num_cols = len(col_settings)
                col = 0
                for column in col_settings:
                    label = tk.Label(frame, bg=self.table_cell_background_col, fg=self.table_cell_foreground_col, text=column['column'].capitalize(), borderwidth=0, width=column['width']) #background is grey & fg white for positive text
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
                    label = tk.Label(frame, bg=self.table_cell_background_col, fg=self.table_cell_foreground_col, text=column.capitalize(), borderwidth=0, width=btn_col_width)
                    label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1, columnspan=2)

                #to ensure that the button column is dependent on size of the buttons
                frame.grid_columnconfigure(col, weight=0)

                #Add the notes to the table & respective rows & columns
                row = 1
                #use the passed through data from row 1 to add the data for the table
                for entry in data:
                    print(entry)
                    col = 0
                    for key, value in entry.items():
                        inner_cell_frame = tk.Frame(frame, borderwidth=0)
                        label = tk.Label(inner_cell_frame, text=value, borderwidth=0, wraplength=self.get_setting(key, col_settings, "wraplength")) #I have included a wraplength as the length of text could be longer than the cell
                        label.pack(side="left", padx=2, pady=2)
                        inner_cell_frame.grid(row=row, column=col, sticky="nswe", padx=1, pady=1)

                        if key == col_settings[col]['column']:
                            if col_settings[col]['fill']: #if this is true, it means the value is a colour
                                inner_cell_frame['background'] = value
                                label['background'] = value
                            else:
                                inner_cell_frame['background'] = "white"
                                label['background'] = "white"
                            #wraplength: #Pieters, M. (2013) Label break line if string is too big [Online]. Available at: https://stackoverflow.com/questions/16761726/label-break-line-if-string-is-too-big [Accessed: 12 July 2020]
                        col += 1
                    row += 1
                    #add the btns per row
                    for btn in self.row_btns:
                        inner_cell_frame = tk.Frame(frame, bg="white", borderwidth=0)
                        inner_cell_frame.grid(row=row - 1, column=col, sticky="nswe", padx=1, pady=1)
                        data = []
                        data.append(entry)

                        button = tk.Button(inner_cell_frame, text=btn['text'], width=btn['width'], command = lambda data=data, function=btn['function']: function(data))
                        #https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda
                        button.pack(side="left", padx=1, pady=1)
                        col += 1

                #Further scrollable functionality to ensure it reacts to the canvas
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
    # def action_note(self, btn, note):
    #     if btn['name'] == "edit":
    #         print("This note is to be edited", note)
    #         val = btn['function']
    #     if btn['name'] == "remove":
    #         print("This note is to be removed", note)
    #         val = btn['function']

    #Function for clearing the table from the frame eg. if refresh needed
    def clear_table(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    #Function for destroy the table. Uses above clear_table functionality
    def destroy(self):
        self.clear_table(self.parent_frame)

#This class creates a frame with a text label & colour square next to it, it is used throughout the program for instance in the settings so the user can see which colour has been selected
class ColourSquare:
    def __init__(self, parent_frame, row, column, start_col):
        self.parent_frame = parent_frame
        self.row = row
        self.column = column
        self.start_col = start_col
        self.frame = None

        if self.start_col != None: #if there is a start colour passed through then create the frame & set the colour
            self.create_frame()
            self.set_colour(self.start_col)

    #Create the frame. I pass the row & col to the grid
    def create_frame(self):
        self.frame = tk.Frame(self.parent_frame, width=15, height=15)
        self.frame.grid(row=self.row, column=self.column, sticky="W", padx=(10, 0))

    #Set the colour of the frame, eg. when the colour is passed through from the colorchooser in change settings
    def set_colour(self, colour):
        if self.frame != None:
            if self.frame.winfo_exists() == 1:
                self.frame['background'] = colour
        else:
            self.create_frame() #frame has been destroyed or not created
            self.frame['background'] = colour

    #Remove the colour square frame
    def remove(self):
        if self.frame != None:
            self.frame.destroy() #destroy
        else:
            print("Frame has not been created.")

#CLass for toggled frame, it initialises a frame. This is used for the categorisation in the frame
class ToggledFrame(tk.Frame):
    #I have manipulated the below structure to work such as knowing when one toggle frame is open to close a toggle frame when another toggle frame opens
    #Onlyjus (2012) Expandable and contracting frame in Tkinter [Online]. Available at: https://stackoverflow.com/questions/13141259/expandable-and-contracting-frame-in-tkinter [Accessed: 01 August 2020]

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

        #label for that frame - title
        ttk.Label(self.title_frame, text=self.title).pack(side="left", fill="x", expand=1)

        #toggle button for opening title frame - either + or -
        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text=' +', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        #sub frame
        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1, bg=sub_frame_color)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1) #pack the sub frame which is what the contents is packed onto
            self.toggle_button.configure(text=' -') #- button as is open
            self.parent.tab_toggle_open(self.title) #call parent & look to close all other toggles
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text=' +') #plus button for the toggle button now as is closed

    def open(self): #to see if the toggle is open
        return self.show.get()

    def close(self): #to see if the toggle is closed
        self.sub_frame.forget()
        self.toggle_button.configure(text=' +')

    def get_sub_frame(self): #get the sub frame
        return self.sub_frame

#Class for a login label frame, this is used not primarily for security but for adding a username to the session to then attach to notes etc
class LoginFrame:
    def __init__(self, parent, parent_frame, background_col, font_col, password):
        self.parent = parent
        self.parent_frame = parent_frame
        self.background_col = background_col
        self.font_col = font_col
        self.password_details = password

        #login labelFrame - contains the labels username, password etc
        self.login_frame = tk.LabelFrame(self.parent_frame, text="  Login:  ", padx=10, pady=10, bg=self.background_col, fg=self.font_col)
        self.login_frame.grid(row=0, column=1, pady=10, padx=10)

        #create a grid in main so login frame is positioned centrally.
        for j in range(3):
            self.parent_frame.rowconfigure(j, weight=1)
            self.parent_frame.columnconfigure(j, weight=1)

        #if incorrect details provided
        self.error_label = tk.Label(self.login_frame, text="", font=8, fg="red", bg=self.background_col)

        #For the entry of the username & password - can add to this if need further fields
        self.entries = [{"name": "name", "type": "entry", "width": 30, "password": False}]
        if self.password_details['required']:
            self.entries.append({"name": "password", "type": "entry", "width": 30, "password": True})


        self.label_entry_boxes = tk.Frame(self.login_frame, bg=self.background_col)
        self.label_entry_boxes.grid(row=0, column=0, sticky="NSWE", padx=0, pady=0)
        row, col, parent_frame = 0, 0, self.label_entry_boxes
        #Create the entries & labels in similar way the information box works by iterating through a dict of them & then packing them down
        for entry in self.entries:
            label = tk.Label(parent_frame, text=entry['name'].capitalize() + ": ", font=("Verdana", 10), fg=self.font_col, bg=self.background_col)
            label.grid(row=row, column=col, pady=10, padx=10, sticky="w")
            if entry['type'] == "entry":
                entry_box = tk.Entry(parent_frame, width=entry['width'])
                entry_box.grid(row=row, column=col + 1, pady=10, padx=10)
                if entry['password']:
                    entry_box['show'] = "*" #asterix is so password cannot be seen
                entry['widget'] = entry_box
            row += 1 #go onto next row

        #The main enter button
        self.enter_btn = ttk.Button(self.login_frame, text="Enter", command=lambda: self.get_login_details(), width=45) #click enter to then call the login method
        self.enter_btn.grid(row=3, column=0, pady=10, padx=10)

    #function for the login details to pull those from the entry boxes
    def get_login_details(self):
        username, password = None, None
        for item in self.entries:
            if item['name'] == 'name':
                username = item['widget'].get()
            if item['name'] == 'password':
                password = item['widget'].get()

        self.login(username, password) #call login

    #Trys to login. This is not very dynamic I know but it is not the main focus of the program. I can develop it more if security becomes a larger focus.
    #Future development - this is not very dynamic - please improve.
    def login(self, username, password):
        if self.password_details['required']:
            if password == self.password_details['password'] and len(username) > 0:
                self.parent.pass_through_login_frame(username) #Username can be passed to parent, then PageOne, by called the parent class of .pass_through_login_frame
                self.error_label.grid_forget() #forget the error message if go through (if close session then want to return to a fresh login frame)
                self.label_entry_boxes.grid(row=0, column=0) #reset the grid position

            elif (len(username) == 0) or username == None: #username is required
                self.error_label.grid(row=0, column=0)
                self.error_label['text'] = "Please enter a username"
                self.label_entry_boxes.grid(row=1, column=0)

            elif (len(username) > 0 and (password != self.password_details['password'] or password == None)): #password is incorrect
                self.label_entry_boxes.grid(row=1, column=0)
                self.error_label.grid(row=0, column=0,  columnspan=2)
                self.error_label['text'] = "Incorrect Password"
        else:
            if len(username) > 0:
                self.parent.pass_through_login_frame(username) #Username can be passed to parent, then PageOne, by called the parent class of .pass_through_login_frame
                self.error_label.grid_forget() #forget the error message if go through (if close session then want to return to a fresh login frame)
                self.label_entry_boxes.grid(row=0, column=0) #reset the grid position

            elif (len(username) == 0) or username == None: #username is required
                self.error_label.grid(row=0, column=0)
                self.error_label['text'] = "Please enter a username"
                self.label_entry_boxes.grid(row=1, column=0)

    #Function that resets the login widgets that are used above - the entry widgets
    def reset_login_widgets(self):
        for item in self.entries:
            if item['name'] == 'name':
                item['widget'].delete(0, tk.END) #clear entry box for username upon return to StartPage once closed session
