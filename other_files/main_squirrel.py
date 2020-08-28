#example code
#tkinter imports
import tkinter as tk
from tkinter import ttk #for styling eg. ttk buttons
from tkinter import messagebox, colorchooser, filedialog
#other imports
import random, os, re, time, datetime, sqlite3, numpy as np, json
#matplotlib imports
import matplotlib
matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#https://stackoverflow.com/questions/32188180/from-matplotlib-backends-import-tkagg-importerror-cannot-import-name-tkagg
from matplotlib.figure import Figure
import matplotlib.image as mpimg

#image imports
from PIL import ImageTk, Image
from PIL import Image as PIL_image, ImageTk as PIL_imagetk

#classes
# from graph_actions_2 import cidPress, PolygonIntersector, jsonFileWriterPolygon, PolygonTagChanger
from toggle_frame import ToggledFrame
from TopLevelWin import TopLevelWin
from widget_creator_classes import TextBox, InformationBox, ButtonCreator, Tab, CreateToolTip, ToolTip, NoteTable, ColourSquare
from figure_custom_classes import cidPress, PolygonIntersector, CustomToolbar
from PolygonTagChanger import TagFileLoader, PolygonTagChanger

from button_images import custom_btn_images
from storage_classes import jsonFileWriter, Database
from other import ConvertImages

from polygon_settings_test import PolygonSettings

# from tab_pane_close import CustomNotebook
MAKE_DB = False
MAKE_JSON = True

#fonts
LARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 14)
SMALL_FONT = ("Verdana", 10)
#settings
PASSWORD = ""
DIRECTORY = r"C:/Users/Andrew/Documents/dissertation/data/proc" #directory here

# PROGRAM_ICON = r'C:\Users\Andrew\Documents\dissertation\tkinter\images\MRI_Icon.ico'
#Colour Schemes
COLOUR_SCHEMES = [{"name": "Dark", "colours":[
                    {"header_background": "#00004d"},
                    {"header_text": "#FFFFFF"},
                    {"background": "#0066cc"},
                    {"background_text": "#FFFFFF"},
                    {"button": "orange"},
                    {"button_text": "orange"},
                    {"hover_background": "#ffffe0"}, #yellowish colour used by matplotlib
                    {"text": "#FFFFFF"},
                    ]},
                {"name": "Monochrome", "colours":[
                    {"header_background": ""},
                    {"header_text": ""},
                    {"background": ""},
                    {"background_text": ""},
                    {"button": ""},
                    {"button_text": "orange"},
                    {"hover_background": "#ffffe0"}, #yellowish colour used by matplotlib
                    {"font": ""},
                    ]}
                ]
HOVER_BG = "#ffffe0"
HEADER_BG = "#00004d"
FONT_BG = "#FFFFFF"
MAIN_BG = "#0066cc"
FONT_COL = "#FFFFFF"
ERROR_FONT = "red"

#DB Names & Columns
DB_NAME = "MRIScansNotesDatabase.db"
TABLES = [{"value": "Slice", "table_name": "MRISliceNotes", "columns":[
                    {"col_name": "note", "col_type": "text"},
                    {"col_name": "user", "col_type": "text"},
                    {"col_name": "year", "col_type": "text"}, #I want this to be number
                    {"col_name": "patient", "col_type": "text"},
                    {"col_name": "scan_type", "col_type": "text"},
                    {"col_name": "slice", "col_type": "text"},
                    {"col_name": "date", "col_type": "text"},
                    {"col_name": "time", "col_type": "text"},
                    ]},
        {"value": "Scan Type", "table_name": "ScanTypeNotes", "columns": [
                    {"col_name": "note", "col_type": "text"},
                    {"col_name": "user", "col_type": "text"},
                    {"col_name": "year", "col_type": "text"}, #I want this to be number
                    {"col_name": "patient", "col_type": "text"},
                    {"col_name": "scan_type", "col_type": "text"},
                    {"col_name": "date", "col_type": "text"},
                    {"col_name": "time", "col_type": "text"},
                    ]}
        ]

#Here, I pull in the settings json file, if there is one (if not one is created) & I check it for errors. If errors then default values are used (which are hardcoded in that file).
#In the settings json file only the config & default values can be changed. They need to be changed before the program is loaded. Any changes within the program will be temporary for the session.
from SetSettings import SetSettings

settings_data_filename = r".\settings.json"
settings_file = SetSettings(settings_data_filename)
SETTINGS = settings_file.settings #These are the settings that are used for the program while it is live.

#Filename that contains the tags
TAGS_DATA_FILENAME = r".\tags.json"

#A function that calulcates the date stamp
def start_time():
    #https://timestamp.online/article/how-to-get-current-timestamp-in-python
    #https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
    ts = time.time()
    readable = datetime.datetime.fromtimestamp(ts).isoformat()

    date_time = re.split("T", readable)
    date_stamp = date_time[0]
    time_stamp = date_time[1][:5]

    day = date_stamp[8:]
    month = date_stamp[5:7]
    year = date_stamp[:4]
    date_stamp_adjust = day + "-" + month + "-" + year

    final_stamp = date_stamp_adjust + " " + time_stamp
    return final_stamp



class MainApp(tk.Tk):  #inherit tkinter methods from tk class inside tkinter
    def __init__(self, *args, **kwargs): #initialise the method
        global imgs_custom_btns #need to pass through the images as global variables for some reason,

        tk.Tk.__init__(self, *args, *kwargs) #initalise tkinter
        tk.Tk.wm_title(self, "Dissertation Application") #seems like title works okay anyhow
        # tk.Tk.iconbitmap(self, default=PROGRAM_ICON) #16 by 16 ico file

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1) #0 is setting of min size
        container.grid_columnconfigure(0, weight=1)

        #MenuBar with controls on colour scheme & quiting applications (these are the same across the application)
        menubar = tk.Menu(container) #menu bar for all pages
        filemenu = tk.Menu(menubar, tearoff = 0) #dotted line that allows the little window to come off, if don't want can use 0
        filemenu.add_command(label="Exit", command=quit) #built in method quit
        menubar.add_cascade(label="File", menu=filemenu)

        help_choice = tk.Menu(menubar, tearoff = 0)
        help_choice.add_command(label="Colour Scheme")
        menubar.add_cascade(label="Settings", menu=help_choice)
        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        for f, geometry in zip((StartPage, PageOne), ('400x300+550+200', "1400x700+50+0")):
            #geom is x by y (size) + offset x & offset y
            frame = f(container, self)
            self.frames[f] = (frame, geometry)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage, "No Session") #remember to pass msg through

        #function to raise the particular frame called & also send info & struc geom
    def show_frame(self, cont, msg): #when show_frame called, msg needs to be passed through
        frame, geometry = self.frames[cont]
        frame.sendmsg(msg) #send the message to the class before rasied
        self.geometry(geometry) #change the geom of the whole frame
        frame.tkraise() #raise to the front



#Class for the start page, this page has the ability to login
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #header container
        self.header = tk.Frame(self, bg=HEADER_BG)
        self.header.pack(side="top", fill="both", expand=True)

        #page title
        self.page_title =tk.Label(self.header, text="MRI Delineation", font=LARGE_FONT, fg=FONT_COL, bg=HEADER_BG)
        self.page_title.pack(side="left", expand=True, fill="both", padx=(10, 10))

        #main container
        self.main = tk.Frame(self, bg=MAIN_BG)
        self.main.pack(side="bottom", fill="both", expand=True)

        #login labelFrame
        self.login_frame = tk.LabelFrame(self.main, text="  Login:  ", padx=10, pady=10, bg=MAIN_BG, fg=FONT_COL)
        self.login_frame.grid(row=0, column=1, pady=10, padx=10)

        #create a grid in main so login frame is positioned centrally.
        for j in range(3):
            self.main.rowconfigure(j, weight=1)
            self.main.columnconfigure(j, weight=1)

        #if incorrect details provided
        self.error_label = tk.Label(self.login_frame, text="", font=SMALL_FONT, fg=ERROR_FONT, bg=MAIN_BG)

        #For the entry of the username
        self.entries = [{"name": "name", "type": "entry", "width": 30, "password": False},
                        {"name": "password", "type": "entry", "width": 30, "password": True}
                        ]

        self.label_entry_boxes = tk.Frame(self.login_frame, bg=MAIN_BG)
        self.label_entry_boxes.grid(row=0, column=0, sticky="NSWE", padx=0, pady=0)
        row, col, parent_frame = 0, 0, self.label_entry_boxes
        for entry in self.entries:
            label = tk.Label(parent_frame, text=entry['name'].capitalize() + ": ", font=SMALL_FONT, fg=FONT_COL, bg=MAIN_BG)
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

        self.last_user = tk.Label(self.main, bg=MAIN_BG, fg=FONT_COL)

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
    def login(self, username, password):
        if password == PASSWORD and len(username) > 0:
            self.controller.show_frame(PageOne, username) #Username can be passed to parent, then PageOne, here for current session info

        elif (len(username) == 0) or username == None:
            self.error_label.grid(row=0, column=0)
            self.error_label['text'] = "Please enter a username"
            self.label_entry_boxes.grid(row=1, column=0)

        elif (len(username) > 0 and (password != PASSWORD or password == None)):
            self.label_entry_boxes.grid(row=1, column=0)
            self.error_label.grid(row=0, column=0,  columnspan=2)
            self.error_label['text'] = "Incorrect Password"

        #sendmsg function that passes info from A to B
    def sendmsg(self, msg ):
        self.last_user['text'] = "Last User: " + msg
        self.last_user.grid(row=2, column=1, pady=(0, 10), padx=10, sticky="N")

        for item in self.entries:
            if item['name'] == 'name':
                item['widget'].delete(0, tk.END) #clear entry box for username upon return to StartPage once closed session

