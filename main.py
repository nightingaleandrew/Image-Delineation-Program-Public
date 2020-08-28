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
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea
from matplotlib.figure import Figure
#image imports
from PIL import ImageTk, Image
from PIL import Image as PIL_image, ImageTk as PIL_imagetk

#classes
from window_classes import TopLevelWin, WindowLayout, ResizingCanvas
from widget_creator_classes import TextBox, InformationBox, ButtonCreator, Tab, NoteTable, ColourSquare, ToggledFrame, LoginFrame, HoverToolTip
from figure_custom_classes import cidPress, PolygonIntersector, CustomToolbar, PolygonHover, cidHover
from other_windows import PolygonSettings, EditNote, PolygonTagChanger

from button_images import custom_btn_images
from other import ConvertImages, TimeDate, StringMaker

#Files to be trimmed down
from json_file_adder import jsonNoteAdder, jsonNoteShow, jsonNoteEdit, jsonNoteDelete #adding data at different depths of a file after it has been read
from storage_classes import jsonFileWriter, Database, jsonFileReaderWriter



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
from check_json_files import SetSettings, TagFileLoader

settings_data_filename = r".\settings.json"
settings_file = SetSettings(settings_data_filename)
SETTINGS = settings_file.settings #These are the settings that are used for the program while it is live.

#Filename that contains the tags
TAGS_DATA_FILENAME = r".\tags.json"

#Main App that controls which frame or page is shown - either Start Page or Page One
class MainApp(tk.Tk):  #inherit tkinter methods from tk class inside tkinter
    def __init__(self, *args, **kwargs): #initialise the method
        tk.Tk.__init__(self, *args, *kwargs) #initalise tkinter
        tk.Tk.wm_title(self, "Dissertation Application - Andrew Nightingale") #seems like title works okay anyhow
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
        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        for f, geometry in zip((StartPage, PageOne), ('400x300+550+200', "1400x700+50+0")): #pages & their respective geometries
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

        self.window_layout = WindowLayout(self)
        self.header = self.window_layout.create_header("MRI Delineator", "top", LARGE_FONT)
        self.main = self.window_layout.create_main()

        # #header container
        # self.header = tk.Frame(self, bg=HEADER_BG)
        # self.header.pack(side="top", fill="both", expand=True)
        #
        # #page title
        # self.page_title =tk.Label(self.header, text="MRI Delineator", font=LARGE_FONT, fg=FONT_COL, bg=HEADER_BG)
        # self.page_title.pack(side="left", expand=True, fill="both", padx=(10, 10))

        #main container
        # self.main = tk.Frame(self, bg=MAIN_BG)
        # self.main.pack(side="bottom", fill="both", expand=True)

        #Login Frame
        self.login = LoginFrame(self, self.main, MAIN_BG, FONT_COL, PASSWORD)

        #Last User label
        self.last_user = tk.Label(self.main, bg=MAIN_BG, fg=FONT_COL)

    #Simple function that is called by the login frame as the parent is passed through if login is successfull
    def pass_through_login_frame(self, username):
         self.controller.show_frame(PageOne, username)

        #sendmsg function that passes info from A to B
    def sendmsg(self, msg ):
        self.last_user['text'] = "Last User: " + msg
        self.last_user.grid(row=2, column=1, pady=(0, 10), padx=10, sticky="N")

        self.login.reset_login_widgets() #resets the login widgets that were used using the login frame obj created in innit

