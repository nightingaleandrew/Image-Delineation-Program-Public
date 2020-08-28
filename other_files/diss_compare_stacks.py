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
#image imports
from PIL import ImageTk, Image
from PIL import Image as PIL_image, ImageTk as PIL_imagetk

#classes
from toggle_frame import ToggledFrame
from TopLevelWin import TopLevelWin
from widget_creator_classes import TextBox, InformationBox, ButtonCreator, Tab, ToolTip, NoteTable, ColourSquare
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
# EXAMPLE_NPARRAY = r'C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\t2-axial\PR150_01_0006_002_t2-axial.npy'
DIRECTORY = r"C:/Users/Andrew/Documents/dissertation/data/proc" #directory here
#images

# PLAY_ICON = r"./images/pause_play_2.jpg" #https://simpleicon.com/play-2.html
# DRAW_ICON = r"./images/polyjpg.png" #https://www.kindpng.com/imgv/iiRwTmh_line-symbol-polygon-draw-polygon-icon-png-transparent/ says free download
# SELECT_ICON = r"./images/select_icon_3.png"
# DELETE_ICON = r"./images/delete_2.png"
# START_ICON = r"./images/start_icon.png" #http://www.myiconfinder.com/icon/next-pause-previous-rewind-forward-stop-play-back-eject-controls-music-button/4923
# END_ICON = r"./images/end_icon.png" #http://www.myiconfinder.com/icon/next-pause-previous-rewind-forward-stop-play-back-eject-controls-music-button/4923
# SHOW_ICON = r"./images/show.png" #https://thenounproject.com/term/show/
# REFRESH_ICON = r"./images/refresh.png" #https://www.vectorstock.com/royalty-free-vector/refresh-icon-vector-10874963
# EDIT_ICON = r"./images/edit_polygon.png" #https://www.flaticon.com/premium-icon/polygon_2350224
# EDIT_TAG_ICON = r"./images/label_3.png" #https://www.pinclipart.com/maxpin/oTxJix/



class ConvertImages:
    def __init__(self, dict):
        self.dict = dict

    def prepare_images(self):
        for image in self.dict:
            image['image'] = self.convert_image(image['file'], image['zoom'])
        return self.dict

    def convert_image(self, image, zoom):
        call_img = PIL_imagetk.PhotoImage(file=image)
        zoom_img = call_img._PhotoImage__photo.subsample(zoom)
        return zoom_img

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