#Class for the Page One where username is passed through & session begins
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #create the DB and tables if not present in dir - created when session starts so in PageOne
        if MAKE_DB:
            needcreate = not os.path.exists('./' + DB_NAME)
            if needcreate:
                db = Database(DB_NAME)
                for table in TABLES:
                    db.create_table(table['table_name'], table['columns'])

        #widgets for main page
        self.header = tk.Frame(master=self, bg=HEADER_BG)
        # self.header.grid(row=0, column=0, sticky="EW")
        self.header.pack(side="top", fill="x")
        # style = ttk.Style()
        # style.theme_use('alt')
        # style.theme_create( "yummy", parent="alt", settings={
        #         "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": "blue",
        #                                     } },
        #         "TNotebook.Tab": {
        #             "configure": {"padding": [5, 5], "background": "#00004d", "foreground":"white", "focusthickness":3, "focuscolor":"#ff971a" },
        #             "map":       {"background": [("selected", "orange")],
        #                           "expand": [("selected", [1, 1, 1, 0])] } },
        #                 "TButton": {
        #             "configure": {"background": "#e67e00", "foreground":'white', "focusthickness":3, "focuscolor":'#ff971a'},
        #             "map": { "background": [('active','#ff971a')]}
        #                 }
        #         } )
        #
        # style.theme_use("yummy")
        headerstyle = ttk.Style(self.header)
        # headerstyle.theme_use('alt')
        headerstyle.theme_use('alt')
        headerstyle.configure('TButton', background = "#e67e00", foreground = 'white', focusthickness=3, focuscolor='#ff971a')
        headerstyle.map('TButton', background=[('active','#ff971a')])
        headerstyle.configure('TNotebook', tabmargins = [2, 5, 2, 0], background=MAIN_BG, borderwidth=0)
        headerstyle.configure('TNotebook.Tab', padding = [5, 5], background="orange", foreground="white", focusthickness=3, focuscolor="#ff971a")
        headerstyle.map('TNotebook.Tab', background = [("selected", HEADER_BG)], expand =[("selected", [1, 1, 1, 0])])
        headerstyle.configure('Wild.TRadiobutton',    # First argument is the name of style. Needs to end with: .TRadiobutton
            background=HEADER_BG,         # Setting background to our specified color above
            foreground='white')
            #https://stackoverflow.com/questions/37234071/changing-the-background-color-of-a-radio-button-with-tkinter-in-python-3
        # noteStyle = ttk.Style()
        # noteStyle.theme_create( "yummy", parent="alt", settings={
        #         "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        #         "TNotebook.Tab": {
        #             "configure": {"padding": [5, 1], "background": "green" },
        #             "map":       {"background": [("selected", "red")],
        #                           "expand": [("selected", [1, 1, 1, 0])] } } } )
        #
        # noteStyle.theme_use("yummy")


        #Main Container
        self.main_section = tk.Frame(master=self, bg=MAIN_BG)
        self.main_section.pack(side="bottom", fill="both", expand=True)

        canvas = tk.Canvas(self.main_section, bg="aqua", borderwidth=0, highlightthickness=0)  #create a canvas, canvas has the scrollbar functionality

        #frame is the scrollable area
        frame = tk.Frame(canvas, bg="brown", height=250, width=250)
        yscrollbar = ttk.Scrollbar(self.main_section, orient="vertical", command=canvas.yview) #add the scrollbar to the container on the y
        xscrollbar = ttk.Scrollbar(self.main_section, orient="horizontal", command=canvas.xview) #add the scrollbar to the container on the x

        frame.bind( #function for ensuring the scrolling capacity is for all the text
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        self.page_title = tk.Label(self.header, text="Delineation Can Commence", font=LARGE_FONT, foreground=FONT_COL, bg=HEADER_BG)      # Store this as an instance variable
        self.page_title.pack(side="left", pady=10, padx=10)

        #load scans button frame (incs 2 load scans btns) & arrow btns (Close tabs & config settings also in the frame)
        self.browse_frame = tk.Frame(frame, bg=MAIN_BG)
        self.browse_frame.pack(side="top", fill="x")

        self.browse_frame.rowconfigure(0, weight=1)
        self.browse_frame.columnconfigure(0, weight=1)
        self.browse_frame.columnconfigure(1, weight=1)
        self.browse_frame.columnconfigure(2, weight=1)

        #Number of tab panes that are created
        self.num_notebooks = 2 #2 notebooks created at start
        self.notebook_frames = []
        self.comparison_open = False #if two panes are being compared then is true, start with no comparisons
        self.current_figures = []
        self.all_tabs = []

        self.panes = []

        #Tab area & Panes
        self.tab_area = tk.Frame(frame, background=MAIN_BG)
        self.tab_area.pack(side="bottom", fill="both", expand=True)

        #create the notebooks
        # for i in range(self.num_notebooks):
        #     notebook_frame = tk.Frame(self.tab_area, bg="red")
        #
        #     if not self.comparison_open and i = 0:
        #         notebook_frame.grid(row=0, column=i, sticky="NSWE") #only grid out first frame
        #         self.tab_area.rowconfigure(0, weight=1) #set grid area so only one tab area if presented
        #         self.tab_area.columnconfigure(i, weight=1)
        #     elif self.comparison_open:
        #          notebook_frame.grid(row=0, column=i, sticky="NSWE") #grid every frame if comparison open
        #          self.tab_area.rowconfigure(0, weight=1) #all frames are on 0 row
        #          self.tab_area.columnconfigure(i, weight=1) #columns would increase depending on comparison
        #
        #     notebook = ttk.Notebook(notebook_frame)
        #     notebook.pack(side="left", fill="both", expand=True, pady=(0, 10), padx=10)
        #     self.notebook_frames.append({"parent_frame": notebook_frame, "notebook":notebook, "tabs": None, "slice_information": None}) #collect all frames together & notebooks inc current tabs & INformationBox obj
        #
        # for notebook in self.notebook_frames:
        #     notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_viewing_information(notebook['notebook'], notebook['slice_information'], notebook['tabs']))


        self.notebook_1_frame = tk.Frame(self.tab_area, bg="red") #frame for notebook one (either central tab pane or left hand side pane)
        self.notebook_1_frame.grid(row=0, column=0, sticky="NSWE")
        self.panes.append(self.notebook_1_frame)
        self.notebook_2_frame = tk.Frame(self.tab_area, bg="yellow") #frame for notebook two (right hand pane)
        self.panes.append(self.notebook_2_frame)

        self.tab_area.rowconfigure(0, weight=1) #currently only one tab is presented so grid area set so (tab area is whole area includes both tab panes)
        self.tab_area.columnconfigure(0, weight=1)

        self.tab_pane = ttk.Notebook(self.notebook_1_frame)
        # self.tab_pane = CustomNotebook(self.main_section)

        self.slice_info = None
        self.slice_info_tab_2 = None

        self.tab_pane.bind("<<NotebookTabChanged>>", lambda e: self.update_viewing_information(self.tab_pane, self.slice_info, self.tabs_1)) #Used to know which tab is selected for that particular notebook
        #https://stackoverflow.com/questions/48104061/python-tkinter-bindtag-event-handling-how-to-update-which-tab-is-currently-sel
        self.tab_pane.pack(side="left", fill="both", expand=True, pady=(0, 10), padx=10)

        #This is used to store instances of tab panes when they are open
        self.tabs_1 = []
        self.tabs_2 = []
        self.first_notebook_tabs = []
        self.second_notebook_tabs = []


        self.tab_pane_2 = ttk.Notebook(self.notebook_2_frame)
        # self.tab_pane = CustomNotebook(self.main_section)
        self.tab_pane_2.bind("<<NotebookTabChanged>>", lambda e: self.update_viewing_information(self.tab_pane_2, self.slice_info_tab_2, self.tabs_2)) #Used to know which tab is selected
        #https://stackoverflow.com/questions/48104061/python-tkinter-bindtag-event-handling-how-to-update-which-tab-is-currently-sel
        self.tab_pane_2.pack(side="left", fill="both", expand=True, pady=10, padx=10)

        #Frame for the controls & btns
        self.load_stacks_controls = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.load_stacks_controls.grid(column=0, row=0, sticky="NSWE")

        self.load_stacks_buttons_dict = [{"name": "load a stack", "command":lambda tab_pane = self.tab_pane: self.load_scans(tab_pane), "default_state": "normal", "side":"left", "width":25},
                                        {"name": "load a comparison stack", "command":lambda tab_pane = self.tab_pane_2: self.load_scans(tab_pane), "default_state": "disabled", "side":"left", "width":25}]
        self.load_stacks_buttons = ButtonCreator(self.load_stacks_controls, self.load_stacks_buttons_dict)

        #swap buttons frame & btns
        self.swap_btn_frame = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.swap_btn_frame.grid(column=1, row=0, sticky="NSWE")

        self.arrow_btn_dict = [{"name": "<", "command":lambda side = "left", to_pane = self.tab_pane_2, from_pane = self.tab_pane: self.swap_tab(side, to_pane, from_pane), "default_state": "normal", "side":"left", "width":5},
                                {"name": ">", "command":lambda side = "right", to_pane = self.tab_pane, from_pane = self.tab_pane_2: self.swap_tab(side, to_pane, from_pane), "default_state": "normal", "side":"left", "width":5}]
        self.arrow_btns = ButtonCreator(self.swap_btn_frame, self.arrow_btn_dict) #create arrow buttons
        self.arrow_btns.forget_btns() #forget arrow buttons unless there are two tab panes open

        #swap buttons frame & btns (contains close tabs & settings config btn)
        self.other_btns_frame = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.other_btns_frame.grid(column=2, row=0, sticky="NSWE")


        self.other_btns_dict = [{"name": "polygon settings", "command":lambda  function=self.open_settings_config: function(), "default_state": "normal", "side":"right", "width":15},
                                {"name": "close all tabs", "command":lambda function=self.remove_tabs: function(), "default_state": "disabled", "side":"right", "width":15}]
        self.other_btns = ButtonCreator(self.other_btns_frame, self.other_btns_dict) #create arrow buttons

        #Controls for quiting or heading back to Start Page
        self.header_btns = tk.Frame(master=self.header, bg=HEADER_BG)
        self.header_btns.pack(side="right", pady=10, padx=10)

        self.quit_btn = ttk.Button(self.header_btns, text="Quit", command=quit, width=12)
        self.quit_btn.grid(row=0, column=0, pady=(0, 10))

        self.close_session_btn = ttk.Button(self.header_btns, text="Close Session", command=lambda: self.controller.show_frame(StartPage, self.entry.get()), width=12)
        self.close_session_btn.grid(row=1, column=0)

        #Information for User currently on program
        self.session_info = InformationBox(self.header, "right", 2, "Current Session", None, HEADER_BG, FONT_COL, False)

        self.currently_viewing_frame = tk.Frame(self.header, bg=HEADER_BG)
        self.currently_viewing_frame.pack(side="right")

        canvas.create_window((0, 0), window=frame, anchor="n") #position the canvas

        canvas.pack(side="left", fill="both", expand=True) #put the text frame on the left
        # canvas.grid(row=0, column=0, sticky="NSEW")
        # canvas.columnconfigure(0, weight=1)
        canvas.configure(yscrollcommand=yscrollbar.set) #so it scroll only for canvas area for the y
        canvas.configure(xscrollcommand=xscrollbar.set) #so it scroll only for canvas area for the x
        yscrollbar.pack(side="right", fill="y") #put the scroller on the right hand side
        xscrollbar.pack(side="bottom", fill="x") #put the scroller on the right hand side

    def add_comparison_frame(self):
        if self.comparison_open == False:
            self.panes[0].grid(row=0, column=0, sticky="NSWE")
            self.panes[1].grid(row=0, column=1, sticky="NSWE")
            self.tab_area.rowconfigure(0, weight=1)
            self.tab_area.columnconfigure(0, weight=1)
            self.tab_area.columnconfigure(1, weight=1)
            self.comparison_open = True
        elif self.comparison_open == True:
            self.panes[1].grid_forget()
            self.tab_area.columnconfigure(0, weight=1)
            self.tab_area.columnconfigure(1, weight=0)
            self.comparison_open = False

    def unlock_comparison_stacks_btn(self):
        if len(self.tabs_1) > 0:
            self.load_stacks_buttons.enable_all_btns() #load comparison button is now enabled
        else:
            self.load_stacks_buttons.change_to_default_states() #load comparison stacks button goes back to disabled, load stack to normal

    #Updates the viewing information in the Information Box for each slice
    def update_viewing_information(self, notebook, currently_viewing_info, tabs):
        #if length of tabs is less than two then focused tab will be tab in existance anyway, destorying the tabs actually focuses each tab in turn
        if len(tabs) > 1:
            text = notebook.tab(notebook.select(), "text")
            #https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook
            text = re.split(" | ", text)
            #change currently viewing on tab select not load of scans
            # info = [text[0], text[4], text[2]]
            figure_information = {"year": text[0], "scan type": text[4], "patient":text[2]}
            currently_viewing_info.refresh_information(figure_information)

        #temp thing to destroy the frames - need to really create a session class that is called

    #Function that is called when the session is closed
    def destroyFrame(self, StartPage, username):
        #reset to defaults
        self.hard_reset_settings()

        #resets the slice info to not applicable
        if self.slice_info != None:
            self.slice_info.reset_to_na()

        #removes the tabs
        self.remove_tabs()

        #Head back to the start page
        self.controller.show_frame(StartPage, username)

    #Function is called by the "owner" of PageOne, MainApp, which can pass messages for us
    def sendmsg(self, username):
        #update the information box that displays the session information
        session_information = {"user": username, "start time": start_time()} #call time to get current time this is called
        self.session_info.create_insides(session_information)

        self.close_session_btn.destroy() #Need to destroy current close session btn
        self.close_session_btn = ttk.Button(self.header_btns, text="Close Session", command=lambda: self.destroyFrame(StartPage, username), width=12)
        self.close_session_btn.grid(row=1, column=0)

    #Function that loads up a folder of slices in a new tab
    def load_scans(self, notebook):
        folder_selected = tk.filedialog.askdirectory(initialdir = DIRECTORY, title = "Browse Files For your MRIs!!!") #browse directories
        options = []
        for item in os.listdir(folder_selected):
            if item.endswith('.npy'): #has to be a numpy file
                options.append(str(item))
        if len(options) > 0: #if there are numpy file options in the folder
            # try:
                if len(self.tabs_1) < 1:
                    #Information for slice selected box created when first tab loaded
                    self.slice_info = InformationBox(self.currently_viewing_frame, "left", 2, "Currently Viewing Tab 1", None, HEADER_BG, FONT_COL, False)

                if (notebook == self.tab_pane_2) and len(self.tabs_2) < 1:
                    self.slice_info_tab_2 = InformationBox(self.currently_viewing_frame, "right", 2, "Currently Viewing Tab 2", None, HEADER_BG, FONT_COL, False)
                    self.add_comparison_frame()

                    self.arrow_btns.pack_btns(5, 5) #pack the arrow buttons

                slice_address_segments = re.split("/", folder_selected) #split directory address
                new_tab = Tab(notebook, HEADER_BG) #create a new tab instance
                tab_pane = new_tab.add_tab(slice_address_segments[7] + " | " + slice_address_segments[8] + " | " +  slice_address_segments[10])
                self.tabs_1.append(tab_pane) #add the pane to self.tabs - works with the remove tabs btn
                # self.list_of_tabs.append({"tab_obj": new_tab, "tab_pane_frame":tab_pane})

                self.figure_information = {"year":slice_address_segments[7], "scan type":slice_address_segments[10], "patient":slice_address_segments[8]}
                # info = [slice_address_segments[7], slice_address_segments[10], slice_address_segments[8]]
                if notebook == self.tab_pane:
                    # self.slice_info.state_information(info) #updates the slice info for the current loaded up tab - loaded tab is one in focus
                    self.slice_info.create_insides(self.figure_information)
                    self.first_notebook_tabs.append({"tab_obj": new_tab, "tab_pane_frame":tab_pane})


                if notebook == self.tab_pane_2:
                    self.tabs_2.append(tab_pane)
                    self.second_notebook_tabs.append({"tab_obj": new_tab, "tab_pane_frame":tab_pane})
                    # self.slice_info_tab_2.state_information(info)
                    self.slice_info_tab_2.create_insides(self.figure_information)

                figure = SliceFigure(tab_pane, folder_selected,  options, True, 0, self.session_info.pull_detail('User'), self.figure_information, self) #creates the figure for the tab
                self.current_figures.append(figure)
                # self.close_tabs_btn['state'] = "normal" #can now close all tabs
                self.other_btns.enable_btn("close all tabs") #enable close btn
                self.unlock_comparison_stacks_btn()
        else:
            messagebox.showerror("Error Loading MRI Slices", "There are no Numpy Array Files available within this folder.") #there were no numpy arrays in the folder

    #Function to remove all tabs
    def remove_tabs(self):
        if len(self.tabs_1) > 0:
            for tab in self.tabs_1:
                tab.destroy()

        self.tabs_1.clear() #remember to clear the self.tabs as this is not reset as page one is not called by original class it is lifted above
        self.tabs_2.clear()
        # self.close_tabs_btn['state'] = "disabled" #now no tabs to remove
        self.other_btns.enable_btn("close all tabs") #disable close btn as no tabs to close
        # self.slice_info.reset_to_na() #reset slice information to not applicable

        if self.slice_info != None:
            self.slice_info.make_box_go_walkies()
            self.slice_info = None
        if self.slice_info_tab_2 != None:
            self.slice_info_tab_2.make_box_go_walkies()
            self.slice_info_tab_2 = None

        self.comparison_open = True #resets the screen to one screen
        self.unlock_comparison_stacks_btn()
        self.add_comparison_frame()
        self.arrow_btns.forget_btns() #remove arrow buttons from show

        self.current_figures.clear()

    def swap_tab(self, direction, current_notebook, destination_notebook):
        print(current_notebook)
        print("INDEX", current_notebook.index("current"))
        text = current_notebook.tab(current_notebook.select(), "text") #get text of currently selected notebook (this would be the tab that the user wants to move)
        # print("TAB", current_notebook.tab())
        #get index of currently selected tab


        text = re.split(" | ", text)
        #change currently viewing on tab select not load of scans

        print("TEXT", text)

        info = [text[0], text[2], text[4]]

        info.insert(2, "01")
        folder = DIRECTORY + "/"
        for item in info:
            folder += item + "/"

        options = []
        for item in os.listdir(folder):
            if item.endswith('.npy'): #has to be a numpy file
                options.append(str(item))

        slice_address_segments = re.split("/", folder)

        # try:
        new_tab = Tab(destination_notebook, HEADER_BG) #create a new tab instance
        tab_pane = new_tab.add_tab(text[0] + " | " + text[2] + " | " +  text[4])
        self.tabs_1.append(tab_pane)

        figure_information = {"year": slice_address_segments[7], "scan type":slice_address_segments[10], "patient":slice_address_segments[8]}

        SliceFigure(tab_pane, folder,  options, True, 0, self.session_info.pull_detail('User'), figure_information, self)

        current_notebook.forget(current_notebook.select())

        if len(current_notebook.tabs()) == 0:
            if direction == "left":
                print("hello")
                self.comparison_open == True
                self.arrow_btns.forget_btns() #remove arrow buttons from show

                self.add_comparison_frame()

                self.tabs_2.clear()
                self.slice_info_tab_2.make_box_go_walkies()
                self.slice_info_tab_2 = None

        elif len(current_notebook.tabs()) == 1:
            if direction == "right":
                self.arrow_btns.disable_btn(">") #if only one tab in left hand side pane, then cannot swap another tab to left hand side pane
                # self.swap_to_right_btn['state'] = 'disabled'
        else:
            if direction == "right":
                self.arrow_btns.enable_btn(">")
                # self.swap_to_right_btn['state'] = 'normal'

    # except Exception as e:
    #     print(e)
        # messagebox.showerror("Error Loading MRI Slices", "An error occured loading this folder.")
        #remove from apropiate tabs list
        #add to appropiate tabs list
        #check if any tabs in tab pane 2 - if none then go back to whole screen

    #Function that refreshes the tabs with the new settings
    def open_settings_config(self):
        result = PolygonSettings(SETTINGS).send() #create Settings class
        if result and len(self.current_figures) > 0:
            self.refresh_figures()

    #This is used to refresh the slice figure class for settings that are configuable. I don't delete the tab due to UX comfort
    def refresh_figures(self):
        for figure in self.current_figures:
            figure.refresh()

    #When the session is closed the settings are hard reset to their default values
    def hard_reset_settings(self):
        for item in SETTINGS:
            item['current_value'] = item['default_value']
            item['temp_value'] = None

    def sync_tabs(self, figure_information):
        for figure in self.current_figures:
            #don't sync tabs if they are the same scan type of the same patient
            if (figure.figure_information['patient'] == figure_information['patient'] and figure.figure_information['year'] == figure_information['year']):
                figure.sync_btn['text'] = 'Tab Synced'
                figure.sync_btn['background'] = "red"
                figure.sync_btn['foreground'] = "white"
                CreateToolTip(figure.sync_btn, "Click to DeSync all Tabs", HOVER_BG, SMALL_FONT) #if clicked, de syncs all tabs from polygon translation

                figure.synchronised_status = True
    def unsync_tabs(self, figure_information):
        for figure in self.current_figures:
            if (figure.figure_information['patient'] == figure_information['patient'] and figure.figure_information['year'] == figure_information['year']):
                figure.sync_btn['text'] = 'Synchronise'
                figure.sync_btn['background'] = "light gray"
                figure.sync_btn['foreground'] = "black"
                CreateToolTip(figure.sync_btn, "Click to Synchronise Tabs of Patient " + figure_information['patient'], HOVER_BG, SMALL_FONT)

                figure.synchronised_status = False

#Class for the Figure generated by selecting a folder
class SliceFigure:
    def __init__(self, parent_frame, folder_selected, slice_list, new_load, current_position, username, figure_information, parent):
        self.parent = parent

        self.frame = parent_frame
        self.username = username
        self.figure_information = figure_information
        self.folder_selected  = folder_selected
        self.current_position = current_position
        self.slice_list = slice_list
        self.intro_label_frm_txt = "Stack: "

        #This is changed if the figure is synced
        self.synchronised_status = False

        #start off settings that can be changed
        self.settings = SETTINGS
        self.figure_background = self.get_setting("Figure Background")
        self.default_tag_index = self.get_setting("Default Tag")


        self.graph_frame = tk.Frame(self.frame, background=HEADER_BG)
        self.graph_frame.pack()
        #Frame includes the dropdown & the information labels
        self.graph_frame_header = tk.Frame(self.graph_frame, background=HEADER_BG)
        self.graph_frame_header.pack(side="top", fill="x", padx=10, pady=10)
        self.graph_frame_header.grid_columnconfigure(0, weight=1) #evenly space out the labels
        self.graph_frame_header.grid_columnconfigure(1, weight=1)
        self.graph_frame_header.grid_columnconfigure(2, weight=1)

        #Sub frame contianing the label & tag drop down
        self.polygon_tag_frame = tk.Frame(self.graph_frame_header, background=HEADER_BG)
        self.polygon_tag_frame.grid(row=0, column=0, sticky="W")

        self.polygon_tag_var = tk.StringVar(self.frame)
        self.polygon_tags = self.load_tags()
        # self.polygon_tag_var.set(self.polygon_tags[0]) # default value is shown, to then be changed for speed

        self.polygon_tag_var.set(self.polygon_tags[self.default_tag_index])
        self.polygon_tag_chosen = self.polygon_tag_var.get() #assign variable to default

        self.polygon_tag_lab = tk.Label(self.polygon_tag_frame, text="Draw: ", background=HEADER_BG, fg=FONT_COL)
        self.polygon_tag_lab.grid(row=0, column=0, sticky="W")

        self.polygon_tag_choice = ttk.Combobox(self.polygon_tag_frame, values=self.polygon_tags) #Use ttk. combo box as looks more appealing
        self.polygon_tag_choice.current(self.default_tag_index) #current value in the combo box
        self.polygon_tag_choice.grid(row=0, column=1, sticky="W", padx=5)

        self.polygon_tag_choice.bind("<<ComboboxSelected>>", self.change_tag)

        #information label, updated throughout depending on actions
        self.information = tk.Label(self.graph_frame_header, text="Hola, Me llamo Andrew", fg="green", background=HEADER_BG)
        self.information.grid(row=0, column=1, sticky="W")

        self.sync_btn = tk.Button(self.graph_frame_header, text="Synchronise", command=self.synchronise)
        self.sync_btn.grid(row=0, column=2, sticky="E", padx=10)
        # self.sync_tooltip = CreateToolTip(self.sync_btn, "Click to Synchronise Tabs of Patient " + self.figure_information['patient'], HOVER_BG, SMALL_FONT)

        #Graph Frame
        self.slice_name = self.slice_list[self.current_position][:-4]

        self.fig_frame = tk.LabelFrame(self.graph_frame, text="  {} {} ".format(self.intro_label_frm_txt, self.slice_name), background=HEADER_BG, foreground=FONT_COL)
        self.fig_frame.pack(padx=10, pady=(0, 10))
        self.fig_frame_inner = tk.Frame(self.fig_frame, background=self.figure_background)
        self.fig_frame_inner.pack()

        #Figure, Axis & Canvas
        self.figure = Figure()
        self.a = self.figure.add_subplot(111) #only one chart
        self.a.grid(False)

        self.a.axis("off")
        self.figure.patch.set_facecolor(self.figure_background)
        self.figure.subplots_adjust(left=0,right=1,bottom=0,top=1)
        self.a.format_coord = lambda x, y: "[{}, {}]".format(str(x)[:4], str(y)[:4]) #https://stackoverflow.com/questions/36012602/disable-coordinates-from-the-toolbar-of-a-matplotlib-figure
        self.canvas = FigureCanvasTkAgg(self.figure, self.fig_frame_inner) #would normally run plot.show() but show in tkinter window
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        self.fc = cidPress(self.figure) #class of cid

        # self.figure.canvas("<leave_notify_event>", lambda e: self.print_hello(e))


        #Toolbar
        self.toolbar = CustomToolbar(self.canvas, self.fig_frame) # self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame) = I have used a CustomToolbar
        self.toolbar.config(background=HEADER_BG)
        self.toolbar.update()
        self.figure.canvas.mpl_connect('figure_leave_event', self.leave_figure)
        # self.a.format_coord = lambda x, y: "[{}, {}]".format(str(x)[:4], str(y)[:4])
        #https://stackoverflow.com/questions/48351630/how-do-you-set-the-navigationtoolbar2tkaggs-background-to-a-certain-color-in-tk
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.toolbar.children['!button6'].pack_forget() #to forget the configure subplots button
        self.toolbar.children["!button2"].config(background="orange", foreground="white")
        self.toolbar.children["!button3"].config(background="orange")
        self.toolbar.children["!button4"].config(background="orange")
        self.toolbar.children["!button5"].config(background="orange")
        # self.toolbar.children["!button0"].config(background="orange")
        self.toolbar.children["!button7"].config(background="orange")

        #Custom Buttons Frame
        custom_btn_frame = tk.Frame(master=self.toolbar, background=HEADER_BG)
        custom_btn_frame.pack(side = "left")

        #Custom Buttons
        btn_width, btn_height = 24, 24
        self.custom_btns = [{"name": 'Jump to First Slice', "text": "_", "padding": (5, 1), "description": 'start', "dlft_state": "normal", "command": lambda name="start": self.click_tb_btn('start')},
                            {"name": 'Jump to Last Slice', "text": "_", "padding": (1, 2), "description": 'end', "dlft_state": "normal", "command": lambda: self.click_tb_btn('end')},
                            {"name": 'Play Slice Slideshow', "text": "_", "padding": (5, 5), "description": 'play', "dlft_state": "normal", "command": lambda: self.click_tb_btn('play')},
                            {"name": "Draw Polygon", "text": "_", "padding": (0, 2), "description": 'draw', "dlft_state": "normal", "command": lambda name="draw": self.click_tb_btn("draw")},
                            {"name": "Select Polygon", "text": "_", "padding": (0, 2), "description": 'select', "dlft_state": "disabled", "command": lambda name="select": self.click_tb_btn("select")},
                            {"name": "Edit Polygon", "text": "_", "padding": (0, 2), "description": 'edit', "dlft_state": "disabled", "command": None},
                            {"name": "Delete Polygon", "text": "_", "padding": (0, 2), "description": 'delete', "dlft_state": "disabled", "command": None},
                            {"name": "Show Polygons", "text": "ON", "padding": (0, 2), "description": 'show', "dlft_state": "normal", "command": lambda name="show": self.click_tb_btn("show")},
                            {"name": "Edit Polygon Tag", "text": "_", "padding": (0, 2), "description": 'edit_tag', "dlft_state": "disabled", "command": None},
                            {"name": "Refresh Polygons", "text": "_", "padding": (0, 2), "description": 'refresh', "dlft_state": "normal", "command": lambda name="refresh": self.click_tb_btn("refresh")}
                            ]
        #create the images for the buttons
        images = ConvertImages(custom_btn_images)
        imgs_custom_btns = images.prepare_images()

        #assign image to correct btn in dict above
        for item in imgs_custom_btns:
            for btn in self.custom_btns:
                if item['name'] == btn['name']:
                    btn['image'] = item['image']
        #Create the btns
        i = 0
        for btn in self.custom_btns:
            button = tk.Button(master=custom_btn_frame, image=btn['image'], command=btn['command'], state = btn['dlft_state'])
            btn['widget'] = button
            button.config(width=btn_width, height=btn_height)
            CreateToolTip(button, btn['name'], HOVER_BG, SMALL_FONT) #calling of instance of tooltip for draw btn
            button.grid(row=0, column=i, padx=btn['padding'])
            i += 1
            #https://stackoverflow.com/questions/47212078/tkinter-how-to-replace-a-button-with-a-image

        #load up First Figure
        if new_load == True:
            self.create_figure(self.fig_frame)

        self.pause = False
        self.clicked = 0

        #create instance of json file writer here
        self.selected_polygon = None
        self.current_slice = None

        #Notebox Class is called to make this appear when calling Slice Figure
        self.notebox = Notebox(self.frame, self.username, self.slice_list[self.current_position][:-4], self.figure_information, self.folder_selected, self.slice_list)
        #Instance of Json File Writer
        self.filename = self.folder_selected + "/" + self.slice_list[self.current_position][:-4] + '_polygon_data.json'
        self.jsonFileWriterPolygon = jsonFileWriterPolygon(self.filename, self.slice_list[self.current_position][:-4])
        #Instance of Polygons upon the Slice
        self.slice_polygons = Polygons(self.jsonFileWriterPolygon, self.slice_list[self.current_position][:-4], self.figure, self.a, self.custom_btns, self.fc, self.information, self)

    def leave_figure(self, event):
        self.toolbar.left_figure(event)

    def create_figure(self, graph_frame):
        self.fig_frame['text'] = "  {} {} ".format(self.intro_label_frm_txt, self.slice_list[self.current_position][:-4])
        slice_address = self.folder_selected + "/" + self.slice_list[self.current_position]
        # slice = np.load(slice_address)
        #
        # self.a.imshow(np.squeeze(slice), cmap='gray')
        img=mpimg.imread("./images/squirrel.png")
        self.a.imshow(img)

        self.filename = self.folder_selected + "/" + self.slice_list[self.current_position][:-4] + '_polygon_data.json'
        self.jsonFileWriterPolygon = jsonFileWriterPolygon(self.filename, self.slice_list[self.current_position][:-4])
        self.slice_polygons = Polygons(self.jsonFileWriterPolygon, self.slice_list[self.current_position][:-4], self.figure, self.a, self.custom_btns, self.fc, self.information, self)
        self.canvas.draw() #canvas.show does not work anymore

        self.determine_btn_status()

    #passes figure_information from the class where the sync was made up
    def synchronise(self):
        if not self.synchronised_status:
            self.parent.sync_tabs(self.figure_information)
        else:
            #unsync
            self.parent.unsync_tabs(self.figure_information)

    def get_selected_polygon(self, polygon):
        self.selected_polygon = polygon
        self.notebox.set_selected_polygon(polygon)
        # self.current_slice = slice

    def get_setting(self, setting_name):
        return [item['current_value'] for item in self.settings if item['setting'] == setting_name][0]

    #Function that refreshes the slice figure if a setting is changed through config settings
    def refresh(self):
        self.settings = SETTINGS
        #figure background change
        self.figure_background = self.get_setting("Figure Background")
        self.figure.patch.set_facecolor(self.figure_background) #doesn't need canvas draw, resets colour
        self.fig_frame_inner['background'] = self.figure_background #sets background of the inner frame

        self.default_tag_index = self.get_setting("Default Tag")
        self.polygon_tag_var.set(self.polygon_tags[self.default_tag_index]) #set the value to the variable
        self.polygon_tag_choice.current(self.default_tag_index) #set the current value of the combo box
        self.change_tag(None) #need to then reassign this as the current tag is changed

        #load polygons
        self.slice_polygons.load_polygons() #reloads the polygons

        #load new tags & assign to dropdown
        self.polygon_tag_choice['values'] = self.load_tags()

    def click_tb_btn(self, btn):
        # self.figure.canvas.mpl_disconnect(self.cid)
        self.fc.disconnect()
        if btn == 2:
            self.current_position -= 1
            self.create_figure(self.fig_frame)
            self.notebox.update_slice_name(self.slice_list[self.current_position][:-4])

        elif btn == 3:
            self.current_position += 1
            self.create_figure(self.fig_frame)
            self.notebox.update_slice_name(self.slice_list[self.current_position][:-4])
            # self.jsonFileWriterPolygon = jsonFileWriterPolygon(self.filename, self.slice_list[self.current_position][:-4])
            # self.slice_polygons = Polygons(self.settings, self.jsonFileWriterPolygon, self.slice_list[self.current_position][:-4], self.figure, self.a, self.custom_btns, self.fc, self.information)

        elif btn == "play":
            self.play_slideshow()
        elif btn == "start":
            self.current_position = 0
            self.create_figure(self.fig_frame)
            self.notebox.update_slice_name(self.slice_list[self.current_position][:-4])
            # self.jsonFileWriterPolygon = jsonFileWriterPolygon(self.filename, self.slice_list[self.current_position][:-4])
            # self.slice_polygons = Polygons(self.settings, self.jsonFileWriterPolygon, self.slice_list[self.current_position][:-4], self.figure, self.a, self.custom_btns, self.fc, self.information)

        elif btn == "end":
            self.current_position = len(self.slice_list) - 1
            self.create_figure(self.fig_frame)
            self.notebox.update_slice_name(self.slice_list[self.current_position][:-4])

        elif btn == "draw":
            self.fc.connect(lambda event: self.slice_polygons.draw_btn_click(event, self.polygon_tag_chosen))
        elif btn == "select":
            self.fc.connect(lambda event: self.slice_polygons.select_polygon(event))
        elif btn == "show":
            self.fc.connect(self.slice_polygons.show_polygons())
        elif btn == "refresh":
            self.fc.connect(self.slice_polygons.load_polygons()) #load polygons just refreshs the polygons on the slice, incomplete polygons are not saved to json
            # print(btn, "Polygon btn")

    def load_tags(self):
        polygon_tags = []

        tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        tags = tags_writer.return_tags()

        for tag in tags:
            polygon_tags.append(tag['label'].capitalize())

        return polygon_tags

    #Function that sets the default tag for speed
    def set_default_tag(self, default):
        if type(default) == str:
            if default in self.poylgon_tags:
                return self.polygon_tags.index(tag)
            else:
                return 0
        elif type(default) == int:
            return default

    def play_slideshow(self):
        self.clicked += 1
        self.pause = True
        i = 0
        play_btn = self.custom_btns[2]['btn']
        #iterate through images
        while (self.clicked == 0) or (self.clicked % 2 != 0):
            # print("play")
            for slice in self.slice_list:
                # play_btn['state'] = "disabled"
                self.current_position = i
                self.create_figure(self.fig_frame)
                time.sleep(1.25)
                i += 1
        if (self.clicked % 2 == 0):
            pass
            # print("paused")

        #reset back to first image
        self.current_position = 0
        self.create_figure(self.fig_frame)

        # play_btn['state'] = "normal"
        #https://realpython.com/python-sleep/
    def determine_btn_status(self):
        start_btn = self.custom_btns[0]['widget']
        end_btn = self.custom_btns[1]['widget']
        if self.current_position == 0: #disable left as cannot go left
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="disabled")
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="normal")
            start_btn['state'] = "disabled"
            end_btn['state'] = "normal"
        elif (self.current_position == len(self.slice_list) - 1):
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="normal")
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="disabled")
            start_btn['state'] = "normal"
            end_btn['state'] = "disabled"
        else:
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="normal")
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="normal")
            start_btn['state'] = "normal"
            end_btn['state'] = "normal"

    #Called when the tag is changed, this is bound to the dropdown, ensures correct current tag is passed through
    def change_tag(self, event):
        self.polygon_tag_chosen = self.polygon_tag_choice.get()

        #Function for updating the information label

    def update_information(self, text, type):
        self.information['text'] = text
        if type == "positive":
            self.information['fg'] = "green"
        elif type == "warning":
            self.information['fg'] = "red"
        else:
            self.information['fg'] = "black"

    def draw_figure(self, figure):
        figure.canvas.draw()