#Class for the Page One where username is passed through & session begins
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #create the DB and tables if not present in dir - created when session starts so in PageOne
        self.setup_db() #this is done in the setup db method

        #widgets for main page
        self.window_layout = WindowLayout(self)
        self.header = self.window_layout.create_header("Delineate", "left", LARGE_FONT)

        #some styling
        headerstyle = ttk.Style(self.header)
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

        #Main Container
        # self.main_section = tk.Frame(master=self, bg=MAIN_BG)
        # self.main_section.pack(side="bottom", fill="both", expand=True)
        main_window = self.window_layout.create_main()

        vscrollbarframe = tk.Frame(main_window, bg="yellow")
        vscrollbarframe.pack(side="right", expand=False, fill="y")


        xscrollbarframe = tk.Frame(main_window, bg="blue")
        xscrollbarframe.pack(side="bottom", expand=False, fill="x")

        # create a canvas object and a vertical scrollbar for scrolling it

        canvas = tk.Canvas(main_window, bd=0, highlightthickness=0, bg=MAIN_BG)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor="nw")
        # canvas.grid(row=0, column=0)

        vscrollbar = tk.Scrollbar(vscrollbarframe, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        # vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        # vscrollbar.grid(row=0, column=1)

        xscrollbar = tk.Scrollbar(xscrollbarframe, orient=tk.HORIZONTAL)
        xscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)
        # xscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)
        # xscrollbar.grid(row=1, column=0)
        xscrollbar.config(command=canvas.xview, bg="yellow")
        vscrollbar.config(command=canvas.yview, bg="yellow")

        canvas.config(yscrollcommand=vscrollbar.set)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas, bg="green")
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
        #
        # canvas = tk.Canvas(self.main_section, bg="aqua", borderwidth=0, highlightthickness=0)  #create a canvas, canvas has the scrollbar functionality
        #
        # frame = tk.Frame(canvas, bg="brown", height=250, width=250) #frame is the scrollable area
        # frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) #function for ensuring the scrolling capacity is for all the text
        #
        # yscrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview) #add the scrollbar to the container on the y
        # xscrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview) #add the scrollbar to the container on the x
        #
        #
        #

        #title for the PageOne
        # self.page_title = tk.Label(self.header, text="Delineate", font=LARGE_FONT, foreground=FONT_COL, bg=HEADER_BG)      # Store this as an instance variable
        # self.page_title.pack(side="left", pady=10, padx=10)

        #Controls for quiting or heading back to Start Page
        self.header_btns = tk.Frame(master=self.header, bg=HEADER_BG)
        self.header_btns.pack(side="right", pady=10, padx=10)

        self.quit_btn = ttk.Button(self.header_btns, text="Quit", command=quit, width=12) #quits application
        self.quit_btn.grid(row=0, column=0, pady=(0, 10))

        self.close_session_btn = ttk.Button(self.header_btns, text="Close Session", command=lambda: self.controller.show_frame(StartPage, self.entry.get()), width=12) #closes the session & brings up the show_frame method of the controller.
        self.close_session_btn.grid(row=1, column=0)

        #Information for User currently on program
        self.session_info = InformationBox(self.header, "right", 2, "Current Session", None, HEADER_BG, FONT_COL, False)

        self.currently_viewing_frame = tk.Frame(self.header, bg=HEADER_BG) #for the information boxes
        self.currently_viewing_frame.pack(side="right")
        #
        # canvas.create_window((0, 0), window=frame, anchor="n") #position the canvas
        # # frame.pack(side="top", anchor="n")
        #
        # canvas.pack(side="left", fill="both", expand=True) #put the text frame on the left
        # # canvas.grid(row=0, column=0, sticky="NSEW")
        # # canvas.columnconfigure(0, weight=1)
        # canvas.configure(yscrollcommand=yscrollbar.set) #so it scroll only for canvas area for the y
        # canvas.configure(xscrollcommand=xscrollbar.set) #so it scroll only for canvas area for the x
        # yscrollbar.pack(side="right", fill="y") #put the scroller on the right hand side
        # xscrollbar.pack(side="bottom", fill="x") #put the scroller on the right hand side

        #load scans button frame (incs 2 load scans btns) & arrow btns (Close tabs & config settings also in the frame)
        self.browse_frame = tk.Frame(self.interior, bg=MAIN_BG)
        self.browse_frame.pack(side="top", fill="x")

        self.browse_frame.rowconfigure(0, weight=1)
        for i in range(3): #just create a 3
            self.browse_frame.columnconfigure(i, weight=1)

        #NOTEBOOK SETTINGS
        #Number of tab panes that are created
        self.num_notebooks = 2 #2 notebooks created at start

        self.notebook_frames = [] #contains all the notebooks with relevent info in a dict
        self.comparison_open = False #if two panes are being compared then is true, start with no comparisons
        self.current_figures = [] #contains all current figures for updating settings etc
        self.all_tabs = [] #contains all the Tab instances
        self.swap_tab_btns = [] #contains instances in a dict of the swap tab btns. Aswell as ButtonCreator class, it has left & right notebook instances for each to determine if there are any tabs open

        #Tab area for notebooks
        self.tab_area = tk.Frame(self.interior, background=MAIN_BG)
        self.tab_area.pack(side="bottom", fill="both", expand=True)

        #create the notebooks depending on number mentioned above
        for i in range(self.num_notebooks):
            notebook_frame = tk.Frame(self.tab_area, bg=MAIN_BG)

            if not self.comparison_open and i == 0:
                notebook_frame.grid(row=0, column=i, sticky="NSWE") #only grid out first frame
                self.tab_area.rowconfigure(0, weight=1) #set grid area so only one tab area if presented
                self.tab_area.columnconfigure(i, weight=1)
            elif self.comparison_open:
                 notebook_frame.grid(row=0, column=i, sticky="NSWE") #grid every frame if comparison open
                 self.tab_area.rowconfigure(0, weight=1) #all frames are on 0 row
                 self.tab_area.columnconfigure(i, weight=1) #columns would increase depending on comparison

            notebook = ttk.Notebook(notebook_frame) #instance of ttk.notebook
            notebook.pack(side="left", fill="both", expand=True, pady=(0, 10), padx=10)
            self.notebook_frames.append({"id": i, "parent_frame": notebook_frame, "notebook":notebook, "tabs": [], "slice_information": None}) #collect all frames together & notebooks inc current tabs & INformationBox obj

        for notebook in self.notebook_frames:
            notebook['notebook'].bind("<<NotebookTabChanged>>", lambda e, notebook=notebook: self.update_viewing_information(notebook)) #seems I have to do binding seperatly, when a tab is clicked, changes info in currently viewing
            #https://stackoverflow.com/questions/48104061/python-tkinter-bindtag-event-handling-how-to-update-which-tab-is-currently-sel

        #Frame for the controls & btns for loading stacks
        self.load_stacks_controls = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.load_stacks_controls.grid(column=0, row=0, sticky="NSWE")

        self.load_stacks_buttons_dict = []
        for i in range(self.num_notebooks):
            name = "load a stack (tab " + str(i + 1) +")" #load a stack for a particular notebook
            state = "normal" #first btn is normal
            comparison = False #no comparison with first button
            if i > 0:
                state = "disabled" #further comparison btns disabled
                comparison = True #comparisons onwards - used in load_scans method
            self.load_stacks_buttons_dict.append({"name": name, "command":lambda notebook_frame = self.notebook_frames[i], comparison=comparison: self.load_scans(notebook_frame, comparison), "default_state": state, "side":"left", "width":25})

        self.load_stacks_buttons = ButtonCreator(self.load_stacks_controls, self.load_stacks_buttons_dict) #create btn using ButtonCreator

        #For other buttons like Polygon Settings, Close Tabs
        self.other_btns_frame = tk.Frame(self.browse_frame, bg=MAIN_BG)
        self.other_btns_frame.grid(column=2, row=0, sticky="NSWE")

        self.other_btns_dict = [{"name": "polygon settings", "command":lambda  function=self.open_settings_config: function(), "default_state": "normal", "side":"right", "width":15},
                                {"name": "close all tabs", "command":lambda function=self.remove_tabs: function(), "default_state": "disabled", "side":"right", "width":15}]
        self.other_btns = ButtonCreator(self.other_btns_frame, self.other_btns_dict) #create arrow buttons

    #GENERAL METHODS
    #Method for setting up the Database if needed when a new session starts
    def setup_db(self):
        if MAKE_DB:
            needcreate = not os.path.exists('./' + DB_NAME)
            if needcreate:
                db = Database(DB_NAME)
                for table in TABLES:
                    db.create_table(table['table_name'], table['columns'])

    #Function that is called when the session is closed
    def destroyFrame(self, StartPage, username):
        self.hard_reset_settings() #reset to defaults
        self.remove_tabs() #removes the tabs & sets back settings back to start eg. comparison
        self.controller.show_frame(StartPage, username) #Head back to the start page

        if self.session_info != None:
            self.session_info.present_no_value() #allows the session info box to overwritten with no values so the new values can take place without looking like they are above previous

    #Function is called by the "owner" of PageOne, MainApp, which can pass messages for us
    def sendmsg(self, username):
        #update the information box that displays the session information
        session_information = {"user": username, "start time": TimeDate().get_time_stamp()} #call time to get current time this is called
        self.session_info.create_insides(session_information)

        self.close_session_btn.destroy() #Need to destroy current close session btn
        self.close_session_btn = ttk.Button(self.header_btns, text="Close Session", command=lambda: self.destroyFrame(StartPage, username), width=12)
        self.close_session_btn.grid(row=1, column=0)

    #When the session is closed the settings are hard reset to their default values
    def hard_reset_settings(self):
        for item in SETTINGS:
            item['current_value'] = item['default_value']
            item['temp_value'] = None

    #NOTEBOOK & TAB METHODS
    #Function that creates a tab
    def create_tab(self, slice_address, notebook_frame, folder_dir, sibling_slices):
        self.figure_information = {"year":slice_address[7], "scan type":slice_address[10], "patient":slice_address[8]} #figure information for the figure, get this from json?

        #Figure Information Box: Currently Viewing
        if notebook_frame['slice_information'] != None: #if figure information box already there then replace with new
            notebook_frame['slice_information'].make_box_go_walkies()#forget the sliceinfo box so a new one can be added. Or could use refresh method
        notebook_frame['slice_information'] = InformationBox(self.currently_viewing_frame, "left", 2, "Currently Viewing Tab " + str(notebook_frame['id'] + 1), self.figure_information, HEADER_BG, FONT_COL, True) #assigns the information contents

        #Creation of Tab & storing of Tab
        tab_obj = Tab(notebook_frame['notebook'], HEADER_BG)  #create tab objs
        tab_pane = tab_obj.add_tab(StringMaker().title_formatter(self.figure_information)) #create tab pane
        self.all_tabs.append({"parent_frame": notebook_frame['parent_frame'], "tab_obj": tab_obj, "tab_pane_frame":tab_pane}) #add tab to all tabs list

        #TAB ID METHOD: Simple non duplicate tab id functionality (for swapping tabs)
        if len(notebook_frame['tabs']) > 0:
            tab_id = notebook_frame['tabs'][-1]['id'] + 1 #always add one to the last one & therefore never have a duplicate
        else:
            tab_id = 1
        notebook_frame['tabs'].append({"id":tab_id, "tab_obj": tab_obj, "tab_pane_frame":tab_pane, "tab_figure_slice_address": slice_address, "tab_figure_info": self.figure_information, "folder_dir": folder_dir, "sister_slices": sibling_slices}) #add tab to particular notebook's frame

        #FIGURE CREATION
        print("create tab", self.session_info.pull_detail('User'))
        figure = SliceFigure(tab_pane, folder_dir,  sibling_slices, self.session_info.pull_detail('user'), self.figure_information, self) #creates the figure for the tab
        self.current_figures.append(figure) #append so all figures stored for settings usage

    #Method for adding a new comparison frame if comparison wanted
    def add_comparison_frame(self):
        if self.comparison_open == False:
            self.tab_area.rowconfigure(0, weight=1)
            for i in range((len(self.notebook_frames))):
                self.notebook_frames[i]['parent_frame'].grid(row=0, column=i, sticky="NSWE")
                self.tab_area.columnconfigure(i, weight=1)
                if i >= 1:
                    swap_btn_frame = tk.Frame(self.browse_frame, bg=MAIN_BG)
                    swap_btn_frame.grid(column=1, row=0, sticky="NSWE") #THIS IS NOT DYNAMIC
                    arrow_btn_dict = [{"name": "<", "command":lambda side = "left", to_pane = self.notebook_frames[i], from_pane = self.notebook_frames[i - 1]: self.swap_tab(side, to_pane, from_pane), "default_state": "normal", "side":"left", "width":5},
                                    {"name": ">", "command":lambda side = "right", to_pane = self.notebook_frames[i - 1], from_pane = self.notebook_frames[i]: self.swap_tab(side, to_pane, from_pane), "default_state": "normal", "side":"left", "width":5}]
                    arrow_btns = ButtonCreator(swap_btn_frame, arrow_btn_dict) #create arrow buttons
                    self.swap_tab_btns.append({"button_class": arrow_btns, "left_hand_frame": self.notebook_frames[i - 1], "right_hand_frame": self.notebook_frames[i]})

            self.comparison_open = True
            self.swap_tab_btn_status_changer() #disable the btn going right if only one tab in the left hand pane

        elif self.comparison_open == True:
            self.reset_to_one_tab() #reset the screen to one notebook, self.comparison_open is set to false in here

            for arrow_btns in self.swap_tab_btns: #forget the arrow buttons
                arrow_btns['button_class'].forget_btns()

            # self.comparison_open = False

    #Function that loads up a folder of slices in a new tab
    def load_scans(self, notebook_frame, comparison):
        folder_selected = tk.filedialog.askdirectory(initialdir = DIRECTORY, title = "Browse files for a stack of Numpy Arrays") #browse directories
        numpy_files = []
        for item in os.listdir(folder_selected):
            if item.endswith('.npy'): #has to be a numpy file
                numpy_files.append(str(item)) #store all the numpy files to pass through
        if len(numpy_files) > 0: #if there are numpy file options in the folder
            slice_address_segments = re.split("/", folder_selected) #split directory address

            self.create_tab(slice_address_segments, notebook_frame, folder_selected, numpy_files)  #create the tab with the segements from the file

            #**MAKE DYNAMIC**
            if comparison == True and len(notebook_frame['tabs']) == 1:
                self.add_comparison_frame()
            ##**

            self.other_btns.enable_btn("close all tabs") #enable close btn
            self.unlock_comparison_stacks_btn()
        else:
            messagebox.showerror("Error Loading MRI Slices", "There are no Numpy Array Files available within this folder.") #there were no numpy arrays in the folder

    #Function to remove all tabs
    def remove_tabs(self):
        if len(self.all_tabs) > 0:
            for tab in self.all_tabs:
                tab['tab_pane_frame'].destroy() #destroy each tab frame

        self.all_tabs.clear()  #clear the tabs list

        for notebook in self.notebook_frames: #clear all tabs from notebooks
            notebook['tabs'].clear()
            if notebook['slice_information'] != None:
                self.remove_and_nullify_slice_information(notebook)

        self.comparison_open = False #There is no comparison window open
        self.other_btns.disable_btn("close all tabs") #disable close btn as no tabs to close
        self.comparison_open = True #Needs to be True even if there are no comparisons open as will reset screen to just one grid column
        self.unlock_comparison_stacks_btn() #to lock the comparison btn
        self.add_comparison_frame() #to change the setup of the screen
        self.current_figures.clear() #as no current figures

    #Updates the viewing information in the Information Box for each slice
    def update_viewing_information(self, notebook):
        #There has to be a tab in existence
        if len(notebook['tabs']) > 1:
            text = notebook['notebook'].tab(notebook['notebook'].select(), "text") #https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook
            text = re.split(" | ", text) #get the name of the tab from the notebook
            #change currently viewing on tab select not load of scans
            figure_information = {"year": text[0], "scan type": text[2], "patient":text[4]}
            notebook['slice_information'].refresh_information(figure_information) #refresh the information for the notebook box

    #Function for unlocking the comparison stacks buttons, currently unlocks all
    def unlock_comparison_stacks_btn(self):
        if len(self.all_tabs) > 0:
            self.load_stacks_buttons.enable_all_btns() #load comparison button is now enabled
        else:
            self.load_stacks_buttons.change_to_default_states() #load comparison stacks button goes back to disabled, load stack to normal

    #Function that looks to swap a tab from one notebook to another & updates relevent lists
    def swap_tab(self, direction, current_notebook, destination_notebook):
        #Cannot just swap tab over as cannot change parent frame in tkinter. I tried creating a change_notebook functionality in tab!
        tab_index = current_notebook['notebook'].index("current") #get the current index of the tab in the notebook which will be the same as the tabs list for notebook in dict
        tab = current_notebook['tabs'][tab_index] #get that tab dict which will contain the id
        tab_id = tab['id'] #get id of tab

        self.create_tab(tab['tab_figure_slice_address'], destination_notebook, tab['folder_dir'], tab['sister_slices']) #create new tab

        current_notebook['notebook'].forget(current_notebook['notebook'].select()) #remove the tab from the notebook
        current_notebook['tabs'] = [item for item in current_notebook['tabs'] if item['id'] != tab_id] #remove the tab if it has the same id

        #Button & grid styling depending on direction
        #**NEED TO MAKE DYNAMIC - only allow the right to left btn active if btn in left hand
        self.swap_tab_btn_status_changer()
        ##**

        #forget the information box if no tabs in
        for notebook_frame in self.notebook_frames:
            if (notebook_frame['slice_information'] != None) and len(notebook_frame['tabs']) == 0:
                self.remove_and_nullify_slice_information(notebook_frame)

    #Function that resets the screen to one notebook, of course, comparison open would be set to false
    def reset_to_one_tab(self):
        for i in range((len(self.notebook_frames))):
            if i == 0:
                self.tab_area.columnconfigure(i, weight=1)
            if i > 0:
                self.notebook_frames[i]['parent_frame'].grid_forget()
                self.tab_area.columnconfigure(i, weight=0) #second one has to be weight 0 & has to be stated
        self.comparison_open = False # comparison is now false as there are no frames on the right hand side

    #A function that changes the swap tb button status according to number of tabs open in each notebook
    def swap_tab_btn_status_changer(self):
        for btns in self.swap_tab_btns:
            if len(btns['right_hand_frame']['tabs']) == 0: #if there are no tabs open in right hand notebook then reset to one notebook
                btns['button_class'].forget_btns() #forget the comparison buttons as not needed as only one notebook open
                self.reset_to_one_tab() #reset the screen to just one notebook
            elif len(btns['left_hand_frame']['tabs']) == 1: #if there is 1 tab in left hand frame then prevent moving this to the right
                btns['button_class'].disable_btn(">")
            elif len(btns['left_hand_frame']['tabs']) > 1: #if there is >1 tab open in left hand frame then allow this to move to right
                btns['button_class'].enable_btn(">")

    #OTHER METHODS
    #Function that refreshes the tabs with the new settings
    def open_settings_config(self):
        result = PolygonSettings(SETTINGS).send() #create Settings class
        if result and len(self.current_figures) > 0: #if there are current figures and there was a True response from exiting the Settings Window (means there was a change made)
            self.refresh_figures() #refresh all figures

    #This is used to refresh the slice figure class for settings that are configuable. I don't delete the tab due to UX comfort
    def refresh_figures(self):
        for figure in self.current_figures:
            figure.refresh() #call refresh method in below class

    #Just a quick method that removes the slice_information box & replaces the value with None
    def remove_and_nullify_slice_information(self, notebook_frame):
        notebook_frame['slice_information'].make_box_go_walkies()
        notebook_frame['slice_information'] = None

    #Synchronising the tabs and unsynchronising the tabs
    def sync_tabs(self, figure_information):
        for figure in self.current_figures:
            #don't sync tabs if they are the same scan type of the same patient
            if (figure.figure_information['patient'] == figure_information['patient'] and figure.figure_information['year'] == figure_information['year']):
                figure.sync_btn['text'] = 'Tab Synced'
                figure.sync_btn['background'] = "red"
                figure.sync_btn['foreground'] = "white"
                figure.sync_tooltip.change_hover_text("Remove Sync")

                figure.synchronised_status = True
    def unsync_tabs(self, figure_information):
        for figure in self.current_figures:
            if (figure.figure_information['patient'] == figure_information['patient'] and figure.figure_information['year'] == figure_information['year']):
                figure.sync_btn['text'] = 'Synchronise'
                figure.sync_btn['background'] = "light gray"
                figure.sync_btn['foreground'] = "black"
                figure.sync_tooltip.change_hover_text("Sync Stacks\nPatient: " + figure_information['patient'])

                figure.synchronised_status = False