#A function that creates the tooltip
def CreateToolTip(widget, text):
    #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
    toolTip = ToolTip(widget)
    def enter(event): #to show tooltip
        toolTip.showtip(text) #call showtip
    def leave(event):
        toolTip.hidetip() #hide tooltip
    widget.bind('<Enter>', enter) #upon entry of mouse
    widget.bind('<Leave>', leave) #upon leave of mouse

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

        #for some reason these need to be global variables for the images to show
        # imgs_custom_btns = [{"name": 'Jump to First Slice', "image": self.convert_image(START_ICON, 8)},
        #                     {"name": 'Jump to Last Slice', "image": self.convert_image(END_ICON, 7)},
        #                     {"name": 'Play Slice Slideshow', "image": self.convert_image(PLAY_ICON, 20)},
        #                     {"name": "Draw Polygon", "image": self.convert_image(DRAW_ICON, 8)},
        #                     {"name": "Select Polygon", "image": self.convert_image(SELECT_ICON, 8)},
        #                     {"name": "Edit Polygon", "image": self.convert_image(EDIT_ICON, 28)},
        #                     {"name": "Delete Polygon", "image": self.convert_image(DELETE_ICON, 10)},
        #                     {"name": "Show Polygons", "image": self.convert_image(SHOW_ICON, 8)},
        #                     {"name": "Edit Polygon Tag", "image": self.convert_image(EDIT_TAG_ICON, 23)},
        #                     {"name": "Refresh Polygons", "image": self.convert_image(REFRESH_ICON, 10)}
        #                     ]

        #Prepare the Images for the buttons
        # images = ConvertImages(custom_btn_images)
        # imgs_custom_btns = images.prepare_images()

        self.frames = {}
        for f, geometry in zip((StartPage, PageOne), ('400x300+550+200', "1400x1050+50+0")):
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

        #function for converting an image so it can be displayed, also takes a zoom parameter
    def convert_image(self, image, zoom):
        call_img = PIL_imagetk.PhotoImage(file=image)
        zoom_img = call_img._PhotoImage__photo.subsample(zoom)
        return zoom_img
        #https://stackoverflow.com/questions/58411250/photoimage-zoom

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

        self.page_title = tk.Label(self.header, text="Delineation Can Commence", font=LARGE_FONT, foreground=FONT_COL, bg=HEADER_BG)      # Store this as an instance variable
        self.page_title.pack(side="left", pady=10, padx=10)

        #load scans button frame & btns (Close tabs & config settings also in the frame)
        self.browse_frame = tk.Frame(self.main_section, bg=MAIN_BG)
        self.browse_frame.pack(side="top", fill="x")
        self.browse_frame.rowconfigure(0, weight=1)
        self.browse_frame.columnconfigure(0, weight=1)
        self.browse_frame.columnconfigure(1, weight=1)
        self.browse_frame.columnconfigure(2, weight=1)

        #Tab area & Panes & Close tab controls
        self.tab_area = tk.Frame(self.main_section, background=MAIN_BG)
        self.tab_area.pack(side="bottom", fill="both", expand=True)

        self.panes = []
        self.notebook_1_frame = tk.Frame(self.tab_area, bg=MAIN_BG) #had as red when working with the split frames
        self.notebook_1_frame.grid(row=0, column=0, sticky="NSWE")
        self.panes.append(self.notebook_1_frame)
        self.notebook_2_frame = tk.Frame(self.tab_area, bg=MAIN_BG) #had as yellow when working with the split frames
        self.panes.append(self.notebook_2_frame)
        self.comparison_open = False

        self.tab_area.rowconfigure(0, weight=1)
        self.tab_area.columnconfigure(0, weight=1)

        self.tab_pane = ttk.Notebook(self.notebook_1_frame)
        # self.tab_pane = CustomNotebook(self.main_section)

        self.slice_info_items = ["Year", "Scan Type", "Patient"]
        self.slice_info = None
        self.slice_info_tab_2 = None

        self.tab_pane.bind("<<NotebookTabChanged>>", lambda e: self.update_viewing_information(self.tab_pane, self.slice_info, self.tabs_1)) #Used to know which tab is selected
        #https://stackoverflow.com/questions/48104061/python-tkinter-bindtag-event-handling-how-to-update-which-tab-is-currently-sel
        self.tab_pane.pack(side="left", fill="both", expand=True, pady=(0, 10), padx=10)
        self.tabs_1 = [] #This is used to store instances of tab panes when they are open
        self.tabs_2 = []
        self.tab_pane_2 = ttk.Notebook(self.notebook_2_frame)
        # self.tab_pane = CustomNotebook(self.main_section)
        self.tab_pane_2.bind("<<NotebookTabChanged>>", lambda e: self.update_viewing_information(self.tab_pane_2, self.slice_info_tab_2, self.tabs_2)) #Used to know which tab is selected
        #https://stackoverflow.com/questions/48104061/python-tkinter-bindtag-event-handling-how-to-update-which-tab-is-currently-sel
        self.tab_pane_2.pack(side="left", fill="both", expand=True, pady=10, padx=10)

        # self.browse_btn_lab = tk.Label(self.browse_frame, text="Load Stacks:", font=SMALL_FONT, bg=MAIN_BG, fg=FONT_COL)      # Store this as an instance variable
        # self.browse_btn_lab.pack(side="left", pady=10, padx=10)
        self.load_stacks_controls = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.load_stacks_controls.grid(column=0, row=0, sticky="NSWE")

        self.browse_btn = ttk.Button(self.load_stacks_controls, text="Load A Stack", command=lambda: self.load_scans(self.tab_pane), width=25)
        self.browse_btn.pack(side="left", pady=(10, 0), padx=10)

        self.browse_btn_two = ttk.Button(self.load_stacks_controls, text="Load A Comparison Stack", command=lambda: self.load_scans(self.tab_pane_2), width=25, state='disabled')
        self.browse_btn_two.pack(side="left", pady=(10, 0), padx=10)

        self.swap_btn_frame = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.swap_btn_frame.grid(column=1, row=0, sticky="NSWE")
        # self.swap_btn_frame.pack(side="left", pady=10, padx=(105, 0))

        self.swap_to_left_btn = ttk.Button(self.swap_btn_frame, text="<", width=5, command=lambda: self.swap_tab("left", self.tab_pane_2, self.tab_pane))
        # self.swap_to_left_btn.pack(side="left", pady=5, padx=(30, 5))
        self.swap_to_right_btn = ttk.Button(self.swap_btn_frame, text=">", width=5, command=lambda: self.swap_tab("right", self.tab_pane, self.tab_pane_2))
        # self.swap_to_right_btn.pack(side="left", pady=5, padx=5)

        self.other_btns = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.other_btns.grid(column=2, row=0, sticky="NSWE")

        self.settings = PolygonSettings(SETTINGS)
        self.config_settings = ttk.Button(self.other_btns, text="Polygon Settings", command=self.settings.change_settings)
        self.config_settings.pack(side="right", pady=(10, 0), padx=10)

        self.close_tabs_btn = ttk.Button(self.other_btns, text="Close all tabs", command=self.remove_tabs, state="disabled")
        self.close_tabs_btn.pack(side="right", pady=(10, 0), padx=10)

        #Controls for quiting or heading back to Start Page
        self.header_btns = tk.Frame(master=self.header, bg=HEADER_BG)
        self.header_btns.pack(side="right", pady=10, padx=10)
        self.close_session_btn = ttk.Button(self.header_btns, text="LogOut", command=lambda: self.controller.show_frame(StartPage, self.entry.get()), width=12)
        self.close_session_btn.grid(row=1, column=0)
        self.quit_btn = ttk.Button(self.header_btns, text="Quit", command=quit, width=12)
        self.quit_btn.grid(row=0, column=0, pady=(0, 10))

        #Information for User currently on program
        self.session_info_items = ["User", "Start Time"]
        self.session_info = InformationBox(self.header, "right", 10, 2, "Current Session", self.session_info_items)

        self.currently_viewing_frame = tk.Frame(self.header, bg=HEADER_BG)
        self.currently_viewing_frame.pack(side="right")



        #colour picker
        # self.variable = tk.StringVar(self)
        # self.colour_schemes = []
        # for item in COLOUR_SCHEMES:
        #     self.colour_schemes.append(item['name'])
        #
        # self.optionmenu = ttk.OptionMenu(self.header, self.variable, *self.colour_schemes)
        # self.optionmenu.pack(side="right", pady=0)

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
            self.browse_btn_two['state'] = 'normal'
        else:
            self.browse_btn_two['state'] = 'disabled'

    def update_viewing_information(self, notebook, currently_viewing_info, tabs):
        #if length of tabs is less than two then focused tab will be tab in existance anyway, destorying the tabs actually focuses each tab in turn
        if len(tabs) > 1:
            text = notebook.tab(notebook.select(), "text")
            #https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook
            text = re.split(" | ", text)
            #change currently viewing on tab select not load of scans
            info = [text[0], text[4], text[2]]
            print("info", info)
            currently_viewing_info.state_information(info)

        #temp thing to destroy the frames - need to really create a session class that is called
    def destroyFrame(self, StartPage, username):
        #reset to defaults
        self.settings.reset()
        #resets the slice info to not applicable
        if self.slice_info != None:
            self.slice_info.reset_to_na()
        #removes the tabs
        self.remove_tabs()
        #Head back to the start page
        self.controller.show_frame(StartPage, username)

    #Function is called by the "owner" of PageOne, MainApp, which can pass messages for us
    def sendmsg(self, username ):
        time = start_time() #call time to get current time this is called
        self.session_info.state_information([username, time]) #update the session info for the new session

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
                    self.slice_info = InformationBox(self.currently_viewing_frame, "left", 10, 2, "Currently Viewing Tab 1", self.slice_info_items)

                if (notebook == self.tab_pane_2) and len(self.tabs_2) < 1:
                    self.slice_info_tab_2 = InformationBox(self.currently_viewing_frame, "right", 10, 2, "Currently Viewing Tab 2", self.slice_info_items)
                    self.add_comparison_frame()
                    self.swap_to_left_btn.pack(side="left", pady=5, padx=(30, 5))
                    self.swap_to_right_btn.pack(side="left", pady=5, padx=5)

                slice_address_segments = re.split("/", folder_selected) #split directory address
                new_tab = Tab(notebook) #create a new tab instance
                tab_pane = new_tab.add_tab(slice_address_segments[7] + " | " + slice_address_segments[8] + " | " +  slice_address_segments[10])
                self.tabs_1.append(tab_pane) #add the pane to self.tabs - works with the remove tabs btn



                info = [slice_address_segments[7], slice_address_segments[10], slice_address_segments[8]]
                if notebook == self.tab_pane:
                    self.slice_info.state_information(info) #updates the slice info for the current loaded up tab - loaded tab is one in focus

                if notebook == self.tab_pane_2:
                    self.tabs_2.append(tab_pane)
                    self.slice_info_tab_2.state_information(info)

                SliceFigure(tab_pane, folder_selected,  options, True, 0, self.session_info.pull_detail('User'), slice_address_segments) #creates the figure for the tab
                self.close_tabs_btn['state'] = "normal" #can now close all tabs
                self.unlock_comparison_stacks_btn()

            # except Exception as e:
            #     print(e)
            #     messagebox.showerror("Error Loading MRI Slices", "An error occured loading this folder.")
        else:
            messagebox.showerror("Error Loading MRI Slices", "There are no Numpy Array Files available within this folder.") #there were no numpy arrays in the folder

    #Function to remove all tabs
    def remove_tabs(self):
        # notebooks = [self.tab_pane, self.tab_pane_2]
        # for notebook in notebooks:
        #     tabs = notebook.tabs()
        #     if len(tabs) > 0:
        #         for tab in tabs:
        #             tab.forget()


        # if len(self.tab_pane_2.tabs()) > 0:
        #     self.tab_pane_2.forget()

        if len(self.tabs_1) > 0:
            for tab in self.tabs_1:
                tab.destroy()

        self.tabs_1.clear() #remember to clear the self.tabs as this is not reset as page one is not called by original class it is lifted above
        self.tabs_2.clear()
        self.close_tabs_btn['state'] = "disabled" #now no tabs to remove
        # self.slice_info.reset_to_na() #reset slice information to not applicable

        if self.slice_info != None:
            self.slice_info.make_box_go_walkies()
            self.slice_info = None
        if self.slice_info_tab_2 != None:
            self.slice_info_tab_2.make_box_go_walkies()
            self.slice_info_tab_2 = None


        self.comparison_open == True #resets the screen to one screen
        self.unlock_comparison_stacks_btn()
        self.add_comparison_frame()

        self.swap_to_left_btn.pack_forget()
        self.swap_to_right_btn.pack_forget()

    def swap_tab(self, direction, current_notebook, destination_notebook):
        #get selected tab
        #add selected tab to other tab pane #direction provides the tab pane locations left is 2 to 1
        #remove tab from current tab pane
        # tab = current_notebook.select()
        # print(tab)
        # last_tab = re.split("!", tab)
        # last_tab[len(last_tab) - 1]
        # print(last_tab)

        text = current_notebook.tab(current_notebook.select(), "text")
        text = re.split(" | ", text)
        #change currently viewing on tab select not load of scans
        info = [text[0], text[2], text[4]]
        info.insert(2, "01")
        folder = DIRECTORY + "/"
        for item in info:
            folder += item + "/"

        print(folder)



        options = []
        for item in os.listdir(folder):
            if item.endswith('.npy'): #has to be a numpy file
                options.append(str(item))

        slice_address_segments = re.split("/", folder)
        try:
            new_tab = Tab(destination_notebook) #create a new tab instance
            tab_pane = new_tab.add_tab(text[0] + " | " + text[2] + " | " +  text[4])
            self.tabs_1.append(tab_pane)

            SliceFigure(tab_pane, folder,  options, True, 0, self.session_info.pull_detail('User'), slice_address_segments)

            current_notebook.forget(current_notebook.select())

            if len(current_notebook.tabs()) == 0:
                if direction == "left":
                    print("hello")
                    self.comparison_open == True
                    self.swap_to_right_btn.pack_forget()
                    self.swap_to_left_btn.pack_forget()
                    self.add_comparison_frame()
                    print(self.comparison_open)
                    self.tabs_2.clear()
                    self.slice_info_tab_2.make_box_go_walkies()
                    self.slice_info_tab_2 = None

            elif len(current_notebook.tabs()) == 1:
                if direction == "right":
                    self.swap_to_right_btn['state'] = 'disabled'
            else:
                if direction == "right":
                    self.swap_to_right_btn['state'] = 'normal'

        except Exception as e:
            print(e)
            messagebox.showerror("Error Loading MRI Slices", "An error occured loading this folder.")
        #remove from apropiate tabs list
        #add to appropiate tabs list
        #check if any tabs in tab pane 2 - if none then go back to whole screen