#Class for the polygons upon the Slice Figure
class Polygons(SliceFigure):
    def __init__(self, file_writer, slice_name, f, a, polygon_buttons, cid, information_label, parent):
        #Tag Checker & pull tags
        # self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        # self.tags = self.tags_writer.return_tags()
        self.refresh_tags()

        # self.slice_name = slice_name
        # self.file_writer = jsonFileWriterPolygon(self.filename, self.slice_name)

        #I call the SETTINGS variable that is initialised at the start of program. It is recalled in load_polygons (i.e when the slice is refreshed)
        self.settings = SETTINGS
        self.precision = [item['current_value'] for item in self.settings if item['setting'] == "Precision"][0]
        self.line_thickness = [item['current_value'] for item in self.settings if item['setting'] == "Line Thickness"][0]
        self.select_col = [item['current_value'] for item in self.settings if item['setting'] == "Selected Polygon Colour"][0]

        self.file_writer = file_writer
        self.slice_name = slice_name


        self.co_ordinates = []
        self.num_of_lines = 0
        self.polygon_num = 0 #IDs the polygons for that are drawn - need to be taken from json file
        self.polygons_visible = True #Boolean if poylgons are visible
        self.highlighted_points = [] #stores any highlighted points that are not part of polygons
        self.selected_polygon = None #stores the selected polygon at the time
        self.polygon_info = [] #stores polygons
        self.current_slice = slice_name

        self.figure = f
        self.axis = a
        self.fc = cid

        self.polygon_buttons = polygon_buttons
        self.information = information_label
        self.parent = parent
        self.load_polygons()




        # self.get_current_slice()


    #Following two methods are inherited from Slice
    def update_information(self, text, type):
        super(Polygons, self).update_information(text, type) #Updates the information label

    def draw_figure(self):
        super(Polygons, self).draw_figure(self.figure) #draws the fig to canvas

    def refresh_tags(self):
        tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        self.tags = tags_writer.return_tags()

    #function to load the polygons & draw them to the figure
    def load_polygons(self):
        #assign polygon_info for slice, file will only contain co-ordinates, takes in full file
        file_info = self.file_writer.read_file()
        file_sorted = self.file_writer.sort_file(file_info, "slice", self.slice_name)

        self.refresh_tags()
        #only pull polygons of certain slice name
        slice_polygons = []
        for polygon in file_sorted:
            # print(self.slice_name)
            # print(polygon['slice'])
            if polygon['slice'] == self.slice_name:
                slice_polygons.append(polygon)

        #clear axis & polygon info as this will be reset - different number of polygons for next slice
        self.clear_axis_data()
        self.polygon_info.clear()

        #Recall SETTINGS as changes within the session may have been made
        self.settings = SETTINGS
        self.precision = [item['current_value'] for item in self.settings if item['setting'] == "Precision"][0]
        self.line_thickness = [item['current_value'] for item in self.settings if item['setting'] == "Line Thickness"][0]
        self.select_col = [item['current_value'] for item in self.settings if item['setting'] == "Selected Polygon Colour"][0]

        #if polygons present then draw
        if len(slice_polygons) > 0:
            #update polygon_num with the num of the last polygon entry
            last_entry = slice_polygons[-1:][0]
            self.polygon_num = last_entry['id']

            #plot polygons & create poylgon info
            for polygon in slice_polygons:
                num_of_vertexes = 0
                xlist, ylist = [], []
                for x, y in polygon['co-ordinates']:
                    xlist.append(x)
                    ylist.append(y)
                    num_of_vertexes += 1 #caluclate the num of verteces
                xlist.append(polygon['co-ordinates'][0][0]) #rememember to add first co-ordinate for x so it connects up
                ylist.append(polygon['co-ordinates'][0][1])  #rememember to add first co-ordinate for y so it connects up
                #plot on axis
                poly = self.axis.plot(xlist, ylist, color=self.get_colour(polygon['tag']), marker="o", label=polygon['id'], linewidth=self.line_thickness)
                #create polygon object to be used upon edited - try and move away from polygon_info
                polygon_objs = {}
                polygon_objs["id"] = polygon['id']
                polygon_objs["lines"] = poly
                polygon_objs["num"] = num_of_vertexes
                polygon_objs["tag"] = polygon['tag']
                polygon_objs['slice'] = self.slice_name
                polygon_objs["scatter_points"] = []
                polygon_objs["co-ordinates"] = polygon['co-ordinates']
                self.polygon_info.append(polygon_objs)

            #draw to figure
            self.draw_figure()

        else:
            #no polygons are present for this slice
            print("No Polygons Present for this Slice")

        self.check_if_polygons_present() #if polygons present then select button is enabled
        self.check_polygon_selected() #if no polygon selected then edit/remove btns disabled
        self.selected_polygon = None #no selected polygon currently
        self.update_information("Click Draw to create a polygon!", "positive") #information line

    def get_selected_polygon(self):
        # super(Polygons, self).get_selected_polygon(self.selected_polygon)
        self.parent.get_selected_polygon(self.selected_polygon)

    # def get_current_slice(self):
    #     self.parent.get_current_slice(self.current_slice)

    #A function to show/remove from view polygons, I do call the json to show so they cannot switch here and there if polygon is half complete
    def show_polygons(self):
        if self.polygons_visible:
            for button in self.polygon_buttons:
                if button['description'] == "show":
                    pass
                    # button['widget']['text'] = "OFF" #change the text for show polygons btn
                else:
                    button['widget']['state'] = "disabled" #disable all other buttons if no polygons
            self.clear_axis_data() #clear axis data which draws figure
            self.polygons_visible = False
            self.update_information("Polygons currently hidden.", "warning")
            self.selected_polygon = None
            self.get_selected_polygon()

        else:
            for button in self.polygon_buttons:
                if button['description'] == "show":
                    pass
                    # button['widget']['text'] = button['text'] #change the text for show polygons btn
                else:
                    button['widget']['state'] = button['dlft_state'] #set all other buttons to default states

            self.load_polygons() #load the polygons to figure with button states accordingly
            self.get_selected_polygon()
            self.polygons_visible = True #polygons are now visible

    #function that pulls in the settings that are saved for polygon tags colours
    def get_colour(self, tag):
        colour = False
        for preset in self.tags:
            if preset['label'].capitalize() == tag: #tag needs capitalising
                colour = True
                return preset['colour'] #colour goes with the custom made tag in the settings
        #Return polygons in colours where there are no tags present as in Pink colour - have this setable in the settings
        if not colour:
            return [item['current_value'] for item in self.settings if item['setting'] == "Unknown Tag Colour"][0]

            #function that calls the number of current polygons that are saved in the json
    def get_total_polygons(self):
        file_info = self.file_writer.read_file()
        file_sorted = len(self.file_writer.sort_file(file_info, "slice", self.slice_name)) #length would be the number
        return file_sorted

    #if polygons are present then the select button would be enabled
    def check_if_polygons_present(self):
        polygons = self.get_total_polygons()
        for button in self.polygon_buttons:
            if button['description'] == "select":
                if polygons == 0: #if there are no polygons on screen after deletion for instance
                    button['widget']['state'] = "disabled"
                else:
                    button['widget']['state'] = "normal"

    #used for ID purposes for the polygon counter
    def polygon_counter(self):
        #just increments the polygon num by one
        self.polygon_num += 1
        return self.polygon_num

    #reset the polygon colours back to their originals when for instance one is selected after another has already been selected
    def reset_polygon_cols(self):
        for polygon in self.polygon_info:
            for plot in self.axis.lines:
                if plot in polygon['lines']:
                    plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
            if len(polygon['scatter_points']) > 0:
                for plot in self.axis.collections:
                    if plot in polygon['scatter_points']:
                        plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
        self.draw_figure()

    #Add vertex & draw btns
    def draw_btn_click(self, event, tag):
        self.add_vertex(event, tag)

    #Function to create an x and y list of co_ordinates to be plotted
    def create_x_y_list(self, coords):
        xlist = []
        ylist = []
        for item in coords:
            xlist.append(item[0])
            ylist.append(item[1])
        return xlist, ylist

    #Function to add a vertex & draw a polygon, then save it
    def add_vertex(self, event, tag):
        colour = self.get_colour(tag)

        #reset polygon selected to be None, colours, remove highlighted pts etc
        self.selected_polygon = None
        self.reset_polygon_cols()
        self.check_polygon_selected()
        self.remove_highlighted_points()

        #first plot that is made by user
        label = str(self.polygon_num + 1) + " polygon"
        if not(event.xdata == None and event.ydata == None): #in case the user clicks the white border area
            if len(self.co_ordinates) == 0:

                self.co_ordinates.append([event.xdata, event.ydata])
                a = self.axis.scatter(event.xdata, event.ydata, s=30, color=colour) #create the scatter point so can be edited and the lines would move ?
                self.draw_figure()
                self.num_of_lines +=1

            #For last plot that is made by user eg. the final plot or clicking the first co-ordinate of the polygon
            elif (np.abs(self.co_ordinates[0][0] - event.xdata) < self.precision) and (np.abs(self.co_ordinates[0][1] - event.ydata) < self.precision) and (len(self.co_ordinates) != 0): #np.abs allows the number to be positive only
                self.co_ordinates.append([self.co_ordinates[0][0], self.co_ordinates[0][1]]) #re-add the co-ords of the first point

                coords = self.create_x_y_list(self.co_ordinates)
                label = label + "final"
                v = self.axis.plot(coords[0], coords[1], color=colour, marker="o", label=label, linewidth=self.line_thickness)
                self.draw_figure()

                #formulate polygon infomation
                polygon_objs = {}
                id = self.polygon_counter() #polygon_counter incremements the polygon number everytime a polygon has been completed
                polygon_objs["id"] = id
                polygon_objs["lines"] = self.axis.lines[-self.num_of_lines:] #pulls the last ones from the drawn polygon from axis.lines which contains all the lines
                polygon_objs["num"] = self.num_of_lines
                polygon_objs['tag'] = tag
                print("POLYGON TAG", tag)
                polygon_objs['slice'] = self.slice_name

                polygon_objs["scatter_points"] = self.axis.collections[-self.num_of_lines:] #pulls the last ones from the drawn polygon from axis.collections which contains all the collections
                self.co_ordinates.pop() #as I added the first one on again so need to remove
                polygon_objs["co-ordinates"] = self.co_ordinates
                self.polygon_info.append(polygon_objs) #append the polygon info for this polygon to the wider dict

                #save to json
                data = {"id": id, "slice": self.slice_name, "tag": tag, "co-ordinates": self.co_ordinates}
                self.file_writer.add_polygon(data)

                #update information label
                self.update_information("Polygon with id: {} saved successfully".format(str(id)), "positive")

                #reset details
                self.co_ordinates = []
                self.num_of_lines = 0

                self.check_if_polygons_present() #select btn now allowed

                #For any other point that is plotted
            elif (len(self.co_ordinates) != 0):
                #see if there are any intersections with this point, there could be intersections if there are polygons
                if len(self.polygon_info) > 0:
                    intersection = PolygonIntersector(self.polygon_info, None)
                    intersector = intersection.find_intersection([self.co_ordinates[-1:][0], (event.xdata, event.ydata)])
                else:
                    intersector = False #if there are no polygons then no intersections

                    #If there is no intersection - it is false
                if not intersector:
                    self.co_ordinates.append([event.xdata, event.ydata])
                    a = self.axis.scatter(event.xdata, event.ydata, s=30, color=colour)
                    self.update_information("Plot plotted successfully.", "positive")

                    coords = self.create_x_y_list(self.co_ordinates) #returns x at index 0, y at 1
                    label = label + "line"
                    v = self.axis.plot(coords[0], coords[1], color=colour, marker="o", label=label, linewidth=self.line_thickness)
                    self.draw_figure()
                    self.num_of_lines +=1
                else:
                    print("there is an intersection")
                    self.update_information("Intersection Found.", "warning")
        else:
            print("MRI Slice not clicked.")
            self.update_information("MRI Slice not clicked.", "warning")

    #Function to clear all axis data & draw this to the figure
    def clear_axis_data(self):
        self.axis.lines.clear()
        self.axis.collections.clear()
        self.draw_figure()

    #Function to remove any highlighted points from the figure
    def remove_highlighted_points(self):
        for item in self.highlighted_points:
            if item in self.axis.collections:
                self.axis.collections.remove(item)
        self.highlighted_points.clear()
        self.draw_figure()

    #Select a Polygon
    def select_polygon(self, event):
        #clear any outstanding incomplete drawing objs from axis if select btn clicked
        self.reset_polygon_cols()
        self.remove_highlighted_points()

        #Select Polygon
        polygon_selected = False
        if not(event.xdata == None and event.ydata == None): #in case the user clicks the white border area
            for d in self.polygon_info:
                for x, y in d['co-ordinates']:
                    print(x, y)
                    print("prec", self.precision, type(self.precision))
                    if (np.abs(x - event.xdata) < self.precision) and (np.abs(y - event.ydata) < self.precision): #np.abs allows the number to be positive only
                        polygon_selected = True
                        self.selected_polygon = d
                        self.get_selected_polygon()
                        self.update_information("Polygon {} selected. Click off polygon to deselect.".format(d['id']), "positive")

                        #Convert colours of selected polygon
                        self.show_selected_plots(self.selected_polygon['scatter_points'], self.axis.collections, self.select_col)
                        self.show_selected_plots(self.selected_polygon['lines'], self.axis.lines, self.select_col)
                        self.draw_figure()

        #if click elsehwere then deselect all polygons
        if not polygon_selected:
            self.update_information("No polygon selected, make sure you click a vertex!", "warning")
            self.selected_polygon = None
            self.get_selected_polygon()
            self.reset_polygon_cols() #resets the colours back to their original colours

        self.check_polygon_selected() #this amends the button states depending on button selection

    #Function changes the state of the buttons depending on whether there is a polygon selected or not
    def check_polygon_selected(self):
        #if a polygon is selected or not selected buttons change states accordingly
        if self.selected_polygon != None:
            for button in self.polygon_buttons:
                if button['description'] == "delete":
                    button['widget']['state'] = "normal"
                    button['widget']['command'] = lambda polygon=self.selected_polygon: self.del_btn_click(polygon)
                elif button['description'] == "edit":
                    button['widget']['state'] = "normal"
                    button['widget']['command'] = lambda polygon=self.selected_polygon: self.edit_btn_click(polygon)
                elif button['description'] == "edit_tag":
                    button['widget']['state'] = "normal"
                    button['widget']['command'] = lambda polygon=self.selected_polygon: self.edit_tag(polygon)
        else:
            buttons = ['delete', 'edit', 'edit_tag']
            for button in self.polygon_buttons:
                if button['description'] in buttons:
                    button['widget']['state'] = button['dlft_state']
                    button['widget']['command'] = None

    #For when the select btn is clicked, if select btn is clicked then when click graph select polygon is func called
    def select_btn_click(self):
        self.fc.disconnect()
        self.fc.connect(lambda event: self.select_polygon(event))

    #For when the edit button is clicked
    def edit_btn_click(self, polygon):
        if self.selected_polygon != None: #if polygon is selected then when click on graph, select_vertex func is called
            self.fc.disconnect()
            self.fc.connect(lambda event: self.select_vertex(event, polygon))
        else:
            print("No polygon selected")

    #Function for the user to select a vertex when they click on the graph
    def select_vertex(self, event, polygon):
        #select vertex to be edited
        if not(event.xdata == None and event.ydata == None): #in case the user clicks the white border area
            for x, y in polygon['co-ordinates']:
                #find vertex that is selected
                if (np.abs(x - event.xdata) < self.precision) and (np.abs(y - event.ydata) < self.precision): #np.abs allows the number to be positive only
                    #particular vertex within the polygon
                    index = polygon['co-ordinates'].index([x, y])
                    vertex_selected = {"x": x, "y": y, "index": index}
                    #re-establish this
                    self.selected_polygon = polygon
                    self.check_polygon_selected()

                    #create highlighted pt
                    coord = [x, y]
                    highlighted_point = self.create_highlighted_pt(self.axis, self.highlighted_points, coord)

                    #update information
                    self.update_information("Vertex selected. Click the selection button again!", "positive")

                    #Next time graph is clicked position vertex is called to place a plot
                    self.fc.disconnect()
                    self.fc.connect(lambda event: self.position_vertex(event, polygon, vertex_selected, highlighted_point))

    #Function for the user to place down a plot when they next click the graph
    def position_vertex(self, event, polygon, vertex_selected, highlighted_point):
        self.remove_highlighted_points()
        selected_another_polygon_vertex = False
        self.selected_polygon = polygon
        self.check_polygon_selected()

        #In case the user clicks a vertex that is part of another polygon
        for other_poly in self.polygon_info:
            if other_poly != polygon:
                for x, y in other_poly['co-ordinates']:
                    if (np.abs(x - event.xdata) < self.precision) and (np.abs(y - event.ydata) < self.precision):
                        selected_another_polygon_vertex = True

                        self.update_information("Another polygon vertex found. Plot not possible.", "warning") #update the information to alert the user

                        #Following is to keep the highlighted point on the original selected vertex
                        for poly in self.polygon_info:
                            if poly['id'] == polygon['id']:
                                current_cord = poly['co-ordinates'][vertex_selected['index']]
                        highlighted_point = self.create_highlighted_pt(self.axis, self.highlighted_points, current_cord)

        #If the plot is not part of another polygon but is another vertex of the same polygon
        if not selected_another_polygon_vertex:
            selected_another_vertex = False
            if not(event.xdata == None and event.ydata == None):
                for x, y in polygon['co-ordinates']:
                    if (np.abs(x - event.xdata) < self.precision) and (np.abs(y - event.ydata) < self.precision): #np.abs allows the number to be positive only
                        #if it goes into here then the user has selected another co-ordinate of the polygon
                        selected_another_vertex = True
                        index = polygon['co-ordinates'].index([x, y])
                        #plot the highlighted point
                        coord = [x, y]
                        highlighted_point = self.create_highlighted_pt(self.axis, self.highlighted_points, coord)

                        #need to re-establish selected vertex as a different vertex is clicked
                        vertex_selected = {"x": x, "y": y, "index": index}

                        self.update_information("Vertex selected switched!", "positive") #update the info as clicked another vertex of polygon

                        #Next time the user clicks the graph then position vertex is called again recursivly
                        self.fc.disconnect()
                        self.fc.connect(lambda event, polygon=polygon, vertex_selected=vertex_selected, highlighted_point=highlighted_point: self.position_vertex(event, polygon, vertex_selected, highlighted_point))
                        break #to ensure the loop only runs once (if points are close together)

            #if another vertex has not been selected then continue with looking for intersections
            if not selected_another_vertex:
                new_coord = [event.xdata, event.ydata]

                #change lines & scatter points & co-ordinates in dict
                id = polygon['id']
                xlist, ylist = [], []
                index = vertex_selected['index']

                #check that new position is not creating an intersection
                proposed_lines = []
                #line 1 would be the line with preceeding co-ordinate and current co-ordinate
                line_1 = [polygon['co-ordinates'][index - 1], [event.xdata, event.ydata]]
                proposed_lines.append(line_1)
                #line 2 would be the line with current co-ordinate and succeeding co-ordinate
                if (index + 1) == len(polygon['co-ordinates']):
                    line_2 = [[event.xdata, event.ydata], polygon['co-ordinates'][0]]
                    proposed_lines.append(line_2)
                else:
                    line_2 = [[event.xdata, event.ydata], polygon['co-ordinates'][index + 1]]
                    proposed_lines.append(line_2)

                    #Find an intersection
                for line in proposed_lines:
                    intersection = PolygonIntersector(self.polygon_info, polygon)
                    intersector = intersection.find_intersection(line)

                    #If doesn't intersect
                if not intersector:
                    #Remove the current polygon from the graph
                    print(self.axis)
                    self.remove_plot(polygon['lines'], self.axis.lines)
                    self.remove_plot(polygon['scatter_points'], self.axis.collections)
                    # self.remove_polygon_obj(polygon, self.axis)

                    #swap old co-ordinate with new co-ordinate & replot scatter points
                    for poly in self.polygon_info:
                        if poly['id'] == id:
                            poly['co-ordinates'][index] = new_coord #change co_ordinates

                            data = self.file_writer.read_file()
                            for item in data:
                                if item['id'] == poly['id']:
                                    item['co-ordinates'] = poly['co-ordinates']
                            self.file_writer.create_json_file(data)

                            for x, y in poly['co-ordinates']:
                                xlist.append(x)
                                ylist.append(y)

                    num_of_vertexes = len(xlist)
                    #append first co-ordinate again so line joins up on plot
                    x, y = xlist[0], ylist[0]
                    xlist.append(x)
                    ylist.append(y)

                    #draw lines
                    label = str(id) + " edited final polygon"
                    v = self.axis.plot(xlist, ylist, color=self.select_col, marker="o", label=label, linewidth=self.line_thickness) #plot the new lines for new polygon

                    #change matplotlib objects for scatter points & lines in polygon info to recently made ones
                    for poly in self.polygon_info:
                        if poly['id'] == id:
                            poly['scatter_points'] = self.axis.collections[-num_of_vertexes:]
                            poly['lines'] = self.axis.lines[-1:] #as i only add the final polygon line

                    #draw the highlighted pt
                    highlighted_point = self.create_highlighted_pt(self.axis, self.highlighted_points, new_coord)

                    self.show_selected_plots(polygon['scatter_points'], self.axis.collections, self.select_col)
                    self.show_selected_plots(polygon['lines'], self.axis.lines, self.select_col)

                    self.update_information("Edited Plot placed!", "positive")

                    self.draw_figure()
                    #https://sourceforge.net/p/matplotlib/mailman/message/9334388/
                    #https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.html
                else:
                    #this would keep the yellow highlighted point on the existing point when the user tries to click across an intersection
                    highlighted_point = self.create_highlighted_pt(self.axis, self.highlighted_points, polygon['co-ordinates'][index])

                    self.show_selected_plots(polygon['scatter_points'], self.axis.collections, self.select_col)
                    self.show_selected_plots(polygon['lines'], self.axis.lines, self.select_col)

                    self.update_information("Intersection found. Plot not possible.", "warning")

                    self.draw_figure()

    def create_highlighted_pt(self, axis, pts_list, coord):
        #create a highlighted point to show vertex that is selected
        color = [item['current_value'] for item in self.settings if item['setting'] == "Selected Vertex Colour"][0]
        size =  int([item['current_value'] for item in self.settings if item['setting'] == "Selected Vertex Size"][0])
        highlighted_point = axis.scatter(coord[0], coord[1], s=size, color=color) #forms a highlighted ring
        pts_list.append(highlighted_point)
        self.draw_figure()
        return highlighted_point

    #Function to save the change of tag
    def edit_tag(self, polygon):
        #Result is sent back from PolygonTagChanger depending on user input
        # result = PolygonTagChanger(polygon, self.tags).send()
        result = PolygonTagChanger(polygon, self.tags).send()
        print("RESULT", result)
        #if result is different to current tag then confirm btn would have had to be clicked
        if result != polygon['tag']:

            #Update the Polygon Info
            for item in self.polygon_info:
                if item['id'] == polygon['id']:
                    item['tag'] = result

            #Update json file
            try:
                data = self.file_writer.read_file()
                updated_data = self.file_writer.update_file(data, polygon['id'],'tag', result)
                self.file_writer.create_json_file(updated_data)

            except FileNotFoundError:
                message = "JSON file could not be found."
                error = messagebox.showerror(title="File Not Found", message="JSON file could not be found.")
                print("JSON file could not be found.")


    def show_selected_plots(self, polygon_objs, axis_objs, select_col):
        #https://matplotlib.org/3.2.1/api/collections_api.html #setting the colour
        for plot in axis_objs:
            if plot in polygon_objs:
                # print(plot.get_color())
                plot.set_color(select_col) #select to selected_colour

    def del_btn_click(self, polygon):
        self.remove_highlighted_points()

        result = messagebox.askquestion("Delete Polygon", "Are you sure you want to delete Polygon {}?".format(str(polygon['id']), icon='information'))
        #https://stackoverflow.com/questions/11244753/tkinter-askquestion-dialog-box
        if result == "yes":
            try:
                #remove plots
                # self.remove_polygon_obj(polygon, self.axis)

                self.remove_plot(polygon['lines'], self.axis.lines)
                self.remove_plot(polygon['scatter_points'], self.axis.collections)

                self.draw_figure()
                #remove from dict
                id = polygon['id']
                self.polygon_info = [item for item in self.polygon_info if item['id'] != id]
                #https://stackoverflow.com/questions/33190779/how-to-delete-a-dictionary-from-a-list-of-dictionaries

                #text to tell user was successfully deleted
                self.update_information("Polygon with Id: {} successfully deleted.".format(str(id)), "positive") #information line

                #remove from json
                info = []
                for polygon in self.polygon_info:
                    dict = {"id": polygon['id'], 'tag': polygon['tag'], 'slice': polygon['slice'], 'co-ordinates': polygon['co-ordinates'] }
                    info.append(dict)

                self.file_writer.create_json_file(info)
                self.load_polygons() #re-load polygons & subsquent butn state functions
                self.get_selected_polygon()

            except:
                print("There was an issue deleting the polygon.")
                self.update_information("There was an issue deleting the polygon. Please try again.", "warning")

            self.load_polygons() #re-load polygons & subsquent butn state functions
            self.get_selected_polygon()

    def remove_plot(self, polygon_objs, axis_objs):
        #function to remove a polygon
        for plot in polygon_objs:
            for object in axis_objs:
                if plot == object:
                    axis_objs.remove(plot)

    def remove_polygon_obj(self, polygon, axis_objs):
        self.remove_plot(polygon['lines'], axis.lines)
        self.remove_plot(polygon['scatter_points'], axis.collections)