#Class for the Figure generated by selecting a folder
class SliceFigure:
    def __init__(self, tab_frame, folder_selected, slice_list, username, figure_information, parent):
        self.frame = tab_frame #the frame of the tab where the Figure is placed
        self.folder_selected  = folder_selected #directory information of the folder selected
        self.slice_list = slice_list #slices of the sibling in the folder, for interating over by button
        self.username = username #username of individual in session
        self.figure_information = figure_information #figure information eg. patient/scan type/year
        self.parent = parent #parent frame passed through

        self.current_position = 0 #Current position for the slice. Tab always begins at 0
        self.intro_label_frm_txt = "Stack: " #intro text to the label frame
        self.synchronised_status = False #This is changed if the figure is synced
        self.slice_name = self.current_slice_name_getter() #current slice name - in text of label frame when tab loads, changed by arrow btns through slice stack
        self.selected_polygon = None #this is updated by child classes such as Polygons to then let Notebox know that a polygon is selected

        #start off settings that can be changed
        self.settings = SETTINGS
        self.figure_background = self.get_setting("Figure Background") #the current figure background setting - colour hex value
        self.default_tag_index = self.get_setting("Default Tag") #the index of the current tag in the tag list

        #FRAME inc HEADER & GRAPH
        self.graph_frame = tk.Frame(self.frame, background=HEADER_BG)
        self.graph_frame.pack()

        #HEADER
        #Frame includes the dropdown & the information labels
        self.graph_frame_header = tk.Frame(self.graph_frame, background=HEADER_BG)
        self.graph_frame_header.pack(side="top", fill="x", padx=10, pady=10)

        for i in range(3): #split out the header of the figure
            self.graph_frame_header.grid_columnconfigure(i, weight=1) #evenly space out the labels

        #Sub frame containing the label & tag drop down
        self.polygon_tag_frame = tk.Frame(self.graph_frame_header, background=HEADER_BG)
        self.polygon_tag_frame.grid(row=0, column=0, sticky="W")

        self.polygon_tag_var = tk.StringVar(self.frame)
        self.polygon_tags = self.load_tags() #load the current tags

        self.polygon_tag_var.set(self.polygon_tags[self.default_tag_index])
        self.polygon_tag_chosen = self.polygon_tag_var.get() #assign variable to default

        self.polygon_tag_lab = tk.Label(self.polygon_tag_frame, text="Tag: ", background=HEADER_BG, fg=FONT_COL) #current assigned tag for drawing, can be changed by default in settings
        self.polygon_tag_lab.grid(row=0, column=0, sticky="W")

        self.polygon_tag_choice = ttk.Combobox(self.polygon_tag_frame, values=self.polygon_tags) #Use ttk. combo box as looks more appealing
        self.polygon_tag_choice.current(self.default_tag_index) #current value in the combo box
        self.polygon_tag_choice.grid(row=0, column=1, sticky="W", padx=5)

        self.polygon_tag_choice.bind("<<ComboboxSelected>>", self.change_tag) #when the tag changed, reassign the variable for the tag

        #information label, updated throughout depending on actions
        self.information = tk.Label(self.graph_frame_header, background=HEADER_BG)
        self.information.grid(row=0, column=1, sticky="W")

        self.sync_btn = tk.Button(self.graph_frame_header, text="Synchronise", command=self.synchronise)
        self.sync_btn.grid(row=0, column=2, sticky="E", padx=10)
        self.sync_tooltip = HoverToolTip(self.sync_btn, HOVER_BG, SMALL_FONT, "Sync Stacks\nPatient: " + self.figure_information['patient'])

        #GR
        #Graph Frame - label frame containing the figure & toolbar
        self.fig_frame = tk.LabelFrame(self.graph_frame, text="  {} {} ".format(self.intro_label_frm_txt, self.slice_name), background=HEADER_BG, foreground=FONT_COL)
        self.fig_frame.pack(padx=10, pady=(0, 10))
        #The inner frame changes according to figure_background setting to offer some top & bottom padding to the figure (I have changed the fig size to save space but it removes all top/bottom padding)
        self.fig_frame_inner = tk.Frame(self.fig_frame, background=self.figure_background)
        self.fig_frame_inner.pack()

        #FIGURE, AXIS, CANVAS
        self.figure = Figure()
        self.a = self.figure.add_subplot(111) #only one chart

        self.figure.patch.set_facecolor(self.figure_background) #patches the facecolour of the figurebackground #https://stackoverflow.com/questions/60480832/how-to-put-color-behind-axes-in-python
        self.figure.subplots_adjust(left=0,right=1,bottom=0,top=1) #This reduces the size of the figure somewhat #https://stackoverflow.com/questions/20057260/how-to-remove-gaps-between-subplots-in-matplotlib


        self.canvas = FigureCanvasTkAgg(self.figure, self.fig_frame_inner) #would normally run plot.show() but show in tkinter window here
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10) #pack it to the window
        self.fc = cidPress(self.figure) #class of cid for watching for button clicking

        self.cidHover = cidHover(self.figure)

        #TOOLBAR
        self.toolbar = CustomToolbar(self.canvas, self.fig_frame) # self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame) = I have used a CustomToolbar
        self.toolbar.config(background=HEADER_BG) #change background of the toolbar
        self.toolbar.update() #toolbar needs updating as changes made. See CustomToolbar class
        self.figure.canvas.mpl_connect('figure_leave_event', self.leave_figure) #I put in a fig leave event as I have adjusted the self.mode & set message#https://stackoverflow.com/questions/48351630/how-do-you-set-the-navigationtoolbar2tkaggs-background-to-a-certain-color-in-tk
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.toolbar.children['!button6'].pack_forget() #to forget the configure subplots button as not needed

        # toolbar_buttons = [{"left_arrow":"!button2", "right_arrow":"!button3", "pan":"!button4", "zoom":"!button5", "subplots":"!button6", "save":"!button7"}] #recorded for my own use
        #can do self.toolbar.children["!button2"].config(background="red") to change background but img placed on top

        #Custom Buttons Frame in toolbar - incs buttons like edit & draw
        custom_btn_frame = tk.Frame(master=self.toolbar, background=HEADER_BG)
        custom_btn_frame.pack(side = "left")

        #Custom Buttons stored in a dict with name, function, default state
        self.custom_btns = [{"name": 'Jump to First Slice', "text": "1", "padding": (5, 1), "description": 'start', "dlft_state": "normal", "command": lambda name="start": self.click_tb_btn('start')},
                            {"name": 'Jump to Last Slice', "text": "END", "padding": (1, 2), "description": 'end', "dlft_state": "normal", "command": lambda: self.click_tb_btn('end')},
                            {"name": 'Play Slice Slideshow', "text": "PLY", "padding": (5, 5), "description": 'play', "dlft_state": "normal", "command": lambda: self.click_tb_btn('play')},
                            {"name": "Draw Polygon", "text": "DRW", "padding": (0, 2), "description": 'draw', "dlft_state": "normal", "command": lambda name="draw": self.click_tb_btn("draw")},
                            {"name": "Select Polygon", "text": "SEL", "padding": (0, 2), "description": 'select', "dlft_state": "disabled", "command": lambda name="select": self.click_tb_btn("select")},
                            {"name": "Edit Polygon", "text": "EDIT", "padding": (0, 2), "description": 'edit', "dlft_state": "disabled", "command": None},
                            {"name": "Delete Polygon", "text": "BIN", "padding": (0, 2), "description": 'delete', "dlft_state": "disabled", "command": None},
                            {"name": "Hide Polygons", "text": "ON", "padding": (0, 2), "description": 'hide', "dlft_state": "normal", "command": lambda name="hide": self.click_tb_btn("hide")},
                            {"name": "Edit Polygon Tag", "text": "TAG", "padding": (0, 2), "description": 'edit_tag', "dlft_state": "disabled", "command": None},
                            {"name": "Refresh Polygons", "text": "REF", "padding": (0, 2), "description": 'refresh', "dlft_state": "normal", "command": lambda name="refresh": self.click_tb_btn("refresh")}
                            ]
        #create the images for the buttons, uses PIL - look at widget_creator_classes file
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
            if btn['image'] != None: #if it's none then the image was not able to be loaded
                button = tk.Button(master=custom_btn_frame, image=btn['image'], command=btn['command'], state = btn['dlft_state'], width=24, height=24) #height & width same as standard
                btn['show_image'] = True
            else:
                print("ERROR with loading an image for toolbar button {}, text used instead.".format(btn['name']))
                button = tk.Button(master=custom_btn_frame, text=btn['text'], command=btn['command'], state = btn['dlft_state'] ) #height & width seem to make it play up
                btn['show_image'] = False
            btn['widget'] = button
            btn['hover_tooltip'] = HoverToolTip(button, HOVER_BG, SMALL_FONT, btn['name'])
            button.grid(row=0, column=i, padx=btn['padding'])
            i += 1 #https://stackoverflow.com/questions/47212078/tkinter-how-to-replace-a-button-with-a-image #I don't use text for these btns but use images

        #load up First Figure
        self.create_figure(self.fig_frame)

        #Following is for Play/Pause functionality
        self.pause = False
        self.clicked = 0

        #Notebox Class is called to make this appear when calling Slice Figure
        self.notebox = Notebox(self.frame, self.username, self.current_slice_name_getter(), self.figure_information, self.folder_selected, self.slice_list)
        #Instance of Json File Writer
        self.filename = self.folder_selected + "/" + self.current_slice_name_getter() + "_polygon_slice_notes.json"
        self.jsonFileReaderWriter = jsonFileReaderWriter(self.filename, 'polygon data')
        #Instance of Polygons upon the Slice
        self.slice_polygons = Polygons(self.jsonFileReaderWriter, self.current_slice_name_getter(), self.figure, self.a, self.custom_btns, self.fc, self.information, self)

    #FIGURE METHODS
    #Creates figure every time the user clicks the arrow buttons to change the slice
    def create_figure(self, graph_frame):
        self.fig_frame['text'] = "  {} {} ".format(self.intro_label_frm_txt, self.current_slice_name_getter()) #update label frame text for when slice changes

        self.reset_axis() #reset the axis, set grid off, axes off, clear axes etc for new slice (so slices don't sit on top of each )

        #Pull figure & use slice list
        slice_address = self.folder_selected + "/" + self.slice_list[self.current_position]
        slice = np.load(slice_address) #load the figure
        self.a.imshow(np.squeeze(slice), cmap='gray') #show the fig in monochrome

        self.filename = self.folder_selected + "/" + self.current_slice_name_getter() + "_polygon_slice_notes.json" #filename for json data on polygons & polygon notes & also slice notes
        self.jsonFileReaderWriter = jsonFileReaderWriter(self.filename, 'polygon data') #recall jsonfilewriter instance
        self.slice_polygons = Polygons(self.jsonFileReaderWriter, self.current_slice_name_getter(), self.figure, self.a, self.custom_btns, self.fc, self.information, self)

        self.canvas.draw() #canvas.show does not work anymore. Redraw the canvas with new base figure
        self.determine_btn_status() #status of standard btns in matplotlib toolbar, eg. if slice was first in stack then disable left arrow btn

    #Function is for leaving the figure cursor, to let self.mode & self.setmessage of CustomToolbar know - see CustomToolbar class
    def leave_figure(self, event):
        self.toolbar.left_figure(event)

    #Function to draw the figure
    def draw_figure(self, figure):
        figure.canvas.draw()


    #TAG METHODS
    #Function that loads tags using the TagFileLoader
    def load_tags(self):
        polygon_tags = []

        tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        tags = tags_writer.return_tags()

        for tag in tags:
            polygon_tags.append(tag['label'].capitalize())

        return polygon_tags

    #Function that sets the default tag for speed of user
    def set_default_tag(self, default):
        if type(default) == str:
            if default in self.poylgon_tags:
                return self.polygon_tags.index(tag)
            else:
                return 0
        elif type(default) == int:
            return default

    #Called when the tag is changed, this is bound to the dropdown, ensures correct current tag is passed through
    def change_tag(self, event):
        self.polygon_tag_chosen = self.polygon_tag_choice.get()


    #BUTTON METHODS
    #Button that is called everytime a toolbar button is clicked
    def click_tb_btn(self, btn):
        self.fc.disconnect() #disconnect the CID - see figure classes for cid
        if btn == 2 or btn == 3 or btn == "start" or btn == "end": #change figure
            if btn == 2: #2 is left
                self.current_position -= 1 #postion is decrememented
            elif btn == 3: #3 is right
                self.current_position += 1 #postion is incremented
            elif btn == "start":
                self.current_position = 0
            elif btn == "end":
                self.current_position = len(self.slice_list) - 1
            self.create_figure(self.fig_frame) #create figure
            self.notebox.update_slice_name(self.current_slice_name_getter()) #update slice name of notebox with new slice name

        elif btn == "play":
            self.play_slideshow() #play the slideshow method
        elif btn == "draw":
            self.fc.connect(lambda event: self.slice_polygons.draw_btn_click(event, self.polygon_tag_chosen)) #click to draw
        elif btn == "select":
            self.fc.connect(lambda event: self.slice_polygons.select_polygon(event)) #click to select a polygon
        elif btn == "hide":
            self.fc.connect(self.slice_polygons.show_polygons()) #shows polygons or removes from view
        elif btn == "refresh":
            self.fc.connect(self.slice_polygons.load_polygons()) #load polygons just refreshs the polygons on the slice, incomplete polygons are not saved to json

    #Method to determine the status of the standard Matplotlib toolbar btns
    def determine_btn_status(self):
        start_btn = self.custom_btns[0]['widget'] #to start btn
        end_btn = self.custom_btns[1]['widget'] #to end btn
        if self.current_position == 0: #disable left as cannot go left as current position is at start
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="disabled")
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="normal")
            start_btn['state'] = "disabled"
            end_btn['state'] = "normal"
        elif (self.current_position == len(self.slice_list) - 1): #disable right as cannot go right as current position is at end
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="normal")
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="disabled")
            start_btn['state'] = "normal"
            end_btn['state'] = "disabled"
        else:   #in middle of stack
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="normal")
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="normal")
            start_btn['state'] = "normal"
            end_btn['state'] = "normal"

    #Method that plays the slideshow without any polygons
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

    #passes figure_information from the class where the sync was made up
    def synchronise(self):
        if not self.synchronised_status:
            self.parent.sync_tabs(self.figure_information)
        else:
            #unsync
            self.parent.unsync_tabs(self.figure_information)

    #OTHER METHODS
    #Function that refreshes the slice figure if a setting is changed through config settings
    def refresh(self):
        self.settings = SETTINGS
        #figure background change
        self.figure_background = self.get_setting("Figure Background")
        self.figure.patch.set_facecolor(self.figure_background) #doesn't need canvas draw, resets colour
        self.fig_frame_inner['background'] = self.figure_background #sets background of the inner frame

        #Refresh the tags
        self.default_tag_index = self.get_setting("Default Tag")
        self.polygon_tag_var.set(self.polygon_tags[self.default_tag_index]) #set the value to the variable
        self.polygon_tag_choice.current(self.default_tag_index) #set the current value of the combo box
        self.change_tag(None) #need to then reassign this as the current tag is changed

        #load polygons
        self.slice_polygons.load_polygons() #reloads the polygons

        #load new tags & assign to dropdown
        self.polygon_tag_choice['values'] = self.load_tags()

    #Function called by child class Polygons to let this class know which polygon is selected to then update Notebox
    def get_selected_polygon(self, polygon):
        self.selected_polygon = polygon #reassign polygons
        self.notebox.set_selected_polygon(polygon) #set it in notebox so notebox can allow a note to be taken for a selected polygon

    #Function for updating the information label depending on type of message eg. positive or negative
    def update_information(self, text, type):
        self.information['text'] = text
        if type == "positive":
            self.information['fg'] = "green"
        elif type == "warning":
            self.information['fg'] = "red"
        else:
            self.information['fg'] = "black"

    #Get setting method pulls a setting from self.settings & gets the current value
    def get_setting(self, setting_name):
        return [item['current_value'] for item in self.settings if item['setting'] == setting_name][0]

    #Function that pulls the current slice name from the slice stack & trims off the .npy off the end
    def current_slice_name_getter(self):
        return self.slice_list[self.current_position][:-4]

    def update_hover(self, class_obj):
        # self.disconnect()
        self.cidHover.disconnect()
        self.cidHover.connect(lambda e: class_obj.hover(e))
        # self.figure.canvas.mpl_connect('motion_notify_event', lambda e: class_obj.hover(e)) #calls hover method on the motion notify event, do not need to change the hover class

    def reset_axis(self):
        self.a.cla()
        self.a.grid(False) #remove grid lines
        self.a.axis("off") #removes axis
        self.a.format_coord = lambda x, y: "[{}, {}]".format(str(x)[:4], str(y)[:4]) #https://stackoverflow.com/questions/36012602/disable-coordinates-from-the-toolbar-of-a-matplotlib-figure

        pass