#Class for a tab & tab pane
class Tab:
    def __init__(self, tab_pane):
        self.tab_pane = tab_pane

    def add_tab(self, text):
        tab1 = tk.Frame(self.tab_pane, background=HEADER_BG)
        self.tab_pane.add(tab1, text = text)
        self.tab_pane.select(tab1) #show selected tab  #https://stackoverflow.com/questions/27730509/how-to-change-the-tab-of-ttk-notebook
        return tab1

    def close_all_tabs(self):
        pass

#Class for a tab & tab pane
class PolygonSettings:
    def __init__(self, settings):
        self.settings_win = None
        self.settings = settings

        # for item in self.settings: #change values to default values first off
        #     item['current_value'] = item['default_value']

        self.colbuttons = []

    def change_settings(self):
        self.settings_win = tk.Toplevel(bg=MAIN_BG)
        self.settings_win.grab_set() #only allow one version of win #https://stackoverflow.com/questions/39689046/tkinter-only-allow-one-toplevel-window-instance
        self.settings_win.title("Polygon Settings")
        self.settings_win.lift()
        self.settings_win.resizable(0, 0) #https://www.geeksforgeeks.org/resizable-method-in-tkinter-python/
        # self.settings_win.attributes('-toolwindow', 'true')
        #https://stackoverflow.com/questions/45214662/tkinter-toplevel-always-in-front
        # self.settings_win.geometry("400x300")
        self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        self.tags = self.tags_writer.return_tags()
        #
        # self.tags_filename = r"C:\Users\Andrew\Documents\dissertation\tkinter\tags.json"
        # self.read_tags = jsonFileWriter(self.tags_filename, None, None)
        # self.tags = self.read_tags.read_file()

        self.colbuttons.clear()

        header_frame = tk.Frame(self.settings_win, bg=HEADER_BG)
        header_frame.pack(side="top", fill="x", expand=True)

        label = tk.Label(header_frame, text="Change Polygon Settings:", font=MEDIUM_FONT, bg=HEADER_BG, fg=FONT_COL)
        label.pack(side="top", fill="x", padx=10, pady=10, expand=True)



         #create instance of toggled frame
        t = ToggledFrame(self.settings_win, "Polygon Settings", MAIN_BG)
        t.pack(fill="x", expand=1, pady=10, padx=10, anchor="n")

        # ttk.Label(t.get_sub_frame(), text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
        # ttk.Entry(t.get_sub_frame()).pack(side="left")
        other_btns_frm = tk.Frame(t.get_sub_frame(), bg=MAIN_BG)
        other_btns_frm.pack(fill="x")

        reset_defaults_btn = ttk.Button(other_btns_frm, text="Reset Defaults", command=self.reset)
        reset_defaults_btn.pack(side="right", padx=10, pady=10)

        frame = tk.Frame(t.get_sub_frame(), bg=MAIN_BG)
        frame.pack(fill="x")

        i, j = 0, 0
        for item in self.settings:
            if item['configuable'] == True:
                label = tk.Label(frame, text=item['setting'] + ": ", padx=10, pady=10, bg=MAIN_BG, fg=FONT_COL)
                label.grid(row = i, column = j, sticky="W")
                if item['type'] == "number":
                    entry = tk.Entry(frame, width=5)
                    entry.grid(row=i, column=j + 1)
                    entry.insert(tk.END, item['current_value'])
                    callback = frame.register(self.only_numeric_input)  # registers a Tcl to Python callback
                    entry.configure(validate="key", validatecommand=(callback, "%P"))  # enables validation
                    #https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter/4140988#4140988
                    item['widget'] = entry
                if item['type'] == "color":
                    print(item['setting'])
                    button = tk.Button(frame, text="Change", command=lambda task=item['task'], setting=item['setting'], current_val = item['current_value'] : self.change_colour(task, setting, current_val))
                    button.grid(row=i, column=j + 1, sticky="W")
                    self.colbuttons.append(button)
                    square = tk.Frame(frame, background=item['current_value'], width=15, height=15)
                    item['widget'] = square
                    square.grid(row=i, column= j+2, padx=10, pady=10)
                i += 1

        ##**FIX **##
        #button thing again need to be done manually - don't seem to go through the lambda in the above dynamic work, so need to do seperatly.
        current_vals = []
        for item in self.settings:
            if item['type'] == 'color':
                current_vals.append(item['current_value'])
        print(self.colbuttons)
        self.colbuttons[0]['command'] = lambda: self.change_colour("Choose Unknown Tag Colour", "Unknown Tag Colour", current_vals[0])
        self.colbuttons[1]['command'] = lambda: self.change_colour("Choose Selected Polygon Colour", "Selected Polygon Colour", current_vals[1])
        self.colbuttons[2]['command'] = lambda: self.change_colour("Choose Selected Vertex Colour", "Selected Vertex Colour", current_vals[2])

        ##** **##

        #Tags frame
        tags_tab = ToggledFrame(self.settings_win, "Tags", MAIN_BG)
        tags_tab.pack(fill="x", expand=1, pady=10, padx=10, anchor="n")

        self.tags_frame = tk.Frame(tags_tab.get_sub_frame(), bg=MAIN_BG)
        self.tags_frame.pack(fill="x")

        self.add_tag_frame = tk.LabelFrame(self.tags_frame, text=" Add New Tag: ", background=MAIN_BG, fg=FONT_COL)
        self.add_tag_frame.grid(row=0, column=0, sticky="NSWE", padx=10, pady=10)

        self.error_msg = tk.Label(self.add_tag_frame, background=MAIN_BG, fg="red") #Error message that appears when tag already exists/no tag is added

        self.tag_entry = tk.Entry(self.add_tag_frame, highlightbackground = "red", highlightcolor = "red", highlightthickness = 0)
        self.tag_entry.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10)
        self.tag_entry.insert(tk.END, "Tag Label...")
        self.tag_entry.bind("<Button-1>", lambda e: self.watch_for_txtbx_click(self.tag_entry.get())) #bind function on the event of clicking the text box


        self.colour_pick = tk.Button(self.add_tag_frame, text="Pick Colour", command=lambda: self.pick_colour("Choose Tag Colour"), state="disabled")
        self.colour_pick.grid(row=2, column=0, padx=10, pady=10)

        self.colour_frm = tk.Frame(self.add_tag_frame, width=15, height=15)

        self.clear_btn = ttk.Button(self.add_tag_frame, text="Clear", command=self.clear_tag, state="disabled")
        self.clear_btn.grid(row=3, column=0, padx=10, pady=10)
        self.add_btn = ttk.Button(self.add_tag_frame, text="Add", command=self.add_tag, state="disabled")
        self.add_btn.grid(row=3, column=1, padx=10, pady=10)

        self.added_tag = {"label": None, "colour": None}

        self.create_tags_table(self.tags_frame)


        buttons_frame = tk.Frame(self.settings_win, padx=15, pady=15, bg=MAIN_BG)
        buttons_frame.pack(side="bottom", fill="x")

        confirm_btn = ttk.Button(buttons_frame, text="Confirm", command=self.confirm_settings)
        confirm_btn.pack(side="right")

        cancel_btn = ttk.Button(buttons_frame, text="Cancel", command=self.close_settings_win)
        cancel_btn.pack(side="left")

    def create_tags_table(self, frame):
        table_frame = tk.Frame(frame, background=MAIN_BG)
        table_frame.grid(row=1, column=0, sticky="NSEW")
        col_settings = [{"column": "label", "wraplength":75, "side": "left", "width": 11, "fill": False},
                        {"column": "colour", "wraplength":50, "side": "left", "width": 7, "fill": True}
                        ]

        row_btns = [{"name": "remove", "text": "X", "function":lambda args: self.remove_tag(args), "width": 3},
                    {"name": "edit", "text": "Edit", "function": lambda args: self.change_tag_colour(args), "width": 3}
                    ]
        table = NoteTable(table_frame, col_settings, self.tags, 205, 150, row_btns)

    def change_tag_colour(self, *args):
        print(args)
        # print(title)
        colour = colorchooser.askcolor(title = "Change Colour: Tag {}".format(args[0][0]), color=args[0][1])
        if colour != None:
            print(colour[1])
            #add tag to JSON file - Use jsonFileWriter for this as not checking contents

            for tag in self.tags:
                if (tag['label'] == args[0][0]) and (tag['colour'] == args[0][1]):
                    tag['colour'] = colour[1]

            self.tag_writer = jsonFileWriter(TAGS_DATA_FILENAME, self.tags, None)
            self.tag_writer.create_json_file(self.tags) #will overwrite json file with new tag colour
            #call again to get updated
            self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
            self.tags = self.tags_writer.return_tags()
            #update table
            self.create_tags_table(self.tags_frame)

    def remove_tag(self, *args):
        print(args)
        result = messagebox.askquestion("Delete Tag", "Are you sure you want to delete Tag: {}?".format(args[0][0]), icon='question')
        print(result)
        if result:
            #update json
            #remove tag
            self.tags = [item for item in self.tags if item['label'] != args[0][0] and item['colour'] != args[0][1]] ##**DOESN@T SEEM TO WORK|

            self.tag_writer = jsonFileWriter(TAGS_DATA_FILENAME, self.tags, None)
            self.tag_writer.create_json_file(self.tags) #will overwrite json file with new tag colour

            #call again to get updated
            self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
            self.tags = self.tags_writer.return_tags()
            #update table
            self.create_tags_table(self.tags_frame)

    def watch_for_txtbx_click(self, text):
        if (text == "Tag Label...") or (text == "Add..."): #if the present text in the textbox is equal to the insert then remove all text
            self.tag_entry.delete(0, 'end') #https://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
            # self.tag_entry.delete("insert linestart", "insert lineend") #removes all text
        self.colour_pick['state'] = "normal"

    def clear_tag(self):
        self.tag_entry.delete(0, 'end')
        self.tag_entry.insert(tk.END, "Tag Label...")
        self.tag_entry['highlightthickness'] = 0

        self.colour_pick['state'] = "disabled"
        self.colour_frm.grid_forget()
        self.error_msg.grid_forget()
        self.added_tag['label'] = None
        self.added_tag['colour'] = None

        self.add_btn['state'] = "disabled"
        # self.colour_frm['background'] = None

    def add_tag(self):
        if len(self.tag_entry.get()) > 0: #if there is text present in the label entry box
            #get tag from label box, (strip removes the whitespace from the edges)
            self.added_tag['label'] = self.tag_entry.get().strip()
            #check that the tag is not already present
            print("tags", self.tags)
            tag_replicated = False
            for tag in self.tags:
                if tag['label'] == self.added_tag['label']:
                    tag_replicated = True
                    self.tag_entry['highlightthickness'] = 2
                    self.error_msg['text'] = "Tag Name Already Exists."
                    self.error_msg.grid(row=0, column=0, padx=10, columnspan=2, sticky="W")

            if not tag_replicated:
                #add tag
                self.tags.append(self.added_tag) #add new tag

                #add tag to JSON file - Use jsonFileWriter for this as not checking contents
                self.tag_writer = jsonFileWriter(TAGS_DATA_FILENAME, self.tags, None)
                self.tag_writer.create_json_file(self.tags) #will overwrite json file

                #Need to reload as jsonFIleWrtier is only called once in this class, need to show updated
                self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
                self.tags = self.tags_writer.return_tags() #pull tags

                self.error_msg.grid_forget()
                self.clear_tag() #clear the new tag to be added
                self.create_tags_table(self.tags_frame) #refresh the table
        else:
            print("No Label Entered.")
            self.tag_entry['highlightthickness'] = 2 #highlight the box in red to alert user, done this instead of warning label
            self.error_msg['text'] = "Tag Name Required."
            self.error_msg.grid(row=0, column=0, padx=10, columnspan=2, sticky="W")
            self.tag_entry.insert(tk.END, "Add...")
            self.tag_entry.bind("<Button-1>", lambda e: self.watch_for_txtbx_click(self.tag_entry.get())) #bind function on the event of clicking the text box
            #highlight entry box

    def only_numeric_input(self, digit):
        # checks if entry's value is an integer or empty and returns an appropriate boolean
        if digit.isdigit() or digit == "":  # if a digit was entered or nothing was entered
            return True
        return False

    def hello(self):
        print("hello")

    def close_settings_win(self):
        if self.settings_win != None:
            for item in self.settings:
                item['temp_value'] = None #reset the temp values
            self.settings_win.destroy() #destroy window

    def reset(self):
        for item in self.settings: #change values to default values
            item['temp_value'] = item['default_value'] #reset the settings to their default value
        if self.settings_win != None: #if window has been opened in session
            if self.settings_win.winfo_exists() == 1: #if window exists then == 1 and is open
                for item in self.settings:
                    if item['widget'] != None:
                        if item['type'] == "number":
                            item['widget'].delete(0, tk.END) #clear entry box
                            item['widget'].insert(tk.END, item['temp_value']) #refil entry box
                        elif item['type'] == "color":
                            item['widget']['background'] = item['temp_value'] #reset the colour sqaure

    def confirm_settings(self):
        for item in self.settings:
            if item['type'] == 'number':
                item['temp_value'] = int(item['widget'].get()) #remember get from an entry box returns a String
        for item in self.settings:
            if item['temp_value'] != None: #item has been changed
                item['current_value'] = item['temp_value']

        self.close_settings_win()

    def change_colour(self, task, setting, current_col):
        for item in self.settings:
            if item['setting'] == setting:
                print(item['setting'])
                print(item['task'])
                if item['temp_value'] != None:
                    current_col = item['temp_value']
        colour = colorchooser.askcolor(title = task, color=current_col)

        for item in self.settings:
            if item['setting'] == setting:
                item['temp_value'] = colour[1]
                item['widget']['background'] = colour[1]
        self.settings_win.lift()
        #https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front

        #When the Pick Colour btn is clicked, following function is called to allow user to choose colour. Depending on choice unlocks next stage of btns etc
    def pick_colour(self, task):
        colour = colorchooser.askcolor(title = task)

        #if cancel is clicked then None is returned, only unlock if a colour is returned
        #colour[1] is the hex value
        if colour[1] != None:
            self.colour_frm['background'] = colour[1]
            self.colour_frm.grid(row=2, column=1, pady=10, sticky="W")
            self.added_tag['colour'] = colour[1]
            self.clear_btn['state'] = "normal"
            self.add_btn['state'] = "normal"

        return colour[1]