#Class for the Notebox upon the Slice Figure
class Notebox(SliceFigure):
    def __init__(self, parent_frame, username, slice_name, figure_information, folder_selected, slice_list):
        self.parent_frame = parent_frame #parent frame for notebox (Notebox contains the tab panes & instantiates the notetables & add note)
        self.username = username #passes through the username for the username for the session
        self.slice_name = slice_name #current slice name of the slice that is visible
        self.figure_information = figure_information #DISPENSIBLE = used for passing split up pieces of folder selected
        self.folder_selected = folder_selected #folder selected address used - this is used to look for & create json file objs in appropiate locations
        self.slice_list = slice_list #DISPENSIBLE = used for creating the file for individual slice notes

        self.selected_polygon = None #when a selected polygon is selected, this is passed up

        self.note_tabs = [] #stores the tabs as dicts
        self.note_types = [ {"name": "Scan Type", "radio_name": "Scan Type", "table_col_settings":[{"column": "polygon id", "wraplength":10, "side": "left", "width": 10, "fill": False, "btns": None},
                                                                                                    {"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False, "btns": None},
                                                                                                    {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
                                                                                                    {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
                                                                                                    {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": None}
                                                                                                    ]},
                            {"name": "Slice", "radio_name": "Current Slice", "table_col_settings":[{"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False, "btns": None},
                                                                                                    {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
                                                                                                    {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
                                                                                                    {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": None}
                                                                                                    ]},
                            {"name": "Polygon", "radio_name": "Selected Polygon", "table_col_settings":[{"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False},
                                                                                                    {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False},
                                                                                                    {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False},
                                                                                                    {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False}
                                                                                                    ]}]
        #for later on: select btn will maybe select the polygon on the slice etc
        # self.note_types = [{"name": "Polygon", "radio_name": "Selected Polygon", "table_col_settings":[{"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False, "btns": None},
        #                                                                                                 {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
        #                                                                                                 {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
        #                                                                                                 {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": None},
        #                                                                                                 {"column": "adjust", "wraplength":None, "side": "left", "width": 14, "fill": False, "btns": [{"name": "remove", "text": "Remove", "function": None, "width": 7},
        #                                                                                                                                                                                             {"name": "edit", "text": "Edit", "function": None, "width": 7}
        #                                                                                                                                                                                             ]},
        #                                                                                                 ]},
        #                     {"name": "Slice", "radio_name": "Current Slice", "table_col_settings":[{"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False, "btns": None},
        #                                                                                                 {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
        #                                                                                                 {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
        #                                                                                                 {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": None},
        #                                                                                                 {"column": "adjust", "wraplength":None, "side": "left", "width": 14, "fill": False, "btns": [{"name": "remove", "text": "Remove", "function": None, "width": 7},
        #                                                                                                                                                                                             {"name": "edit", "text": "Edit", "function": None, "width": 7}
        #                                                                                                                                                                                             ]},
        #                                                                                                 ]},
        #                     {"name": "Scan Type", "radio_name": "Scan Type", "table_col_settings":[{"column": "polygon id", "wraplength":10, "side": "left", "width": 10, "fill": False, "btns": None},
        #                                                                                             {"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False, "btns": None}
        #                                                                                             {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
        #                                                                                             {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
        #                                                                                             {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": None},
        #                                                                                             {"column": "view", "wraplength":30, "side": "left", "width": 10, "fill": False, "btns": [{"name": "select", "text": "Select", "function": None, "width": 7}
        #                                                                                                                                                                                         ]},
        #                                                                                             {"column": "adjust", "wraplength":None, "side": "left", "width": 14, "fill": False, "btns": [{"name": "remove", "text": "Remove", "function": None, "width": 7},
        #                                                                                                                                                                                         {"name": "edit", "text": "Edit", "function": None, "width": 7}
        #                                                                                                                                                                                         ]},
        #                                                                                             ]}
        #
                         # ]
        #create notebook
        self.note_tab_pane = ttk.Notebook(self.parent_frame)
        self.note_tab_pane.pack(side="bottom", fill="x")

        #create tabs
        for item in self.note_types:
            new_tab = Tab(self.note_tab_pane, HEADER_BG) #create tab pane
            inner_tab_frame = new_tab.add_tab(item['name'] + " Notes")
            self.show_note(inner_tab_frame, item['radio_name'])
            self.note_tabs.append({"tab":item['radio_name'], "frame":inner_tab_frame})
            item['tab_frame'] = inner_tab_frame

        #create add note tab
        self.new_tab_add = Tab(self.note_tab_pane, HEADER_BG) #create a new tab instance
        self.notes_frame = self.new_tab_add.add_tab("Add Note")
        self.note_tab_pane.select(self.notes_frame) #override the function of selecting the last added tab to select a specfic one i.e the add note tab

        #Contents of Add Note tab
        #create radio buttons **REDO**
        self.radio_frame = tk.Frame(self.notes_frame, background=HEADER_BG)
        self.radio_frame.pack(side="top", fill="x")
        self.note_type = tk.StringVar()
        self.radiobuttons = []
        padding_x = (10, 0) #padding just for the first item

        for item in self.note_types:
            radio = ttk.Radiobutton(self.radio_frame, text=item['radio_name'], value=item['radio_name'], variable=self.note_type, command=self.activiateTextBox)
            radio.pack(side = "left", pady=10, padx=padding_x)
            self.radiobuttons.append({"name": item['radio_name'], "widget": radio})
            padding_x = (50, 0) #change the padding going forwards

        self.disable_selected_polygon_radio() #disable the selected polygon button if no polygon selected

        #create Notebox textbox for adding a new note
        self.notebox_frame = tk.Frame(self.notes_frame, bg=HEADER_BG)
        self.notebox_frame.pack(fill="x", expand=True)
        self.initial_text = "Select Option"
        self.notebox = TextBox(self.notes_frame, 3, 10, self.initial_text)
        self.notebox.change_notebox_padding(10, 0) #I remove the y padding here but keep it dynamic
        self.notebox_activated_text = "Add a note..." #text for when the notebox is activiated
        self.notebox.disable_notebox()
        self.contents = self.notebox.read_contents()[:-1]
        #** I CANNOT SEEM TO MAKE THIS DYNANMIC YET**
        self.notebox.notebox.bind("<Button-1>", lambda e: self.watch_for_txtbx_click(self.notebox.read_contents()[:-1]))

        #Create Notebox buttons using ButtonCreator class
        self.notebox_btns_frm = tk.Frame(self.notes_frame, background=HEADER_BG)
        self.notebox_btns_frm.pack(side="bottom", fill="x", expand=True)
        self.notebox_btn_dict = [{"name": "clear", "command":lambda: self.notebox.clear_notebox(), "default_state": "normal", "side": "left", "width":10},
                                {"name": "add", "command":lambda: self.add_note(), "default_state": "disabled", "side": "right", "width":10}]
        self.notebox_btns = ButtonCreator(self.notebox_btns_frm, self.notebox_btn_dict)

    #If no polygon is selected then disable radio button **MAKE DYNAMIC**
    def disable_selected_polygon_radio(self):
        if self.selected_polygon == None:
            self.note_type.set(None) #deselects the radiobutton if value outside of values possible  #https://stackoverflow.com/questions/43403653/how-to-deselect-a-radio-button-tkinter
            for radiobtn in self.radiobuttons:
                if radiobtn['name'] == "Selected Polygon":
                    radiobtn['widget']['state'] = 'disabled'
                    radiobtn['widget']['text'] = "Selected Polygon"

    #When the current slice is changed, the current slice in this class is updated.
    def update_slice_name(self, new_slice_name):
        self.slice_name = new_slice_name #updates the slice name
        self.selected_polygon = None #alters selected polygon to None as if slice is changed then there is no polygon selected
        self.disable_selected_polygon_radio() #disable the polygon radio button

        #show notes according to slice visible
        for item in self.note_tabs:
            self.show_note(item['frame'], item['tab'])

    #This method is called when polygon is selected from Polygons class (child of Slice Figure Parent)
    def set_selected_polygon(self, polygon):
        self.selected_polygon = polygon
        if self.selected_polygon != None:
            for radiobtn in self.radiobuttons:
                if radiobtn['name'] == "Selected Polygon":
                    radiobtn['widget']['state'] = 'normal'
                    radiobtn['widget']['text'] = "Polygon ID: " + str(self.selected_polygon['id'])
        else:
            self.disable_selected_polygon_radio()

    #Method for adding a note **CLEAN UP**
    def add_note(self):
        #Values: #note, username, year, scan_type if Slice, slice_name / patient, date, time #need to make below dynamic
        values_ready = []
        values = []
        note = self.notebox.read_contents()[:-1]
        if self.note_type.get() == 'Scan Type':
            values = [note, self.username, self.figure_information['year'], self.figure_information['patient'], self.format_date_time()[0], self.format_date_time()[1]]
        elif self.note_type.get() == 'Current Slice':
            values = [note, self.username, self.figure_information['year'], self.figure_information['patient'], self.figure_information['scan type'], self.slice_name[:-1], self.format_date_time()[0], self.format_date_time()[1]]
        elif self.note_type.get() == 'Selected Polygon':
            values = {"note": note, "user": self.username, "date": self.format_date_time()[0], "time": self.format_date_time()[1]}
            # values = [self.notebox.get(1.0, tk.END)[:-1], self.username, self.format_date_time()[0], self.format_date_time()[1]]

        for value in values:
            stringed_value = """ '""" + value + """' """
            values_ready.append(stringed_value)

        if self.note_type.get() == 'Selected Polygon':
            try:
                #call filewriter - there would have to be a polygon to be able to write a polygon note
                filename = self.folder_selected + "/" + self.slice_name + '_polygon_data.json'
                print(filename)
                json_file = jsonFileWriter(filename, None, None)
                data = json_file.read_file() #read file
                for polygon in data:
                    if polygon['id'] == self.selected_polygon['id']: #if id the same of the polygon records
                        try: #if there are or if there are not notes present for the polygon
                            polygon['notes'].append(values) #append the note with the structure defined above
                        except KeyError:
                            polygon['notes'] = [] #need to establish notes first if no notes present
                            polygon['notes'].append(values)
                json_file.create_json_file(data) #write to the json file

            except FileNotFoundError:
                print("Not not added as Json file not found.")
            except:
                print("Note not added correctly.")

        #database
        if MAKE_DB:
            for item in TABLES: #making it dynanmic, so can have multiple buttons above
                if self.note_type.get() == item['value']:
                    database_instance = Database(DB_NAME)
                    database_instance.add_record(item['table_name'], values_ready, item['columns'])

        #json file
        if MAKE_JSON:
            data = {"year": self.figure_information['year'], "patient": self.figure_information['patient'], "scan_type": self.figure_information['scan type'], "slices": []}
            for slice in self.slice_list:
                slice_name = {"name": slice}
                data['slices'].append(slice_name)

            note_details = [self.username, note, self.format_date_time()[0], self.format_date_time()[1]]
            filename = self.figure_information['year'] + "-" +  self.figure_information['patient'] + "-" + self.figure_information['scan type'] + '.json'
            dir = self.folder_selected + '/scan and slice notes' + '.json'

            json_file = jsonFileWriter(dir, data, self.slice_name)
            json_file.append_note(note_details, self.note_type.get())

        #only refresh notes for table that note has been added for
        self.refresh_tab(self.note_type.get())
        #Reset the tab now a note has been added
        self.reset_add_note_tab()

    #Method for showing the table **CLEAN UP**
    def show_note(self, frame, note_type):
        if MAKE_JSON:
            print("FIGINFO", self.figure_information)
            data = {"year": self.figure_information['year'], "patient": self.figure_information['patient'], "scan_type": self.figure_information['scan type'], "slices": []}
            dir = self.folder_selected + '/scan and slice notes' + '.json'
            json_file = jsonFileWriter(dir, data, self.slice_name[:-1])
            notes = json_file.read_file()
            col_settings = [{"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False},
                            {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False},
                            {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False},
                            {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False},
                            ]

            if (note_type == "Scan Type"):
                data = notes['scan_type_notes']

            elif( note_type == "Current Slice"):
                dir = self.folder_selected + '/scan and slice notes' + '.json'
                json_file = jsonFileWriter(dir, data, self.slice_name[:-1])
                notes = json_file.read_file()
                data = []
                for item in notes['slices']:
                    if item['name'] == (self.slice_name + '.npy'): #**GET RID OF NEED FOR .npy**
                        for note in item['notes']:
                            formatted_note = {}
                            formatted_note['user'] = note['user']
                            formatted_note['note'] = note['note']
                            formatted_note['date'] = note['date']
                            formatted_note['time'] = note['time']
                            data.append(formatted_note)

            elif( note_type == "Selected Polygon"):
                filename = self.folder_selected + "/" + self.slice_name + '_polygon_data.json'
                json_file = jsonFileWriter(filename, None, None)
                unformatted_data = json_file.read_file() #read file
                #pull data from file - need to sort
                data = []
                for polygon in unformatted_data:
                    try:
                        for note in polygon['notes']:
                            formatted_polygon = {}
                            formatted_polygon['polygon id'] = polygon['id']
                            formatted_polygon['note'] = note['note']
                            formatted_polygon['user'] = note['user']
                            formatted_polygon['date'] = note['date']
                            formatted_polygon['time'] = note['time']
                            data.append(formatted_polygon)
                    except KeyError:
                        pass

                col_settings = [{"column": "polygon id", "wraplength":30, "side": "left", "width": 10, "fill": False},
                                {"column": "user", "wraplength":100, "side": "left", "width": 15, "fill": False},
                                {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False},
                                {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False},
                                {"column": "time", "wraplength":30, "side": "left", "width": 10, "fill": False}
                                ]
            if len(data) > 0:
                row_btns = [{"name": "remove", "text": "Remove", "function": lambda  args, notetype = note_type: self.remove_note(args, notetype), "width": 7},
                            {"name": "edit", "text": "Edit", "function": lambda args, notetype = note_type: self.edit_note(args, notetype), "width": 7}
                            ]
                table = NoteTable(frame, col_settings, data, 665, 150, row_btns, HEADER_BG)

            else:
                #no data is present so forget children if there are any (eg. if there was a table child on a previous slice). Does not error if not children
                for child in frame.winfo_children():
                    child.pack_forget() #https://stackoverflow.
        # database_instance = Database(DB_NAME)
        # row = 14
        # col = 7
        # for item in TABLES:
        #     records = database_instance.show_records(item['table_name'])
        #     notes_frame = tk.LabelFrame(self.parent_frame, text=" Slice Notes: ", padx=10, pady=10, height=200)
        #     notes_frame.grid(row=row, column=col, columnspan=5, sticky="NSEW")
        #     notes_frame_lab = tk.Label(notes_frame, text="Text here").grid(row=0, column=0, sticky="W")
        #     row += 1
        #     col += 1

        #pull notes from the json

    #Method for refreshing the table in a tab
    def refresh_tab(self, tab):
        print("ENTERED REFRESH TAB")
        for item in self.note_tabs:
            if item['tab'] == tab:
                self.show_note(item['frame'], item['tab'])

    #Method for resetting the add Note tab after a note is added
    def reset_add_note_tab(self):
        self.note_type.set("None") #set the radio buttons to a value that is not present
        self.notebox.replace_text(self.initial_text) #replace with initial text
        self.notebox.disable_notebox() #disable the notebox
        self.notebox_btns.disable_all_btns() #changes Add to disable & clear to normal

    #Method called for when a note is to be edited
    def edit_note(self, args, notetype):
        #loads edit window & recieves result for the new note
        current_note = args[1]
        edit_note = EditNote(current_note, notetype, self.folder_selected, self.slice_name).send()
        #if confirm button is clicked then note is returned, if cancel clicked None returned
        if edit_note != None:
            print("EDITED NOTE", edit_note)
            #add note to json
            if len(edit_note) > 0: #if == 0 then there is no note
                if current_note != edit_note:
                    #content is different, edit note in json
                    if notetype == "Scan Type":
                        try:
                            dir = self.folder_selected + '/scan and slice notes' + '.json'
                            json_file = jsonFileWriter(dir, None, None)
                            data = json_file.read_file()

                            for item in data['scan_type_notes']:
                                if item['note'] == current_note:
                                    item['user'] = item['user'] + " (ed)"
                                    item['note'] = edit_note

                            json_file.create_json_file(data)

                        except FileNotFoundError:
                            print("File not found. Note not removed")
                        except:
                            print("Note not removed.")

                    elif notetype == "Current Slice":
                        try:
                            dir = self.folder_selected + '/scan and slice notes' + '.json'
                            json_file = jsonFileWriter(dir, None, None)
                            data = json_file.read_file()

                            for item in data['slices']:
                                if item['name'] == self.slice_name + ".npy":
                                    for note in item['notes']:
                                        if note['note'] == current_note:
                                            note['user'] = note['user'] + " (ed)"
                                            note['note'] = edit_note

                            json_file.create_json_file(data)

                        except FileNotFoundError:
                            print("File not found. Note not removed")
                        except:
                            print("Note not removed.")

                    elif notetype == "Selected Polygon":
                        try:
                            polygon_id = args[0]
                            args[0] == "id"
                            pass
                            dir = self.folder_selected + "/" + self.slice_name + '_polygon_data.json'
                            json_file = jsonFileWriter(dir, None, None)
                            data = json_file.read_file()

                            for polygon in data:
                                if polygon['id'] == polygon_id:
                                    for note in polygon['notes']:
                                        if note['note'] == current_note:
                                            note['user'] = note['user'] + " (ed)"
                                            note['note'] = edit_note

                            json_file.create_json_file(data)

                        except FileNotFoundError:
                            print("File not found. Note not removed")
                        except:
                            print("Note not removed.")

                    self.refresh_tab(notetype) #only refresh if note has actually changed

    #Method called for when a note is to be removed
    def remove_note(self, args, notetype):
        print(args)
        note = args[1]
        if notetype == "Scan Type":
            try:
                dir = self.folder_selected + '/scan and slice notes' + '.json'
                json_file = jsonFileWriter(dir, None, None)
                data = json_file.read_file()

                data['scan_type_notes'] = [item for item in data['scan_type_notes'] if item['note'] != note]
                json_file.create_json_file(data)

            except FileNotFoundError:
                print("File not found. Note not removed")
            except:
                print("Note not removed.")

        elif notetype == "Current Slice":
            try:
                dir = self.folder_selected + '/scan and slice notes' + '.json'
                json_file = jsonFileWriter(dir, None, None)
                data = json_file.read_file()

                for scan in data['slices']:
                    if scan['name'] == self.slice_name + ".npy":
                        scan['notes'] =  [item for item in scan['notes'] if item['note'] != note]

                json_file.create_json_file(data)

            except FileNotFoundError:
                print("File not found. Note not removed")
            except:
                print("Note not removed.")

        elif notetype == "Selected Polygon":
            try:
                polygon_id = args[0]
                args[0] == "id"
                pass
                dir = self.folder_selected + "/" + self.slice_name + '_polygon_data.json'
                json_file = jsonFileWriter(dir, None, None)
                data = json_file.read_file()

                for polygon in data:
                    if polygon['id'] == polygon_id:
                        polygon['notes'] =  [item for item in polygon['notes'] if item['note'] != note]

            except FileNotFoundError:
                print("File not found. Note not removed")
            except:
                print("Note not removed.")

        self.refresh_tab(notetype)

    #When a radio button is clicked, the textbox is activated.
    def activiateTextBox(self):
        self.notebox.enable_notebox()
        self.notebox.replace_text(self.notebox_activated_text)
        self.notebox_btns.change_to_default_states()

    #Watches out for a click in the textbox. Placeholder text is removed if found
    def watch_for_txtbx_click(self, notebox_test):
        if (notebox_test == self.notebox_activated_text): #if the present text in the textbox is equal to the insert then remove all text
            self.notebox.clear_notebox() #clear the notebox, can also use .delete("insert linestart", "insert lineend")
            self.notebox_btns.enable_all_btns() #enable Clear & Add btns

    #Formats Date & Time
    def format_date_time(self):
        date_time_stamp = start_time()
        date = re.split(" ", date_time_stamp)[0]
        time = re.split(" ", date_time_stamp)[1]
        return date, time

#OTHER WINDOWS
#Class that controls the construction & receiving of the Editing Note Window
class EditNote:
    def __init__(self, note, note_type, folder_selected, slice_name):
        self.note = note #the contents of the note
        self.note_type = note_type #whether note is slice, polygon, scan_type etc
        self.folder_selected = folder_selected
        self.slice_name = slice_name

        #Create the toplevel window
        self.window = TopLevelWin("Edit Note", MAIN_BG, self)
        self.window.create_header(HEADER_BG, MEDIUM_FONT, FONT_COL, "Edit Note")
        self.win_main_frame = self.window.create_main(MAIN_BG)

        #all contents includded in a label frame
        self.label_frame = tk.LabelFrame(self.win_main_frame, text=" Edit Note: ", bg=MAIN_BG, fg=FONT_COL)
        self.label_frame.pack(padx=10, pady=10)
        #Create the textbox
        self.notebox_frame = tk.Frame(self.label_frame, bg=MAIN_BG)
        self.notebox_frame.grid(row=1, column=0, sticky="NSEW")
        self.notebox = TextBox(self.notebox_frame, 5, 40, self.note)

        #create a Clear & Reset btn
        self.button_dict = [{"name": "clear", "command": self.clear_txtbox, "side":"left", "default_state": "normal", "width":10},
                        {"name": "reset", "command": self.reset_txtbox,"side":"left", "default_state": "normal", "width":10}]

        self.buttons_frame = tk.Frame(self.label_frame, bg=MAIN_BG)
        self.buttons_frame.grid(row=2, column=0, sticky="W")
        self.buttons = ButtonCreator(self.buttons_frame, self.button_dict)

        #add the cancel & confirm button
        self.window.add_controls()
        self.new_note = None

    #Function for resetting the textbox - Used by the reset button
    def reset_txtbox(self):
        self.notebox.replace_text(self.note)

    #Function for clearing the textbox - Used by the clear button
    def clear_txtbox(self):
        self.notebox.clear_notebox()

    #Function that sends result to parent window
    def send(self):
        self.window.wait()  #waits for the window to be exited now to do anything further
        return self.new_note

    #this method needs to be called 'confirm selection'
    def confirm_selection(self):
        self.new_note = self.notebox.read_contents()[:-1] #get rid of \n at end, assign self.new_note for ready to send

        if len(self.new_note) > 0: #if == 0 then there is no note
            self.window.close_window() #close_window
        else:
            self.warning = tk.Label(self.label_frame, text="Please enter a note.", fg="red", bg=MAIN_BG)
            self.warning.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    #A cancel selection method required by base class if anything required upon cancellation
    def cancel_selection(self):
        self.window.close_window() #close_window

class jsonFileWriterPolygon:
    def __init__(self, filename, slice_name):
        self.filename = filename
        print(self.filename)
        self.slice_name = slice_name
        print(self.slice_name)
        self.data = []
        # self.headers = ["slice", "id", "tag", "co-ordinates"]
        # self.data = {"id": None, "slice": None, "tag": None, "co-ordinates": None}

        needcreate = not os.path.exists(self.filename)
        if needcreate:
            print("Need create")
            self.create_json_file(self.data) #create the file if one doesn't already exist

    def create_json_file(self, data):
        with open(self.filename,'w') as f:
            json.dump(data, f, indent=4)

    def add_polygon(self, dict):
        data = self.read_file()
        data.append(dict)
        self.create_json_file(data)

    def read_file(self):
        with open(self.filename) as f:
            currentdata = json.load(f)
        return currentdata

    def sort_file(self, data, sort_key, sort_val):
        sorted_data = []
        for item in data:
            if item[sort_key] == sort_val:
                sorted_data.append(item)

        # data = [item for item in data if data[sort_key] == sort_val]
        return sorted_data

    def update_file(self, data, polygon_id, key, new_value):
        for item in data:
            if item['id'] == polygon_id:
                item[key] = new_value
        return data

app = MainApp()
# app.geometry("1280x780") #x by y
app.mainloop()