#Class for the polygons upon the Slice Figure
class Polygons(SliceFigure):
    def __init__(self, file_writer, slice_name, f, a, polygon_buttons, cid, information_label, parent):
        #Tag Checker & pull tags
        self.refresh_tags()

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

        self.figure = f
        self.axis = a
        self.fc = cid

        self.polygon_buttons = polygon_buttons
        self.information = information_label
        self.parent = parent
        self.load_polygons()

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
        if file_info != None:
            file_sorted = self.file_writer.sort_file(file_info, "slice", self.slice_name)
        else:
            file_sorted = []

        self.refresh_tags()
        #only pull polygons of certain slice name
        slice_polygons = []
        for polygon in file_sorted:
            if polygon['slice'] == self.slice_name:
                slice_polygons.append(polygon)

        #clear axis & polygon info as this will be reset - different number of polygons for next slice
        self.clear_axis_data()

        #To clear any unfinished polygons
        self.num_of_lines = 0
        self.polygon_num = 0 #IDs the polygons for that are drawn - need to be taken from json file
        self.polygons_visible = True #Polygons always visible after load
        self.polygon_info.clear() #clear all polygon info
        self.co_ordinates.clear() #clear lines so there are not any surprising lines if the user started to draw and then stopped

        self.fc.disconnect() #disconnect from the cid just in case a draw btn was clicked or something similar

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

            print("POLYGON INFO", self.polygon_info)
            #draw to figure
            self.draw_figure()

        else:
            #no polygons are present for this slice
            # print("No Polygons Present for this Slice")
            pass

        self.check_if_polygons_present() #if polygons present then select button is enabled
        self.check_polygon_selected() #if no polygon selected then edit/remove btns disabled
        self.selected_polygon = None #no selected polygon currently
        self.update_information("Click Draw to create a polygon!", "positive") #information line

        hovering_work = PolygonHover(self, self.polygon_info, self.precision, self.figure, self.axis, self.select_col) #calling the hover class
        self.parent.update_hover(hovering_work)

        for button in self.polygon_buttons:
            if button['description'] == "hide":
                button['hover_tooltip'].change_hover_text(button['name']) #change text in tooltip to display that polygons will be shown
                if not button['show_image']:
                    button['widget']['text'] = button['text'] #change the text for show polygons btn if the image is not used


    def get_selected_polygon(self):
        # super(Polygons, self).get_selected_polygon(self.selected_polygon)
        self.parent.get_selected_polygon(self.selected_polygon)

    #A function to show/remove from view polygons, I do call the json to show so they cannot switch here and there if polygon is half complete
    def show_polygons(self):
        self.fc.disconnect() #disconnect from the cid just in case a draw btn was clicked or something similar
        if self.polygons_visible:
            for button in self.polygon_buttons:
                if button['description'] == "hide":
                    button['hover_tooltip'].change_hover_text("Show Polygons") #change text in tooltip to display that polygons will be shown
                    if not button['show_image']:
                        button['widget']['text'] = 'OFF' #change the text for show polygons btn if the image is not used
                else:
                    button['widget']['state'] = "disabled" #disable all other buttons if no polygons
            self.clear_axis_data() #clear axis data which draws figure
            self.polygons_visible = False
            self.update_information("Polygons currently hidden.", "warning")
            self.selected_polygon = None
            self.get_selected_polygon()

        else:
            for button in self.polygon_buttons:
                if button['description'] == "hide":
                    button['hover_tooltip'].change_hover_text(button['name']) #change text in tooltip to display that polygons are to be hidden if clicked
                    if not button['show_image']:
                        button['widget']['text'] = button['text'] #change the text for show polygons btn if the image is not used
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
    def reset_polygon_cols(self, draw):
        for polygon in self.polygon_info:
            for plot in self.axis.lines:
                if plot in polygon['lines']:
                    plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
            if len(polygon['scatter_points']) > 0:
                for plot in self.axis.collections:
                    if plot in polygon['scatter_points']:
                        plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
        if draw:
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
        self.reset_polygon_cols(True)
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

                #Work on trying to prevent polygon intersect with itself
                # current_polygon_coords = [{"co-ordinates": self.co_ordinates[:-1]}] #Need to not use the last plotted co-ordinate as an intersection will always be the case!
                # intersection = PolygonIntersector(current_polygon_coords, None)
                # intersector_own = intersection.find_intersection([self.co_ordinates[-1:][0], (event.xdata, event.ydata)])

                #see if there are any intersections with this point, there could be intersections if there are polygons therefore greater than 0
                if len(self.polygon_info) > 0:
                    intersection = PolygonIntersector(self.polygon_info, None)

                    intersector_other = intersection.find_intersection([self.co_ordinates[-1:][0], (self.co_ordinates[0][0], self.co_ordinates[0][1])])
                else:
                    intersector_other = False #if there are no polygons then no intersections

                    #If there is no intersection - it is false, intersection present is True
                result = "no"
                if intersector_other:
                    self.update_information("Intersection Found with another Polygon. Plot cannot be made", "warning")
                    result = messagebox.askquestion("Intersection Found", "An intersection with another polygon has been found and the plot has not been made.\n\nWould you like to override this?", icon='warning', default='no')
                    print("RESULT", result)
                    #If there is no intersection - it is false
                if not intersector_other or result == "yes": #if the user said yes then they override the intersection

                    self.co_ordinates.append([self.co_ordinates[0][0], self.co_ordinates[0][1]]) #re-add the co-ords of the first point
                    # self.co_ordinates.append([event.xdata, event.ydata])
                    # a = self.axis.scatter(event.xdata, event.ydata, s=30, color=colour)
                    # self.update_information("Plot plotted successfully.", "positive")

                    coords = self.create_x_y_list(self.co_ordinates) #returns x at index 0, y at 1
                    label = label + "final" ##**CHANGE TO BELOW**
                    v = self.axis.plot(coords[0], coords[1], color=colour, marker="o", label=label, linewidth=self.line_thickness)
                    self.draw_figure()
                    # self.num_of_lines +=1

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
                    record = {"id": id, "slice": self.slice_name, "tag": tag, "co-ordinates": self.co_ordinates}
                    self.file_writer.add_record(record)

                    #update information label
                    self.update_information("Polygon with id: {} saved successfully".format(str(id)), "positive")

                    #reset details
                    self.co_ordinates = []
                    self.num_of_lines = 0

                    self.check_if_polygons_present() #select btn now allowed

                #For any other point that is plotted
            elif (len(self.co_ordinates) != 0):
                #to see if there are intersections with it's own polygon

                #Work on trying to prevent polygon from intersecting itself
                # current_polygon_coords = [{"co-ordinates": self.co_ordinates[:-1]}]
                # intersection = PolygonIntersector(current_polygon_coords, None)
                # intersector_own = intersection.find_intersection([self.co_ordinates[-1:][0], (event.xdata, event.ydata)])


                #see if there are any intersections with this point, there could be intersections if there are polygons therefore greater than 0
                if len(self.polygon_info) > 0:
                    intersection = PolygonIntersector(self.polygon_info, None)
                    intersector_other = intersection.find_intersection([self.co_ordinates[-1:][0], (event.xdata, event.ydata)])
                else:
                    intersector_other = False #if there are no polygons then no intersections

                result = "no"
                if intersector_other:
                    self.update_information("Intersection Found with another Polygon. Plot cannot be made", "warning") #update the message before the screen
                    result = messagebox.askquestion("Intersection Found", "An intersection with another polygon has been found and the plot has not been made.\n\nWould you like to override this?", icon='warning', default='no') #https://stackoverflow.com/questions/51804862/python-3-tkinter-message-box-highlight-the-no-button

                    #If there is no intersection - it is false
                if not intersector_other or result == "yes": #if the user said yes then they override the intersection
                    self.co_ordinates.append([event.xdata, event.ydata])
                    a = self.axis.scatter(event.xdata, event.ydata, s=30, color=colour)
                    self.update_information("Plot plotted successfully.", "positive")

                    coords = self.create_x_y_list(self.co_ordinates) #returns x at index 0, y at 1
                    label = label + "line"
                    v = self.axis.plot(coords[0], coords[1], color=colour, marker="o", label=label, linewidth=self.line_thickness)
                    self.draw_figure()
                    self.num_of_lines +=1
                else:
                    # print("there is an intersection")
                    # if intersector_own:
                    #     self.update_information("Intersection Found with itself. Plot cannot be made", "warning")
                    if intersector_other:
                        self.update_information("Intersection Found with another Polygon. Plot cannot be made", "warning")
        else:
            # print("MRI Slice not clicked.")
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
        self.reset_polygon_cols(True)
        self.remove_highlighted_points()

        #I have not cleared the axis when a polygon is selected to rid it of unfinished polygons as the user may be looking to move other polygons out the way to then continue for instance

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
            self.reset_polygon_cols(True) #resets the colours back to their original colours

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
                    if intersector:
                        break #if there is at least one intersection then break the loop and continue, plot cannot be placed

                    #If doesn't intersect
                result = "no"
                if intersector:
                    self.update_information("Intersection Found with another Polygon. Plot cannot be made", "warning")
                    result = messagebox.askquestion("Intersection Found", "An intersection with another polygon has been found and the plot has not been made.\n\nWould you like to override this?", icon='warning', default='no')
                    print("RESULT", result)
                    #If there is no intersection - it is false
                if not intersector or result == "yes":
                    #Remove the current polygon from the graph
                    print(self.axis)
                    self.remove_plot(polygon['lines'], self.axis.lines)
                    self.remove_plot(polygon['scatter_points'], self.axis.collections)

                    #swap old co-ordinate with new co-ordinate & replot scatter points
                    for poly in self.polygon_info:
                        if poly['id'] == id:
                            poly['co-ordinates'][index] = new_coord #change co_ordinates

                            data = self.file_writer.read_file() #read the file to pass that back through
                            polygon_data = self.file_writer.read_key_data() #get the specified key data for polygon data
                            for item in polygon_data:
                                if item['id'] == poly['id']:
                                    #Update json file
                                    self.file_writer.update_file(data, polygon['id'], 'co-ordinates', poly['co-ordinates']) #pass through poly['co-ordinates'] to replace

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
                self.file_writer.update_file(data, polygon['id'], 'tag', result)

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
                #remove plots from axis
                self.remove_plot(polygon['lines'], self.axis.lines)
                self.remove_plot(polygon['scatter_points'], self.axis.collections)
                self.draw_figure() #draw the figure without the deleted plots

                id = polygon['id'] #id of the polygon

                #remove from the json file
                current_data = self.file_writer.read_file() #read up to data file
                self.file_writer.remove_record(current_data, id) #remove the record from the up to date file

                #remove from dict
                self.polygon_info = [item for item in self.polygon_info if item['id'] != id] #remove from self.polygon info #https://stackoverflow.com/questions/33190779/how-to-delete-a-dictionary-from-a-list-of-dictionaries

                #text to tell user was successfully deleted
                self.update_information("Polygon with Id: {} successfully deleted.".format(str(id)), "positive") #information line to let user know that the polygon has been removed

                #remove from json
                # info = []
                # for polygon in self.polygon_info:
                #     dict = {"id": polygon['id'], 'tag': polygon['tag'], 'slice': polygon['slice'], 'co-ordinates': polygon['co-ordinates'] }
                #     info.append(dict)
                #
                # self.file_writer.create_json_file(info)
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
        self.folder_selected = folder_selected #folder selected address used - this is used to look for & create json file objs in appropiate locations

        self.slice_list = slice_list #DISPENSIBLE = used for creating the file for individual slice notes
        self.figure_information = figure_information #DISPENSIBLE = used for passing split up pieces of folder selected

        self.selected_polygon = None #when a selected polygon is selected, this is passed up
        self.no_notes_label_present = False

        self.note_tabs = [] #stores the tabs as dicts
        self.note_types = [ {"name": "Scan Type", "radio_name": "Scan Type", "file_location": self.figure_information['scan type'] +"_scan_type_notes", "table_col_settings":[
                                                                                                                                                                    {"column": "id", "wraplength":15, "side": "left", "width": 4, "fill": False, "btns": None},
                                                                                                                                                                    {"column": "user", "wraplength":90, "side": "left", "width": 15, "fill": False, "btns": None},
                                                                                                                                                                    {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
                                                                                                                                                                    {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
                                                                                                                                                                    {"column": "time", "wraplength":30, "side": "left", "width": 5, "fill": False, "btns": None}
                                                                                                                                                                    ],
                                                                                                                                                                    "details_required": ['note', 'user', 'year', 'patient', 'date', 'time'],
                                                                                                                                                                    "table_information": "Notes concering the Scan Type: {}".format(self.figure_information['scan type']),
                                                                                                                                                                    "file_sub_extension": {"validator_key": "scantype notes", "validator_val": False, "key_val_to_append_to": "scantype notes", "level": None},
                                                                                                                                                                    "table_width": 665
                                                                                                                                                                    },
                            {"name": "Slice", "radio_name": "Current Slice", "file_location": self.slice_name + "_polygon_slice_notes", "table_col_settings":[{"column": "id", "wraplength":15, "side": "left", "width": 4, "fill": False, "btns": None},
                                                                                                                                                            {"column": "user", "wraplength":90, "side": "left", "width": 15, "fill": False, "btns": None},
                                                                                                                                                            {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False, "btns": None},
                                                                                                                                                            {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False, "btns": None},
                                                                                                                                                            {"column": "time", "wraplength":30, "side": "left", "width": 5, "fill": False, "btns": None}
                                                                                                                                                            ],
                                                                                                                                            "details_required": ['note', 'user', 'year', 'patient', 'scan_type', 'date', 'time'],
                                                                                                                                            "table_information": "Notes concering the Slice: " + self.slice_name,
                                                                                                                                            "file_sub_extension": {"validator_key": "slice notes", "validator_val": False, "key_val_to_append_to": "slice notes", "level": None},
                                                                                                                                            "table_width": 665
                                                                                                                                            },
                            {"name": "Polygon", "radio_name": "Selected Polygon", "file_location": self.slice_name + "_polygon_slice_notes", "table_col_settings":[{"column": "id", "wraplength":15, "side": "left", "width": 4, "fill": False, "btns": None},
                                                                                                                                                                    {"column": "user", "wraplength":90, "side": "left", "width": 15, "fill": False},
                                                                                                                                                                    {"column": "note", "wraplength":285, "side": "left", "width": 40, "fill": False},
                                                                                                                                                                    {"column": "date", "wraplength":100, "side": "left", "width": 10, "fill": False},
                                                                                                                                                                    {"column": "time", "wraplength":30, "side": "left", "width": 5, "fill": False}
                                                                                                                                                                    ],
                                                                                                                                            "details_required": ['note', 'user', 'date', 'time'],
                                                                                                                                            "table_information": "Notes concering a Polygon", #this is properly set within self.selected polygon as None type is not subscriptble
                                                                                                                                            "file_sub_extension": {"validator_key": "polygon data", "validator_val": False, "key_val_to_append_to": "polygon data", "level": {"validator_key": "id", "validator_val": -1, "key_val_to_append_to": "notes", "level": None}},
                                                                                                                                            "table_width": 665
                                                                                                                                            }]
        #create notebook
        self.note_tab_pane = ttk.Notebook(self.parent_frame)
        self.note_tab_pane.pack(side="bottom", fill="x")

        #create tabs
        i = 0
        for item in self.note_types:
            new_tab = Tab(self.note_tab_pane, HEADER_BG) #create tab pane
            inner_tab_frame = new_tab.add_tab(item['name'] + " Notes")
            self.show_note(inner_tab_frame, item['radio_name'])
            self.note_tabs.append({"tab":item['radio_name'], "frame":inner_tab_frame, "tab_index": i})
            item['tab_frame'] = inner_tab_frame
            i += 1

        #create add note tab
        self.new_tab_add = Tab(self.note_tab_pane, HEADER_BG) #create a new tab instance
        self.notes_frame = self.new_tab_add.add_tab("Add Note")
        self.note_tab_pane.select(self.notes_frame) #override the function of selecting the last added tab to select a specfic one i.e the add note tab

        #Contents of Add Note tab
        #create radio buttons
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

        # print("SDJSDS")
        self.no_polygon_selected_reset() #disable the selected polygon button if no polygon selected

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

    #GENERAL METHODS REGARDING RADIO BUTTONS & TABS
    #A function that changes the text and the status of a radio btn
    def change_radio_btn_text_and_status(self, radio_btn_name, state, widget_text):
        for radiobtn in self.radiobuttons:
            if radiobtn['name'] == radio_btn_name:
                radiobtn['widget']['state'] = state
                radiobtn['widget']['text'] = widget_text

    #A function that can alter the name of a Tab header
    def set_tab_name(self, tab_name, new_title):
        for item in self.note_tabs: #reset the tab to Polygon Notes
            if item['tab'] == tab_name:
                self.note_tab_pane.tab(item['tab_index'], text=new_title)

    #A function that can customise the note widget text as it normally just says No Notes Made or may provide a table. Customises with label only
    def customise_note_widget_text(self, tab_name, new_label_text):
        for notetype in self.note_types:
            if notetype['radio_name'] == tab_name:
                if 'table_or_error_widget' in notetype:
                    notetype['table_or_error_widget'].destroy()
                    new_label = tk.Label(notetype['table_frame_widget'], text=new_label_text, bg=HEADER_BG, fg=FONT_COL)
                    new_label.pack(side="top", fill="both", expand=True)
                    notetype['table_or_error_widget'] = new_label

    #METHODS REGARDING UPDATING SLICE NAME/SELECTED POLYGON/RADIO BTN
    #If no polygon is selected then disable radio button - relates just to selected polygon
    def no_polygon_selected_reset(self):
        if self.selected_polygon == None: #self.selected polygon should be None
            self.note_type.set(None) #deselects the radiobutton if value outside of values possible  #https://stackoverflow.com/questions/43403653/how-to-deselect-a-radio-button-tkinter

            self.change_radio_btn_text_and_status("Selected Polygon", 'disabled', "Selected Polygon") #disable the selected polygon radio btn to Selected Polygon

            self.customise_note_widget_text("Selected Polygon", "No Polygon Selected") #Add a customised msg as it normally says No Notes Added

            self.set_tab_name("Selected Polygon", "Polygon Notes") #reset the tab to Polygon Notes

    #When the current slice is changed, the current slice in this class is updated.
    def update_slice_name(self, new_slice_name):
        self.slice_name = new_slice_name #updates the slice name
        self.selected_polygon = None #alters selected polygon to None as if slice is changed then there is no polygon selected

        for item in self.note_types:
            if item['name'] == 'Slice':
                item['file_location'] = self.slice_name + "_polygon_slice_notes"
            elif item['name'] == 'Polygon':
                item['file_location'] = self.slice_name + "_polygon_slice_notes"
                item['file_sub_extension']['level']['validator_val'] = -1 #reset to -1 as this will fail validation

        self.refresh_tabs_manually(['Current Slice', 'Selected Polygon'])

        print("HDSBD")
        self.no_polygon_selected_reset() #disable the polygon radio button

    #This method is called when polygon is selected from Polygons class (child of Slice Figure Parent)
    def set_selected_polygon(self, polygon):
        self.selected_polygon = polygon
        if self.selected_polygon != None:
             #set the tab name for polygon notes to be following
            self.set_tab_name("Selected Polygon", "Polygon Notes: Id: " + str(self.selected_polygon['id']) + " Tag: " + self.selected_polygon['tag'])

            #update the validator value for the dict above
            for item in self.note_types:
                if item['radio_name'] == "Selected Polygon":
                    item['file_sub_extension']['level']['validator_val'] = self.selected_polygon['id'] #it's default above is -1 which can never be an id and will therefore not be found when runs if this does not work

            #change the name of the selected polygon
            self.change_radio_btn_text_and_status("Selected Polygon", 'normal', "Polygon ID: " + str(self.selected_polygon['id'])) #normalise radio btn for selected polygon & id into name

            #only refresh notes for table that note has been added for
            self.refresh_tab("Selected Polygon") #refresh the polygon tab for notes as the selected polygon has changed
        else:
            print("HEREDSD")
            self.no_polygon_selected_reset()


    #ADJUSTING OF NOTES METHODS
    #Method for adding a note
    def add_note(self):
        #Get Values - WOuld like below to work
        formatted_date_time = TimeDate().return_formatted_date_time()
        possible_note_details = {"note": self.notebox.read_contents()[:-1], "user": self.username, "year": self.figure_information['year'],
                        "patient": self.figure_information['patient'], "scan_type": self.figure_information['scan type'],
                        "slice name": self.slice_name[:-1], "date": formatted_date_time[0], "time": formatted_date_time[1]}

        for notetype in self.note_types:
            if self.note_type.get() == notetype['radio_name']:
                note_details = {}
                for detail_required in notetype['details_required']:
                    note_details[detail_required] = possible_note_details[detail_required]

                #get the file & read it
                file_name = self.folder_selected + "/" + notetype['file_location'] + '.json'
                json_file = jsonFileWriter(file_name, None, None) #look for json file
                data = json_file.read_file() #read file

                #add data to file - look for sub extensions i.e where to place the data in the file
                jsonNoteAdder(notetype['file_sub_extension'], note_details, data)
                json_file.create_json_file(data) #create new data file

        #database - don't think this will work
        # if MAKE_DB:
        #     for item in TABLES: #making it dynanmic, so can have multiple buttons above
        #         if self.note_type.get() == item['value']:
        #             database_instance = Database(DB_NAME)
        #             database_instance.add_record(item['table_name'], values_ready, item['columns'])

        # #only refresh notes for table that note has been added for
        self.refresh_tab(self.note_type.get())
        # #Reset the tab now a note has been added
        self.reset_add_note_tab()

    #Method for showing the table
    def show_note(self, frame, given_note_type):
        # print("HELLO SHOW")
        for notetype in self.note_types:
            if given_note_type == notetype['radio_name']:
                file_name = self.folder_selected + "/" + notetype['file_location'] + '.json' #Gets the filename
                # print("FILELOCATION", file_name)
                data_present = False
                if os.path.exists(file_name):
                    json_file = jsonFileWriter(file_name, None, None) #calls json file writer
                    notes = json_file.read_file() #reads whats already in the file, if there was not one then will just be an empty list

                    note_finder = jsonNoteShow(notetype['file_sub_extension'], notes) #this class uses the data above to return the notes from the certain depth of json as inputted
                    unformatted_data = note_finder.returned_data
                    # print("RETURNED DATA", note_finder.returned_data)

                    # Only use data as prescribed by column settings

                    formatted_data = []
                    if unformatted_data != None: #the jsonNoteShow will return note through note_finder.returned_data if there is no data or errors
                        if len(unformatted_data) > 0:
                            try: #for instance if it is for some reason not a list
                                data_present = True
                                for record in unformatted_data: #unformtted data will contain a lot of other information that is not wanted by the table
                                    formatted_record = {}
                                    for column in notetype['table_col_settings']: #the columns are structured above, the table will only show the columns, the headers are the same as the keys in the note
                                        try:
                                            formatted_record[column['column']] = record[column['column']]
                                        except:
                                            formatted_record[column['column']] = None #if the column is not found for some reason in the col settings
                                    formatted_data.append(formatted_record)
                            except TypeError:
                                print("ERROR, creating Notes table for note: {}".format(str(notetype))) #if there is an error, lets user know with the notetype

                if 'table_frame_widget' not in notetype: #only create if the frame has not been created before
                    tb_frame = tk.Frame(frame, bg=HEADER_BG)
                    tb_frame.pack(side="top", fill="both", expand=True)
                    notetype['table_frame_widget'] = tb_frame

                if data_present:
                    if 'table_or_error_widget' in notetype:
                        notetype['table_or_error_widget'].destroy()
                    # print("FORMATTED DATA", formatted_data)
                    row_btns = [{"name": "remove", "text": "Remove", "function": lambda  args, notetype = given_note_type: self.remove_note(args, notetype), "width": 7}, #btns for the remove & edit functions
                                {"name": "edit", "text": "Edit", "function": lambda args, notetype = given_note_type: self.edit_note(args, notetype), "width": 7}
                                ]

                    table = NoteTable(notetype['table_frame_widget'], notetype['table_col_settings'], formatted_data, notetype['table_width'], 150, row_btns, HEADER_BG) #create table using NoteTable functionality
                    notetype['table_or_error_widget'] = table #assign so can be destroyed elsewhere in the class
                else:
                    if 'table_or_error_widget' in notetype:
                        notetype['table_or_error_widget'].destroy()
                    error_label = tk.Label(notetype['table_frame_widget'], text="No notes have been made.", bg=HEADER_BG, fg=FONT_COL) #if there are no notes or there was any kind of error then runs this
                    error_label.pack(side="top", fill="both", expand=True, padx=10, pady=10)
                    # print("HELLO")
                    notetype['table_or_error_widget'] = error_label #assign so can be destroyed elsewhere in the class

    #Method called for when a note is to be edited
    def edit_note(self, args, given_note_type):
        #loads edit window & recieves result for the new note
        current_note = args[0]['note']
        current_note_id = args[0]['id']
        edit_note = EditNote(current_note, given_note_type, self.folder_selected, self.slice_name).send()
        # #if confirm button is clicked then note is returned, if cancel clicked None returned
        if edit_note != None:
            for notetype in self.note_types:
                if given_note_type == notetype['radio_name']:
                    file_name = self.folder_selected + "/" + notetype['file_location'] + '.json' #Gets the filename
                    json_file = jsonFileWriter(file_name, None, None) #calls json file writer
                    notes = json_file.read_file() #reads whats already in the file, if there was not one then will just be an empty list

                    jsonNoteEdit(notetype['file_sub_extension'], notes, edit_note, current_note_id)
                    json_file.create_json_file(notes) #create new data file

                    self.refresh_tab(given_note_type) #only refresh if note has actually changed

    #Method called for when a note is to be removed
    def remove_note(self, args, given_note_type):
        current_note = args[0]['note']
        current_note_id = args[0]['id']

        result = messagebox.askquestion("Delete Note", "Are you sure you want to delete note: {}?".format(str(current_note_id)), icon='question') #if result is True then continue

        if result:
            for notetype in self.note_types:
                if given_note_type == notetype['radio_name']:
                    file_name = self.folder_selected + "/" + notetype['file_location'] + '.json' #Gets the filename
                    json_file = jsonFileWriter(file_name, None, None) #calls json file writer
                    notes = json_file.read_file() #reads whats already in the file, if there was not one then will just be an empty list

                    jsonNoteDelete(notetype['file_sub_extension'], notes, current_note_id)
                    json_file.create_json_file(notes) #create new data file

                    self.refresh_tab(given_note_type) #only refresh if note has actually changed

    #TAB ORIENTED METHODS
    #Method for refreshing the table in a tab
    def refresh_tab(self, tab):
        # print("ENTERED REFRESH TAB")
        for item in self.note_tabs:
            if item['tab'] == tab:
                self.show_note(item['frame'], item['tab'])

    #Function that just automates the refresh tab function above
    def refresh_tabs_manually(self, tab_names_list):
        for tab in tab_names_list:
            self.refresh_tab(tab)

    #Method for resetting the add Note tab after a note is added
    def reset_add_note_tab(self):
        self.note_type.set("None") #set the radio buttons to a value that is not present
        self.notebox.replace_text(self.initial_text) #replace with initial text
        self.notebox.disable_notebox() #disable the notebox
        self.notebox_btns.disable_all_btns() #changes Add to disable & clear to normal

    #METHODS REGARDING TEXTBOX
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

app = MainApp()
# app.geometry("1280x780") #x by y
app.mainloop()