#Class for a box of information with labels & dynamic updates
class InformationBox:
    def __init__(self, parent_frame, pack_side, padding, rows, header, label_headers):
        self.parent_frame = parent_frame
        self.pack_side = pack_side
        self.padding = padding
        self.rows = rows
        self.header = header
        self.label_headers = label_headers
        self.labels = []
        self.dict = {}

        # for item in self.label_headers:
        #     label_dict = {}
        #     label_dict["header"] = item
        #     self.dict.append(label_dict)

        #parent label frame box for contents
        self.content_frame = tk.LabelFrame(self.parent_frame, text = self.header + " :  ", foreground = FONT_COL, bg = HEADER_BG, pady=self.padding, padx=self.padding)
        self.content_frame.pack(side=self.pack_side, pady=self.padding, padx=self.padding)

        #create labels and info labels
        row = 0
        column = 0
        padx = (0, 0)
        print(label_headers)
        for label in self.label_headers:
            print(row)
            label_head = tk.Label(self.content_frame, text=label + ": ", foreground=FONT_COL, bg=HEADER_BG).grid(row=row, column=column, sticky="W", padx=padx)
            label = tk.Label(self.content_frame, text= " ", foreground=FONT_COL, bg=HEADER_BG)
            label.grid(row=row, column=column + 1, sticky="W")
            self.labels.append(label)
            if row != self.rows:
                row += 1
            if row == self.rows:
                column += 2
                row = 0
                padx = (25, 0)


        self.reset_to_na() #put them back to not applicable for the start
        # print(self.labels)

    def reset_to_na(self):
        for label in self.labels:
            label['text']  = "n/a"

        for item in self.label_headers:
            self.dict[item] = "n/a"
            # item['value'] = "n/a"

    def state_information(self, information):
        if len(information) != len(self.labels):
            print("incorrect information provided")
        else:
            i = 0
            for label in self.labels:
                label['text']  = information[i]
                i += 1

            # i = 0
            # for item in self.dict:
            #     item['value'] = information[i]
            #     i += 1
            i = 0
            for item in self.label_headers:
                self.dict[item] = information[i]
                i += 1
            print(self.dict)

    def pull_detail(self, label):

        return self.dict[label]

    def make_box_go_walkies(self):
        self.content_frame.pack_forget()

#Class for the Figure generated by selecting a folder
class SliceFigure:
    def __init__(self, parent_frame, folder_selected, slice_list, new_load, current_position, username, slice_info):
        #Global Variables needed for the IMGs
        # global poly_draw_img_zoomed, poly_slct_img_zoomed, poly_delete_img_zoomed, poly_play_img_zoomed, back_to_start_img_zoomed, to_end_img_zoomed
        # global images_list
        # global imgs_custom_btns

        self.frame = parent_frame
        self.username = username
        self.slice_info = slice_info
        self.folder_selected  = folder_selected
        self.current_position = current_position
        self.slice_list = slice_list
        self.intro_label_frm_txt = "Stack: "

        self.settings = SETTINGS
        self.figure_background = [item['current_value'] for item in self.settings if item['setting'] == "Figure Background"][0]

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

        #dropdown for the polygon type, tags come from settings
        self.polygon_tags = []

        #Pull the tags & check file
        self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        self.tags = self.tags_writer.return_tags()

        #Add tag & ensure capitalised
        for tag in self.tags:
            self.polygon_tags.append(tag['label'].capitalize())

        self.polygon_tag_var = tk.StringVar(self.frame)
        self.polygon_tag_var.set(self.polygon_tags[0]) # default value is shown, to then be changed for speed
        self.polygon_tag_chosen = self.polygon_tag_var.get() #assign variable to default

        self.polygon_tag_lab = tk.Label(self.polygon_tag_frame, text="Draw: ", background=HEADER_BG, fg=FONT_COL)
        self.polygon_tag_lab.grid(row=0, column=0, sticky="W")

        self.polygon_tag_choice = ttk.Combobox(self.polygon_tag_frame, values=self.polygon_tags) #Use ttk. combo box as looks more appealing
        self.polygon_tag_choice.current(0) #current value in the combo box
        self.polygon_tag_choice.grid(row=0, column=1, sticky="W", padx=5)

        self.polygon_tag_choice.bind("<<ComboboxSelected>>", self.change_tag)

        #information label, updated throughout depending on actions
        self.information = tk.Label(self.graph_frame_header, text="Hola, Me llamo Andrew", fg="green", background=HEADER_BG)
        self.information.grid(row=0, column=1, sticky="W")

        self.sync_btn = ttk.Button(self.graph_frame_header, text="Synchronise")
        self.sync_btn.grid(row=0, column=2, sticky="E", padx=10)

        #Graph Frame
        self.slice_name = self.slice_list[self.current_position][:-4]

        self.fig_frame = tk.LabelFrame(self.graph_frame, text="  {} {} ".format(self.intro_label_frm_txt, self.slice_name), background=HEADER_BG, foreground=FONT_COL)
        # self.graph_frame.grid(row=13, column=0, columnspan=6, rowspan=10, padx=10, pady=10)
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

        #Toolbar
        self.toolbar = CustomToolbar(self.canvas, self.fig_frame) # self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame) = I have used a CustomToolbar
        self.toolbar.config(background=HEADER_BG)
        # self.toolbar.config(color=HEADER_BG)
        # self.toolbar.config(fg=HEADER_BG)
        # self.toolbar.config(textcolor=HEADER_BG)
        # print(help(self.toolbar))
        # help(self.toolbar.config)
        # print(dir(self.toolbar.config.__format__))
        # print(list(filter(lambda x:callable(getattr(self.toolbar.config,x)),self.toolbar.config.__dir__())))
        style = ttk.Style()
        # print(style.element_options(self.toolbar))
        self.toolbar.update()
        #https://stackoverflow.com/questions/48351630/how-do-you-set-the-navigationtoolbar2tkaggs-background-to-a-certain-color-in-tk
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.toolbar.children['!button6'].pack_forget() #to forget the configure subplots button

        # print(dir(self.toolbar.children["!button4"]))
        # self.toolbar.children["!button"].config(background="orange")
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
        # self.custom_btns = [{"name": 'Jump to First Slice', "image": back_to_start_img_zoomed, "padding": (5, 1), "description": 'start', "dlft_state": "normal"},
        #                     {"name": 'Jump to Last Slice', "image": to_end_img_zoomed, "padding": (1, 2), "description": 'end', "dlft_state": "normal"},
        #                     {"name": 'Play Slice Slideshow', "image": poly_play_img_zoomed, "padding": (5, 5), "description": 'play', "dlft_state": "normal"},
        #                     {"name": "Draw Polygon", "image": poly_draw_img_zoomed, "padding": (0, 2), "description": 'draw', "dlft_state": "normal"},
        #                     {"name": "Select Polygon", "image": poly_slct_img_zoomed, "padding": (0, 2), "description": 'select', "dlft_state": "disabled"},
        #                     {"name": "Delete Polygon", "image": poly_delete_img_zoomed, "padding": (0, 2), "description": 'delete', "dlft_state": "disabled"}
        #                     ]

        # self.custom_btns = [{"name": 'Jump to First Slice', "image": images_list[0], "padding": (5, 1), "description": 'start', "dlft_state": "normal"},
        #                     {"name": 'Jump to Last Slice', "image": images_list[1], "padding": (1, 2), "description": 'end', "dlft_state": "normal"},
        #                     {"name": 'Play Slice Slideshow', "image": images_list[2], "padding": (5, 5), "description": 'play', "dlft_state": "normal"},
        #                     {"name": "Draw Polygon", "image": images_list[3], "padding": (0, 2), "description": 'draw', "dlft_state": "normal"},
        #                     {"name": "Select Polygon", "image": images_list[4], "padding": (0, 2), "description": 'select', "dlft_state": "disabled"},
        #                     {"name": "Delete Polygon", "image": images_list[5], "padding": (0, 2), "description": 'delete', "dlft_state": "disabled"}
        #                     ]

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

        images = ConvertImages(custom_btn_images)
        imgs_custom_btns = images.prepare_images()

        for item in imgs_custom_btns:
            print(item)
            for btn in self.custom_btns:
                if item['name'] == btn['name']:
                    btn['image'] = item['image']

        #QUESTION: WHY CANNOT PASS THROUGH FUNCTION?
        i = 0
        # self.cid = self.figure.canvas.mpl_connect('button_press_event', None)
        for btn in self.custom_btns:
            # button = tk.Button(master=custom_btn_frame, image=btn['image'], command=lambda description = btn['description']: self.click_tb_btn(description), state = btn['dlft_state'])
            # print(btn['description'], "before")
            button = tk.Button(master=custom_btn_frame, image=btn['image'], command=btn['command'], state = btn['dlft_state'])
            # print(btn['description'], "after")
            # button['command'] = lambda: self.click_tb_btn(btn['name'])
            btn['widget'] = button
            button.config(width=btn_width, height=btn_height)
            CreateToolTip(button, text = btn['name']) #calling of instance of tooltip for draw btn
            button.grid(row=0, column=i, padx=btn['padding'])
            i += 1
            #https://stackoverflow.com/questions/47212078/tkinter-how-to-replace-a-button-with-a-image


        #load up First Figure
        if new_load == True:
            self.create_figure(self.fig_frame)

        self.pause = False
        self.clicked = 0

        #create instance of json file writer here
        self.slice_name = "PR150_01_0006_002_t2-axial"
        # self.filename = "./" + "polygon data.json"


        #create instance of polygons here
        # self.settings = {"precision": 5, "line_thickness": 2, "select_pol_col": "blue", "unknown_tag_col": "pink" , "tags":[{"label":"suspicious", "colour":"red"},
        #                                                                                                     {"label":"anatomical", "colour":"green"},
        #                                                                                                     {"label":"other", "colour":"orange"}], "highlighted_plot": {"size": 125, "color": "yellow"}}
        #
        self.selected_polygon = None
        self.current_slice = None
        #Notebox Class is called to make this appear when calling Slice Figure
        self.notebox = Notebox(self.frame, self.username, self.slice_list[self.current_position][:-4], self.slice_info, self.folder_selected, self.slice_list)

        self.filename = self.folder_selected + "/" + self.slice_list[self.current_position][:-4] + '_polygon_data.json'
        print(self.filename)
        self.jsonFileWriterPolygon = jsonFileWriterPolygon(self.filename, self.slice_list[self.current_position][:-4])
        self.slice_polygons = Polygons(self.jsonFileWriterPolygon, self.slice_list[self.current_position][:-4], self.figure, self.a, self.custom_btns, self.fc, self.information, self)


        # print(self, self.notebox)


    def create_figure(self, graph_frame):
        self.fig_frame['text'] = "  {} {} ".format(self.intro_label_frm_txt, self.slice_list[self.current_position][:-4])
        slice_address = self.folder_selected + "/" + self.slice_list[self.current_position]
        slice = np.load(slice_address)

        self.a.imshow(np.squeeze(slice), cmap='gray')
        self.filename = self.folder_selected + "/" + self.slice_list[self.current_position][:-4] + '_polygon_data.json'
        print(self.filename)
        self.jsonFileWriterPolygon = jsonFileWriterPolygon(self.filename, self.slice_list[self.current_position][:-4])
        self.slice_polygons = Polygons(self.jsonFileWriterPolygon, self.slice_list[self.current_position][:-4], self.figure, self.a, self.custom_btns, self.fc, self.information, self)
        self.canvas.draw() #canvas.show does not work anymore

        self.determine_btn_status()



    def get_selected_polygon(self, polygon):
        self.selected_polygon = polygon
        self.notebox.set_selected_polygon(polygon)
        # self.current_slice = slice

    # def get_current_slice(self, slice):
    #     self.current_slice = slice
    #     print(self, self.notebox)
        # self.notebox.set_slice(slice)

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
            # self.jsonFileWriterPolygon = jsonFileWriterPolygon(self.filename, self.slice_list[self.current_position][:-4])
            # self.slice_polygons = Polygons(self.settings, self.jsonFileWriterPolygon, self.slice_list[self.current_position][:-4], self.figure, self.a, self.custom_btns, self.fc, self.information)

        elif btn == "draw":
            self.fc.connect(lambda event: self.slice_polygons.draw_btn_click(event, self.polygon_tag_chosen))
        elif btn == "select":
            self.fc.connect(lambda event: self.slice_polygons.select_polygon(event))
        elif btn == "show":
            self.fc.connect(self.slice_polygons.show_polygons())
        elif btn == "refresh":
            self.fc.connect(self.slice_polygons.load_polygons()) #load polygons just refreshs the polygons on the slice, incomplete polygons are not saved to json
            # print(btn, "Polygon btn")

    # def get_coords(self, event):
    #     ix, iy = event.xdata, event.ydata #x and y data
        # print('x = {}, y = {}'.format(ix, iy)) #prints the co-ordinates
        ##https://stackoverflow.com/questions/25521120/store-mouse-click-event-coordinates-with-matplotlib
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

    # def get_current_slice(self):
    #     pass

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

class TagFileLoader:
    def __init__(self, filename):
        self.filename = filename
        #defaults for the tags, if file is deleted
        self.defaults = [{"label": "Suspicious: PI-RAD 1", "colour": "#FF0000"},
                        {"label": "Suspicious: PI-RAD 2", "colour": "#FF0000"},
                        {"label": "Suspicious: PI-RAD 3", "colour": "#FF0000"},
                        {"label": "Suspicious: PI-RAD 4", "colour": "#FF0000"},
                        {"label": "Suspicious: PI-RAD 5", "colour": "#FF0000"},
                        {"label": "Anatomical", "colour": "#228B22"},
                        {"label": "Other", "colour": "#FFFF00"}
                        ]

        #Load tags file & create if has been deleted
        try:
            self.tag_file_writer = jsonFileWriter(self.filename, self.defaults, None)
            self.tags = self.tag_file_writer.read_file()

            if len(self.tags) == 0:
                #if no tags then re-input with default tags
                self.tag_file_writer.create_json_file(self.defaults)
                #file is just default tags currently
                self.tags = self.defaults
                print("Tags not present. Default tags added.")
            else:
                self.tags = self.check_tags(self.tags)

                print("Tags Present & checked.")

        except FileNotFoundError:
            print("System cannot find path specified using address: " + self.filename)


        #pull the tags from the file
    def return_tags(self):
        return self.tags

        #check tag for correct keys & values in above default structure. Eg. if it has a label that is string & colour which is a hex colour
    def check_tags(self, tags):
        checked_tags = []
        for tag in tags:
            try:
                if type(tag['label']) == str and type(tag['colour']) == str and self.hex_validator(tag['colour']):
                    checked_tags.append(tag)
                else:
                    print("Incorrect Value used for tag: " + str(tag) + " within " + self.filename + ". Tag not loaded.")
            except KeyError:
                print("Incorrect Key used for tag: " + str(tag) + " within " + self.filename + ". Tag not loaded.")
        return checked_tags

    def hex_validator(self, value):
        #supports both 3 and 6 digit forms of hex
        #https://stackoverflow.com/questions/20275524/how-to-check-if-a-string-is-an-rgb-hex-string
        hex = re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$')
        value = bool(hex.match(value))
        return value

class Polygons(SliceFigure):
    def __init__(self, file_writer, slice_name, f, a, polygon_buttons, cid, information_label, parent):
        #Tag Checker & pull tags
        self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        self.tags = self.tags_writer.return_tags()

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

    #function to load the polygons & draw them to the figure
    def load_polygons(self):
        #assign polygon_info for slice, file will only contain co-ordinates, takes in full file
        file_info = self.file_writer.read_file()
        file_sorted = self.file_writer.sort_file(file_info, "slice", self.slice_name)

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
        # for preset in self.settings['tags']:
        for preset in self.tags:
            if preset['label'].capitalize() == tag: #tag needs capitalising
                colour = True
                return preset['colour'] #colour goes with the custom made tag in the settings
        #Return polygons in colours where there are no tags present as in Pink colour - have this setable in the settings
        if not colour:
            # return self.settings['unknown_tag_col']
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
        result = PolygonTagChanger(polygon, self.tags).send()

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

#Class for the Notebox
class Notebox(SliceFigure):
    def __init__(self, parent_frame, username, slice_name, slice_info, folder_selected, slice_list):
        self.parent_frame = parent_frame #parent frame for notebox (Notebox contains the tab panes & instantiates the notetables & add note)
        self.username = username #passes through the username for the username for the session
        self.slice_name = slice_name #current slice name of the slice that is visible
        self.slice_info = slice_info #DISPENSIBLE = used for passing split up pieces of folder selected
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
            new_tab = Tab(self.note_tab_pane) #create tab pane
            inner_tab_frame = new_tab.add_tab(item['name'] + " Notes")
            self.show_note(inner_tab_frame, item['radio_name'])
            self.note_tabs.append({"tab":item['radio_name'], "frame":inner_tab_frame})
            item['tab_frame'] = inner_tab_frame

        #create add note tab
        self.new_tab_add = Tab(self.note_tab_pane) #create a new tab instance
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
            #style="Wild.TRadiobutton"
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
        self.notebox_btn_dict = [{"name": "clear", "command":lambda: self.notebox.clear_notebox(), "default_state": "normal", "side": "left"},
                                {"name": "add", "command":lambda: self.add_note(), "default_state": "disabled", "side": "right"}]
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
        for radiobtn in self.radiobuttons:
            if radiobtn['name'] == "Selected Polygon":
                radiobtn['widget']['state'] = 'normal'
                radiobtn['widget']['text'] = "Polygon ID: " + str(self.selected_polygon['id'])

    #Method for adding a note **CLEAN UP**
    def add_note(self):
        #Values: #note, username, year, scan_type if Slice, slice_name / patient, date, time #need to make below dynamic
        values_ready = []
        values = []
        note = self.notebox.read_contents()[:-1]
        if self.note_type.get() == 'Scan Type':
            values = [note, self.username, self.slice_info[7], self.slice_info[8], self.format_date_time()[0], self.format_date_time()[1]]
        elif self.note_type.get() == 'Current Slice':
            values = [note, self.username, self.slice_info[7], self.slice_info[8], self.slice_info[10], self.slice_name[:-1], self.format_date_time()[0], self.format_date_time()[1]]
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
            data = {"year": self.slice_info[7], "patient": self.slice_info[8], "scan_type": self.slice_info[10], "slices": []}
            for slice in self.slice_list:
                slice_name = {"name": slice}
                data['slices'].append(slice_name)

            note_details = [self.username, note, self.format_date_time()[0], self.format_date_time()[1]]
            filename = self.slice_info[7] + "-" +  self.slice_info[8] + "-" + self.slice_info[10] + '.json'
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
            data = {"year": self.slice_info[7], "patient": self.slice_info[8], "scan_type": self.slice_info[10], "slices": []}
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
                print("i made it in here")
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
                table = NoteTable(frame, col_settings, data, 665, 150, row_btns)

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

#Class for the table construction
class NoteTable:
    #table construction: https://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter
    def __init__(self, parent_frame, col_settings, data, width, height, row_btns):
        self.parent_frame = parent_frame
        self.col_settings = col_settings
        self.data = data
        self.row_btns = row_btns

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
                # wider_frame.grid(row=0, column=0, padx=20, pady=20)
                wider_frame.pack(side="top", padx=10, pady=10)

                #canvas is on the left hand side & scrollbar on the right
                canvas = tk.Canvas(wider_frame, height=height, width=width, bg=HEADER_BG, borderwidth=0, highlightthickness=0)  #create a canvas, canvas has the scrollbar functionality
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
                                # label.pack_forget()
                            else:
                                inner_cell_frame['background'] = "white"
                                label['background'] = "white"
                            #wraplength: https://stackoverflow.com/questions/16761726/label-break-line-if-string-is-too-big
                        col += 1
                    row += 1
                    #add the btns per row
                    # row_btns = ['Remove', 'Edit']
                    # row_btns = [{"name": "Remove", "text": "Remove", "function": None, "width": 7},
                    #         {"name": "Edit", "text": "Edit", "function": None, "width": 7},
                    #         ]
                    for btn in self.row_btns:
                        inner_cell_frame = tk.Frame(frame, bg="white", borderwidth=0)
                        inner_cell_frame.grid(row=row - 1, column=col, sticky="nswe", padx=1, pady=1)
                        data = []
                        data.append(entry[col_settings[0]['column']])
                        data.append(entry[col_settings[1]['column']])
                        # button = tk.Button(inner_cell_frame, text=btn['text'], width=btn['width'], command=lambda note = entry[col_settings[1]['column']], btn = btn: self.action_note(btn, note))
                        print(btn['function'])
                        button = tk.Button(inner_cell_frame, text=btn['text'], width=btn['width'], command = lambda data=data, function=btn['function']: function(data))
                        #https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda
                        button.pack(side="left", padx=1, pady=1)
                        col += 1

                canvas.create_window((0, 0), window=frame, anchor="nw") #position the canvas

                canvas.pack(side="left", fill="both", expand=True) #put the text frame on the left
                if scroll:
                    canvas.configure(yscrollcommand=scrollbar.set) #so it scroll only for canvas area
                    scrollbar.pack(side="right", fill="y") #put the scroller on the right hand side

    #     #function for creating a table
    # def create_table(self, parent_frame, col_settings, data):
    #     wider_frame = tk.Frame(parent_frame)
    #     # wider_frame.grid(row=0, column=0, padx=20, pady=20, sticky="NSWE")
    #     wider_frame.pack(side="top", padx=10, pady=10)
    #
    #     #canvas is on the left hand side & scrollbar on the right
    #     canvas = tk.Canvas(wider_frame, height=150, width=665)  #create a canvas, canvas has the scrollbar functionality
    #     scrollbar = ttk.Scrollbar(wider_frame, orient="vertical", command=canvas.yview) #add the scrollbar to the container
    #     #frame is the scrollable area
    #     frame = tk.Frame(canvas, bg="black")
    #     frame.bind( #function for ensuring the scrolling capacity is for all the text
    #         "<Configure>",
    #         lambda e: canvas.configure(
    #             scrollregion=canvas.bbox("all")
    #         )
    #     )
    #
    #     #create the table
    #     num_cols = len(col_settings)
    #     col = 0
    #     for column in col_settings:
    #         label = tk.Label(frame, bg="grey", fg="white", text=column['column'].capitalize(), borderwidth=0, width=column['width'])
    #         label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
    #         col += 1
    #     #configure the size of the table to ensure that spacing is provided equally and is not dependent on contents
    #     for column in range(num_cols):
    #         frame.grid_columnconfigure(column, weight=1)
    #
    #     #extra column for buttons
    #     buttons = ['adjust']
    #     for column in buttons:
    #         label = tk.Label(frame, bg="grey", fg="white", text=column.capitalize(), borderwidth=0, width=14)
    #         label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1, columnspan=2)
    #
    #     #to ensure that the button column is dependent on size of the buttons
    #     frame.grid_columnconfigure(col, weight=0)
    #
    #     #add the notes to the table
    #     row = 1
    #     for entry in data:
    #         col = 0
    #         for key, value in entry.items():
    #             inner_cell_frame = tk.Frame(frame, bg="white", borderwidth=0)
    #             label = tk.Label(inner_cell_frame, bg="white", text=value, borderwidth=0, wraplength=self.get_setting(key, col_settings, "wraplength"))
    #             #wraplength: https://stackoverflow.com/questions/16761726/label-break-line-if-string-is-too-big
    #             label.pack(side="left", padx=2, pady=2)
    #             inner_cell_frame.grid(row=row, column=col, sticky="nswe", padx=1, pady=1)
    #             col += 1
    #         row += 1
    #         #add the btns per row
    #         btns = ['Remove', 'Edit']
    #         for btn in btns:
    #             inner_cell_frame = tk.Frame(frame, bg="white", borderwidth=0)
    #             inner_cell_frame.grid(row=row - 1, column=col, sticky="nswe", padx=1, pady=1)
    #             button = tk.Button(inner_cell_frame, text=btn, width=7, command=lambda note = entry['note'], btn = btn: self.action_note(btn, note))
    #             #https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda
    #             button.pack(side="left", padx=1, pady=1)
    #             col += 1
    #
    #     canvas.create_window((0, 0), window=frame, anchor="nw") #position the canvas
    #     canvas.configure(yscrollcommand=scrollbar.set) #so it scroll only for canvas area
    #     canvas.pack(side="left", fill="both", expand=True) #put the text frame on the left
    #     scrollbar.pack(side="right", fill="y") #put the scroller on the right hand side

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

    def remove_entry(self, entry):
        pass


    def clear_table(self, frame):
        for child in frame.winfo_children():
            child.destroy()

    #This Class forms the TopLevelWin using the TopLevelWin template class - it is for editing a note

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
        self.button_dict = [{"name": "clear", "command": self.clear_txtbox, "side":"left", "default_state": "normal"},
                        {"name": "reset", "command": self.reset_txtbox,"side":"left", "default_state": "normal"}]

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

#Class for json filesaver
class jsonFileWriter:
    def __init__(self, filename, data, slice_name):
        self.filename = filename
        self.data = data
        # print("data pn load", self.data)
        self.slice = slice_name
        self.note_keys = ["user", "note", "date", "time"]

        #I have not done a try / except here but outside the class when the class is called instead as combines other methods
        needcreate = not os.path.exists(self.filename)
        if needcreate:
            # print("File needed to be created.")
            self.create_json_file(self.data) #create the file if one doesn't already exist

            if self.slice != None:
                self.transform_dict() #change the dictionary so it can accept notes


    def transform_dict(self):
        self.data['scan_type_notes'] = []
        for item in self.data['slices']:
            item['notes'] = []

    # function to create the json file - only do this once
    def create_json_file(self, data):
        with open(self.filename,'w') as f:
            # print(data)
            json.dump(data, f, indent=4)

    #function to append a note to the json file
    def format_note(self, note_details):
        #notedetails = [user_info, note_info, date_info, time_info]
        note = {}
        i = 0
        for item in self.note_keys:
            note[item] = note_details[i]
            i += 1
        # print(note)
        return note

    def append_note(self, note_details, note_type):
        #notedetails = [user, note, date, time]
        note = self.format_note(note_details)
        #read file
        current_data = self.read_file()
        #append the note to the position in the wider json
        if (note_type == "Scan Type"):
            current_data['scan_type_notes'].append(note)
        elif (note_type == "Current Slice"):
            print("NOTE DETAILS", note_details)
            # print("helloinside")
            for item in current_data['slices']:
                # print(item['name'])
                print(item['name'][:-4])
                print(self.slice)
                if item['name'][:-4] == self.slice:
                    print("ITS HERE MATE")
                    item['notes'].append(note)

        #create the json file  (it overwrites)
        self.create_json_file(current_data)

    #read the file
    def read_file(self):
        # print(self.filename)
        try:
            with open(self.filename) as f:
                currentdata = json.load(f)
                # print(currentdata)
            return currentdata
        except:
            # print("Error Reading File")
            return []


    def add_tag(self, data):
        self.create_json_file(data)

#Class for the Database
class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self, table_name, columns):
        conn = sqlite3.connect(self.db_name) #will create the db
        c = conn.cursor() #create the cursor

        query = """CREATE TABLE """ + table_name + """ ("""
        for column in columns:
            query += column['col_name'] + " " + column['col_type'] + ","
        query = query[:-1]
        query += """)"""
        c.execute(query)
        conn.commit() #commit changes
        conn.close() #close the connection to db

    def add_record(self, table_name, values, columns):
        print(values)
        print(columns)
        print(len(values))
        print(len(columns))

        if len(values) == len(columns):
            # try:
            conn = sqlite3.connect(self.db_name) #will create the db
            c = conn.cursor() #create the cursor

            query = "INSERT INTO " + table_name + " ("

            for column in columns:
                query += column['col_name'] + ", "
            query = query[:-2] + ")"
            query += " VALUES ("

            for value in values:
                query += value + ", "
            query = query[:-2] + ")"
            print(query)
            c.execute(query)

            conn.commit() #commit changes
            conn.close() #close the connection to db

            # except Exception as e:
            #     print(e)
        else:
            print("ERROR: Incorrect Number of Values Provided")

    def edit_record(self, table_name, values_to_be_updated, oid):
        #values_to_be_updated is a dict using the columns as keys
        #values_to_be_updated = [{column_name: column, new_val: value}, {column_name: column, new_val: value}] remember for same oid
        #UPDATE CRICKETERS SET AGE = 45 WHERE FIRST_NAME = 'Shikhar'
        if len(values) != len(columns):
            try:
                conn = sqlite3.connect(self.db_name) #will create the db
                c = conn.cursor() #create the cursor

                query = "UPDATE " + table_name + " SET "

                for new_val in values_to_be_updated:
                    query += new_val['column_name'] + " = " + new_val['new_val'] + ", "
                query = query[:-2] + "WHERE oid = " + oid

                c.execute(query)
                conn.commit() #commit changes
                conn.close() #close the connection to db

            except Exception as e:
                print(e)
        else:
            print("ERROR: Incorrect Number of Values Provided")

    def delete_record(self, table_name, oid):
        #delete record from the db using oid (presented on screen)
        try:
            conn = sqlite3.connect(self.db_name) #will create the db
            c = conn.cursor() #create the cursor
            query = "DELETE FROM " + table_name + " WHERE oid = " + oid
            c.execute(query)
            conn.commit() #commit changes
            conn.close() #close the connection to db
        except Exception as e:
            print(e)

    def delete_table(self, table_name):
        #delete table from the db
        try:
            conn = sqlite3.connect(self.db_name) #will create the db
            c = conn.cursor() #create the cursor
            query = "DROP TABLE " + table_name
            c.execute(query)
            conn.commit() #commit changes
            conn.close() #close the connection to db
        except Exception as e:
            print(e)

    def show_records(self, table_name):
        conn = sqlite3.connect(self.db_name) #will create the db
        c = conn.cursor() #create the cursor
        c.execute("SELECT *, oid FROM {}".format(table_name)) #oid is the primary key
        records = c.fetchall() #gets all the records

        conn.commit() #commit changes
        conn.close() #close the connection to db
        return records

#Custom Tooltip to match the other Matplotlib toolbar buttons
class ToolTip:
    #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
    def __init__(self, widget):
        self.widget = widget
        self.text, self.tipwindow = None, None

    def showtip(self, text):
        self.text = text
        x, y, cx, cy = self.widget.bbox("insert") #All 0 at this stage
        x = x + self.widget.winfo_rootx() + 26 #root of the widget on the x axis, 0 = left
        y = y + cy + self.widget.winfo_rooty() + 0 #root of the widget on the y axis, 0 = top
        self.tipwindow = tk.Toplevel(self.widget) #create toplevel widget
        self.tipwindow.wm_overrideredirect(1) #cannot be overrided = https://effbot.org/tkinterbook/wm.htm#wm.Wm.wm_overrideredirect-method
        self.tipwindow.wm_geometry("+%d+%d" % (x, y)) #geometry of toplevel widget
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                    background=HOVER_BG, relief=tk.SOLID, borderwidth=1,
                    font=SMALL_FONT) #styling
        label.pack(ipadx=3) #padding

    def hidetip(self):
            self.tipwindow.destroy()

# custom toolbar with changed hover text
class CustomToolbar(NavigationToolbar2Tk):
    #https://stackoverflow.com/questions/23172916/matplotlib-tkinter-customizing-toolbar-tooltips
    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ('Home', 'Reset Slice View', 'home', 'home'),
            ('Back', 'Previous Slice', 'back', 'back'),
            ('Forward', 'Next Slice', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'Configure Subplots', 'subplots', 'configure_subplots'), #subplots is not included in this figure
            ('Save', 'Save Slice', 'filesave', 'save_figure'),
            )
        NavigationToolbar2Tk.__init__(self, canvas_, parent_)


app = MainApp()
# app.geometry("1280x780") #x by y
app.mainloop()
