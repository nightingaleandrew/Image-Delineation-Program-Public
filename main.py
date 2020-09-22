#This is the main file for this program. Please run this program to run the code.
#In this file are the central imports, centrally set variables & core classes invovling MainApp, PageOne, SliceFigure, Polygons
#This file would need further trimming down & breaking up in phase II.

#IMPORTS
#tkinter imports
import tkinter as tk
from tkinter import ttk #for styling eg. ttk buttons
from tkinter import messagebox, colorchooser, filedialog

#other imports
import random, os, re, time, datetime, sqlite3, numpy as np, json

#matplotlib imports & configs
import matplotlib
matplotlib.use("TkAgg") #backend of matplotlib
matplotlib.rcParams['savefig.format'] = 'png' #the saved image is using png
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#Harry. (2020) from matplotlib.backends import _tkagg ImportError: cannot import name _tkagg [Online]. Available at: https://stackoverflow.com/questions/32188180/from-matplotlib-backends-import-tkagg-importerror-cannot-import-name-tkagg [Accessed 08 July 2020].
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea
from matplotlib.figure import Figure #For loading the figure
import matplotlib.image as mpimg #this is for including imagesif jpgs or pngs wanted to be loaded into the program

#image imports
from PIL import ImageTk, Image
from PIL import Image as PIL_image, ImageTk as PIL_imagetk

#FILE IMPORTS (Please refer to each file for information on respective classes)
#compartmenatislation based classes, widgets, layouts etc
from window_classes import TopLevelWin, WindowLayout
from widget_creator_classes import TextBox, InformationBox, ButtonCreator, Tab, NoteTable, ColourSquare, ToggledFrame, LoginFrame, HoverToolTip
from other_windows import PolygonSettings, EditNote, PolygonTagChanger
from other import ConvertImages, TimeDate, StringMaker, ImageFinder, PolygonMasker

#matplotlib figure orientated classes
from figure_custom_classes import cidPress, PolygonIntersector, CustomToolbar, PolygonHover, cidHover
from PolygonTranslater import TransformationMatrixFinder, PolygonTranslater

#Storage/json classes
from json_file_manipulator import jsonNoteAdder, jsonNoteShow, jsonNoteEdit, jsonNoteDelete #adding data at different depths of a file after it has been read
from storage_classes import Database, jsonFileReaderWriter

#Styles, fonts, file_locations for tags, settings, stacks dir, custom btn images & respective locations & configs
from styles import colour_scheme, fonts
from file_locations import file_locations
from button_images import custom_btn_images

#Here, I pull in the settings json file, if there is one (if not one is created) & I check it for errors. If errors then default values are used (which are hardcoded in that file).
#In the settings json file only the config & default values can be changed. They need to be changed before the program is loaded. Any changes within the program will be temporary for the session.
from check_json_files import SetSettings, TagFileLoader

#NON CONFIG SETTINGS

#TERMINOLOGY
#I will gradually move the program so Slice is removed from terminology throughout. This is a post project development to allow it to be used for not just MRI Slices but any images
EACH_FILE_NAME = "MRI Slice"
GROUP_OF_FILES_NAME = "MRI Stack"

#SECURITY
PASSWORD_REQUIRED = False #if password is not required then just requires a username
PASSWORD = "" #security is not a central functional requirement in this program as files are on machine anyway.

#OTHER
FILETYPES_ACCEPTED = {".npy": True, ".png": False, ".jpg": False} #again linking to the fact to make program any img orientated
NPY_FILES_TYPES_NOT_WANTED = ["nor", "sus"]
IMG_COLOURMAP = 'gray' #viridis is default, for instance if non gray imgs were to be allowed
MASK_COLOUR_OR_BLACK_WHITE = True #if this is false then mask produced will be black or white.

SYNCHRONISATION = True #if synchronisation is on for this program
DISREGARD_TRANSLATED_POLYGONS_WITH_GT_3_SLICE_NUMS = False #if the slices for the translated polygon extend over 3 different numbers, show/hide polygon altogether

#CONFIGUABLE SETTINGS
#These are the settings that are used for the program while it is live such as line thickness & precision. The settings above (not including Password) will gradually be added in as program moves along
settings_file = SetSettings(file_locations['settings'])
SETTINGS = settings_file.settings

#Storage ** In phase II I would set it up so this can be set centrally **
#GOING FORWARDS - if needed. Setup db & test throughout adding/removing/editing records
# MAKE_DB = False #**PLEASE DON'T MAKE TRUE AS WAS DISCONTINUED EARLY ON**
# MAKE_JSON = True #for saving to json



#CLASSES

#MAIN APP
#Main App that controls which frame or page is shown - either Start Page or Page One. Frame is not changed by changing window. It is a tk.raise on the frame.
#Source: Sentdex (2014) GUIs with tkinter (intermediate) [Video]. Available: https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk [Accessed: 01 July 2020].
class MainApp(tk.Tk):  #inherit tkinter methods from tk class inside tkinter
    def __init__(self, *args, **kwargs): #initialise the method
        tk.Tk.__init__(self, *args, *kwargs) #initalise tkinter
        tk.Tk.wm_title(self, "Dissertation Application - Andrew Nightingale") #set the title of the program
        # tk.Tk.iconbitmap(self, default=PROGRAM_ICON) #16 by 16 ico file #using this in some way can change the icon of the program

        #create main container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1) #0 is setting of min size
        container.grid_columnconfigure(0, weight=1)

        #MenuBar with controls for quiting application (these are the same across the application) - Can add colour scheme, settings in here?
        menubar = tk.Menu(container) #menu bar for all pages
        filemenu = tk.Menu(menubar, tearoff = 0) #dotted line that allows the little window to come off, if don't want can use 0
        filemenu.add_command(label="Exit", command=quit) #built in method quit
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        #Frames for application. Application does not switch between window but simply raises a frame above another to change 'pages'. User flow is a lot smoother
        self.frames = {}
        for f, geometry in zip((StartPage, PageOne), ('400x300+550+200', "1400x700+50+0")): #pages & their respective geometries - Login is much smaller for efficient use of space
            #geom is x by y (size) + offset x & offset y
            frame = f(container, self)
            self.frames[f] = (frame, geometry)
            frame.grid(row=0, column=0, sticky="nsew")

        #Show StartPage first off
        self.show_frame(StartPage, "No Session") #remember to pass msg through, 'No Session' is passed through by defaukt but msg would be passed through from PageOne

        #Styling for the program, generally. I am looking to expand on this in page II and create a custom ttk style that is within the styles file that is imported.
        program_style = ttk.Style(self)
        program_style.theme_use('alt') #using alt style for ttk. - I am bringing in the set colours etc from the styles file
        #python.org. tkinter.ttk — Tk themed widgets [Online]. Available at: https://docs.python.org/3/library/tkinter.ttk.html [Accessed: 27 July 2020].
        #Button
        program_style.configure('TButton', background = colour_scheme['secondary_bg'], foreground =colour_scheme['secondary_fg'], focusthickness=3, focuscolor= colour_scheme['button_hover'])
        program_style.map('TButton', background=[('active', colour_scheme['button_hover'])])
        #Notebook
        program_style.configure('TNotebook', tabmargins = [2, 5, 2, 0], background=colour_scheme['main_bg'], borderwidth=0)
        #Notebook tab
        program_style.configure('TNotebook.Tab', padding = [5, 5], background=colour_scheme['secondary_bg'], foreground=colour_scheme['font_col'], focusthickness=3, focuscolor=colour_scheme['secondary_bg'])
        program_style.map('TNotebook.Tab', background = [("selected", colour_scheme['header_bg'])], expand =[("selected", [1, 1, 1, 0])])
        #Radiobutton
        program_style.configure('TRadiobutton', background=colour_scheme['header_bg'], foreground=colour_scheme['font_col'])
        program_style.map('TRadiobutton', foreground=[("selected", colour_scheme['error_font']), ("active", colour_scheme['button_hover'])], background=[("selected", colour_scheme['header_bg']), ("active", colour_scheme['header_bg'])])
        # Stevo Mitric. (2016) Changing the background color of a radio button with tkinter in Python 3 [Online]. Available at: https://stackoverflow.com/questions/37234071/changing-the-background-color-of-a-radio-button-with-tkinter-in-python-3 [Accessed: 01 September 2020].
        # ttk_radiobutton. Tcl8.6.10/Tk8.6.10 Documentation [Online]. Available at: https://www.tcl.tk/man/tcl8.6/TkCmd/ttk_radiobutton.htm [Accessed: 01 September 2020].

    #function to raise the particular frame called & also send info & struc geometry of frame
    def show_frame(self, cont, msg): #when show_frame called, msg needs to be passed through
        frame, geometry = self.frames[cont]
        frame.sendmsg(msg) #send the message to the class before rasied - I use the ability to send msgs between frames so for instance the username can go through to page two
        self.geometry(geometry) #change the geom of the whole frame
        frame.tkraise() #raise to the front

#START PAGE
#Class for the start page, this page has the ability to login & add a username into the system. Remember security is not a main requirement but I have added this to enable it to be added in very easily.
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #initialise tkinter frame
        self.controller = controller #bring in the controller

        #Layout of main app
        self.window_layout = WindowLayout(self)
        self.header = self.window_layout.create_header("MRI Delineator", "top", fonts['large_font']) #create header
        self.main = self.window_layout.create_main() #create main & get this obj

        #Login Frame
        self.password_details = {"required": PASSWORD_REQUIRED, "password": PASSWORD}
        self.login = LoginFrame(self, self.main, colour_scheme['main_bg'], colour_scheme['font_col'], self.password_details) #set up the login frame

        #Last User label
        self.last_user = tk.Label(self.main, bg=colour_scheme['main_bg'], fg=colour_scheme['font_col']) #this is passed back from PageOne. 'NO Session' is the msg set from MainApp

    #Simple function that is called by the login frame as the parent is passed through if login is successfull
    def pass_through_login_frame(self, username):
         self.controller.show_frame(PageOne, username) #call show frame to show page one

    #sendmsg function that passes info from A to B eg. StartPage to PageOne
    def sendmsg(self, msg ):
        self.last_user['text'] = "Last User: " + msg #set up the last user text
        self.last_user.grid(row=2, column=1, pady=(0, 10), padx=10, sticky="N")

        self.login.reset_login_widgets() #resets the login widgets that were used using the login frame obj created in innit

#PAGE ONE
#Class for the Page One where username is passed through & session begins
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #initlaise tkinter & bring in controller
        self.controller = controller

        #SETTING UP DB - NOT USED CURRENTLY
        #create the DB and tables if not present in dir - created when session starts so in PageOne
        # self.setup_db() #this is done in the setup db method

        #MAIN PAGE WIDGETS
        self.window_layout = WindowLayout(self)
        self.header = self.window_layout.create_header("Delineate", "left", fonts['large_font']) #header container
        main_window = self.window_layout.create_main() #main container
        self.interior = self.window_layout.add_scrollbars(main_window) #I add scrollbars to just the main window, doesn't include the header to keep scan data visible

        #HEADER - I set up Header with controls & information first in PageOne
        #SESSION CONTROLS - CLOSE SESSION & QUIT
        self.header_btns = tk.Frame(master=self.header, bg=colour_scheme['header_bg']) #frame for controls
        self.header_btns.pack(side="right", pady=10, padx=10)

        self.quit_btn = ttk.Button(self.header_btns, text="Quit", command=quit, width=12) #quits application
        self.quit_btn.grid(row=0, column=0, pady=(0, 10))

        self.close_session_btn = ttk.Button(self.header_btns, text="Close Session", command=lambda: self.controller.show_frame(StartPage, self.entry.get()), width=12) #closes the session & brings up the show_frame method of the controller.
        self.close_session_btn.grid(row=1, column=0)

        #SESSION INFO BOX IN HEADER
        self.session_info = InformationBox(self.header, "right", 2, "Current Session", None, colour_scheme['header_bg'], colour_scheme['font_col'], False)

        #VISIBLE STACK DATA INFO BOX IN HEADER - frame to contain
        self.currently_viewing_frame = tk.Frame(self.header, bg=colour_scheme['header_bg']) #to contain the information boxes for currently viewing stacks
        self.currently_viewing_frame.pack(side="right")


        #MAIN FRAME - (uses self.interior as scrollbars) - setting up of contents of main frame
        #LOAD STACKS CONTROLS
        self.browse_frame = tk.Frame(self.interior, bg=colour_scheme['main_bg']) #frame that includes load controls, arrow controls for swapping frames, settings controls
        self.browse_frame.pack(side="top", fill="x")

        self.browse_frame.rowconfigure(0, weight=1)
        for i in range(3): #just create a 3
            self.browse_frame.columnconfigure(i, weight=1)


        #NOTEBOOKS
        #- A notebook contains 1 or more tabs which contain a figure. Only one tab can contain one stack where each slice is represented at the time
        #        on the figure. The stack can be iterated through to see the different slices which replace each other & fill the figure
        #- If one notebook is present then will fill screen, if two then will divide in two. Numerous tabs can be added to one notebook.

        #**FUTURE DEVELOPMENT PHASE II (notebooks)
            # 1. Allowing multiple notebooks to be added, not just 2 eg. if very large screen (it is nearly there, just needs a few tweaks)
            # 2. Create Notebook class

        #Number of tab panes that are created
        self.num_notebooks = 2 #2 notebooks created at start

        self.notebook_frames = [] #contains all the notebooks with relevent info in a dict
        self.comparison_open = False #if two panes are being compared then is true, start with no comparisons
        self.current_figures = [] #contains all current figures for updating settings etc
        self.all_tabs = [] #contains all the Tab instances
        self.swap_tab_btns = [] #contains instances in a dict of the swap tab btns. Aswell as ButtonCreator class, it has left & right notebook instances for each to determine if there are any tabs open

        #Tab area for notebooks - all notebooks are contained in tab area
        self.tab_area = tk.Frame(self.interior, background=colour_scheme['main_bg'])
        self.tab_area.pack(side="bottom", fill="both", expand=True)

        #create the notebooks depending on number mentioned above - currently hardcoded at 2
        for i in range(self.num_notebooks):
            notebook_frame = tk.Frame(self.tab_area, bg=colour_scheme['main_bg']) #create the notebook frame

            #IF there is no comparison eg. there is only one notebook or 0 tab & if i is first notebook then set grid to whole area - fill out frame with notebook
            if not self.comparison_open and i == 0:
                notebook_frame.grid(row=0, column=i, sticky="NSWE") #only grid out first frame
                self.tab_area.rowconfigure(0, weight=1) #set grid area so only one tab area if presented
                self.tab_area.columnconfigure(i, weight=1)

            #IF there is a comparison open then divide up frame to fit equally spaced notebooks
            elif self.comparison_open:
                 notebook_frame.grid(row=0, column=i, sticky="NSWE") #grid every frame if comparison open
                 self.tab_area.rowconfigure(0, weight=1) #all frames are on 0 row
                 self.tab_area.columnconfigure(i, weight=1) #columns would increase depending on comparison

            notebook = ttk.Notebook(notebook_frame) #instance of ttk.notebook
            notebook.pack(side="left", fill="both", expand=True, pady=(0, 10), padx=10)

            #collect all frames together & notebooks inc current tabs & INformationBox obj
            self.notebook_frames.append({"id": i, "parent_frame": notebook_frame, "notebook":notebook, "tabs": [], "slice_information": None})


        #FUTURE DEVELOPMENT - make this bind dynanmic
        for notebook in self.notebook_frames:
            #when a notebook is selected, it changes the viewing information for the stack in the associated stack info box in the header. It also changes the colour of the tab
            notebook['notebook'].bind("<<NotebookTabChanged>>", lambda e, notebook=notebook: self.update_viewing_information(notebook)) #seems I have to do binding seperatly, when a tab is clicked, changes info in currently viewing
            #Oakley, B. (2018) Python tkinter bindtag Event handling - how to update which tab is currently selected [Online]. Available at: https://stackoverflow.com/questions/48104061/python-tkinter-bindtag-event-handling-how-to-update-which-tab-is-currently-sel [Accessed: 19 August 2020]


        #LOADING STACKS CONTROLS
        self.load_stacks_controls = tk.Frame(self.browse_frame, bg=colour_scheme['main_bg']) #frame to contain the controls
        self.load_stacks_controls.grid(column=0, row=0, sticky="NSWE")

        self.load_stacks_buttons_dict = [] #create a load button for the number of stacks available. eg. if 3 then create 3 load buttons.
        #FUTURE DEVELOPMENT - only create a load stack button to load another tab AFTER a notebook has been loaded. Therefore only 1 is shown at the start and then 2 if 1 notebook is created
        for i in range(self.num_notebooks):
            name = "load a stack (tab " + str(i + 1) +")" #load a stack for a particular notebook
            state = "normal" #first btn is normal
            comparison = False #no comparison with first button
            if i > 0:
                state = "disabled" #further comparison btns disabled
                comparison = True #comparisons onwards - used in load_stack method
            self.load_stacks_buttons_dict.append({"name": name, "command":lambda notebook_frame = self.notebook_frames[i], comparison=comparison: self.load_stack(notebook_frame, comparison), "default_state": state, "side":"left", "width":25})

        self.load_stacks_buttons = ButtonCreator(self.load_stacks_controls, self.load_stacks_buttons_dict) #create btn using ButtonCreator


        #OTHER BROWSE FRAME BTNS - POLYGON SETTINGS, CLOSE TABS
        self.other_btns_frame = tk.Frame(self.browse_frame, bg=colour_scheme['main_bg']) #create a frame to contain them in
        self.other_btns_frame.grid(column=2, row=0, sticky="NSWE")

        self.other_btns_dict = [{"name": "polygon settings", "command":lambda  function=self.open_settings_config: function(), "default_state": "normal", "side":"right", "width":15},
                                {"name": "close all tabs", "command":lambda function=self.remove_tabs: function(), "default_state": "disabled", "side":"right", "width":15}]
        self.other_btns = ButtonCreator(self.other_btns_frame, self.other_btns_dict) #create the buttons using buttoncreator


        #NON LAYOUT / WIDGET CLASS VARIABLES
        self.synchronised_figures = [] #fills if any figures on PageOne are synchronised.
        #I have done it at this level as there could be multiple different synchronisations. A sync can happen between tabs of same patient & year. Therefore if multiple patients & years open then possible multiple syncs

        self.file_directory = None #this is set when the first stack is loaded, the program tests if the directory exists when it loads a stack. Can then use this going forward



    #METHODS
    #FUTURE DEVELOPMENT - too many methods, dividing up Notebook into seperate class will help with this

    #GENERAL METHODS
    #Method for setting up the Database if needed when a new session starts
    # def setup_db(self):
    #     if MAKE_DB:
    #         needcreate = not os.path.exists('./' + DB_NAME)
    #         if needcreate:
    #             db = Database(DB_NAME)
    #             for table in TABLES:
    #                 db.create_table(table['table_name'], table['columns'])

    #Function that is called when the session is closed, destroys all the widgets on the page
    def destroyFrame(self, StartPage, username):
        self.hard_reset_settings() #reset to defaults the settings in case any have been changed. Config Settings are SESSION ONLY
        self.remove_tabs() #removes the tabs & sets back settings back to start eg. comparison
        self.controller.show_frame(StartPage, username) #Head back to the start page

        if self.session_info != None:
            self.session_info.present_no_value() #allows the session info box to overwritten with no values so the new values can take place without looking like they are above previous

    #Function is called by the "owner" of PageOne, MainApp, which can pass messages for us. This also destroys the frame
    def sendmsg(self, username):
        #update the information box that displays the session information
        session_information = {"user": username, "start time": TimeDate().get_time_stamp()} #call time to get current time this is called
        self.session_info.create_insides(session_information)

        self.close_session_btn.destroy() #Need to destroy current close session btn
        self.close_session_btn = ttk.Button(self.header_btns, text="Close Session", command=lambda: self.destroyFrame(StartPage, username), width=12)
        self.close_session_btn.grid(row=1, column=0)

    #When the session is closed the settings are hard reset to their default values - remember settings are SESSION ONLY
    def hard_reset_settings(self):
        for item in SETTINGS:
            item['current_value'] = item['default_value'] #set to default
            item['temp_value'] = None #temp value which is changed if a setting is changed is set to None.


    #NOTEBOOK & TAB METHODS
    #Function that creates a tab within a notebook
    def create_tab(self, slice_address, notebook_frame, folder_dir, sibling_slices):
        #figure information for the figure, I have used negative values as the path may be different depending on computer (But path within data will be the same)
        self.figure_information = {"year":slice_address[-4], "scan type":slice_address[-1], "patient":slice_address[-3]}

        #Figure Information Box: Currently Viewing
        if notebook_frame['slice_information'] != None: #if figure information box already there then replace with new
            notebook_frame['slice_information'].make_box_go_walkies() #forget the sliceinfo box so a new one can be added. Or could use refresh method
        notebook_frame['slice_information'] = InformationBox(self.currently_viewing_frame, "left", 2, "Currently Viewing Tab " + str(notebook_frame['id'] + 1), self.figure_information, colour_scheme['header_bg'], colour_scheme['font_col'], True) #assigns the information contents

        #Creation of Tab & storing of Tab
        tab_obj = Tab(notebook_frame['notebook'], colour_scheme['header_bg'])  #create tab objs
        tab_pane = tab_obj.add_tab(StringMaker().title_formatter(self.figure_information)) #create tab pane
        self.all_tabs.append({"parent_frame": notebook_frame['parent_frame'], "tab_obj": tab_obj, "tab_pane_frame":tab_pane}) #add tab to all tabs list

        #TAB ID METHOD: Simple non duplicate tab id functionality (for swapping tabs)
        if len(notebook_frame['tabs']) > 0:
            tab_id = notebook_frame['tabs'][-1]['id'] + 1 #always add one to the last one & therefore never have a duplicate
        else:
            tab_id = 1
        notebook_frame['tabs'].append({"id":tab_id, "tab_obj": tab_obj, "tab_pane_frame":tab_pane, "tab_figure_slice_address": slice_address, "tab_figure_info": self.figure_information, "folder_dir": folder_dir, "sister_slices": sibling_slices}) #add tab to particular notebook's frame

        #FIGURE CREATION
        # print("create tab", self.session_info.pull_detail('User'))
        figure = SliceFigure(tab_pane, folder_dir,  sibling_slices, self.session_info.pull_detail('user'), self.figure_information, self) #creates the figure for the tab
        self.current_figures.append(figure) #append so all figures stored for settings usage

    #Method for adding a new comparison frame if comparison wanted - enabling comparison (splitting of screen) or removing comparison if already True and only one notebook going to be open
    #FUTURE DEVEOPMENT - Make this further dynanmic - only works for two notebooks currently
    def set_comparison(self):
        if self.comparison_open == False: #if there is only one notebook present then comparison is false
            self.tab_area.rowconfigure(0, weight=1)
            for i in range((len(self.notebook_frames))):
                self.notebook_frames[i]['parent_frame'].grid(row=0, column=i, sticky="NSWE") #set the parent frame in self.notebook_frames
                self.tab_area.columnconfigure(i, weight=1) #for number of notebooks then divide up page
                if i >= 1:
                    #create the arrow buttons for swapping tabs across notebooks
                    swap_btn_frame = tk.Frame(self.browse_frame, bg=colour_scheme['main_bg'])
                    swap_btn_frame.grid(column=1, row=0, sticky="NSWE") #THIS IS NOT DYNAMIC
                    arrow_btn_dict = [{"name": "<", "command":lambda side = "left", to_pane = self.notebook_frames[i], from_pane = self.notebook_frames[i - 1]: self.swap_tab(side, to_pane, from_pane), "default_state": "normal", "side":"left", "width":5},
                                    {"name": ">", "command":lambda side = "right", to_pane = self.notebook_frames[i - 1], from_pane = self.notebook_frames[i]: self.swap_tab(side, to_pane, from_pane), "default_state": "normal", "side":"left", "width":5}]
                    arrow_btns = ButtonCreator(swap_btn_frame, arrow_btn_dict) #create arrow buttons
                    self.swap_tab_btns.append({"button_class": arrow_btns, "left_hand_frame": self.notebook_frames[i - 1], "right_hand_frame": self.notebook_frames[i]})

            self.comparison_open = True
            self.swap_tab_btn_status_changer() #disable the btn going right if only one tab in the left hand pane

            #If comparison is open then reset to one notebook across screen
        elif self.comparison_open == True:
            self.reset_to_one_notebook() #reset the screen to one notebook, self.comparison_open is set to false in here

            for arrow_btns in self.swap_tab_btns: #forget the arrow buttons as only one notebook so cannot move tabs
                arrow_btns['button_class'].forget_btns()


    #Function that loads a directory or stack of slices into the program
    def load_stack(self, notebook_frame, comparison):
        #check the directory provided is correct.
        try:
            if (os.path.isdir(file_locations['stacks_directory'])):
                self.file_directory = file_locations['stacks_directory']
            else:
                self.file_directory = "./" #if doesn't work just put directory to this.
                print("Error. File Path supplied does not work.") #The error path supplied has not worked. Uses basic directory of where program is located instead.

            #load up the filedialog chooser
            folder_selected = tk.filedialog.askdirectory(initialdir = self.file_directory, title = "Browse files for a stack") #browse directories

            #collect the images contained in the folder if there are any
            possible_images = []
            for item in os.listdir(folder_selected):
                for filetype, accepted in FILETYPES_ACCEPTED.items(): #above True or False can be placed against each file type such as .npy or .jpg (filetype is extension & accepeted boolean)
                    if accepted:
                        if item.endswith(filetype): #has to be a file allowed

                            item_wo_ext =  item[:-len(filetype)] #Here I am checking that the images are not sus or nor & the images that are sent through are correct. This is something that is only applicable to the MRI Slices
                            allowed = True #Use a simple change of bool structure, if it does end with nor or sus then this changes to False & the img won't be added to the final list
                            for type in NPY_FILES_TYPES_NOT_WANTED:
                                if item_wo_ext.endswith(type):
                                    allowed = False
                            if allowed:
                                possible_images.append(str(item)) #store the files in (keep extension as later on differentiate between .npy and .jpg to load)

            #if there are allowed files in the folder
            if len(possible_images) > 0:
                #On Windows, files are loaded in order they are in dir. In linux this is not the case therefore I have sorted the list by string
                #this is assuming that the slice names are the same apart from slice name.
                #Future Development: do sorting upon slice number rather than whole string
                #Eli Courtwright and skolima. How to sort a list of strings? (2011) [Online]. Available at: https://stackoverflow.com/questions/36139/how-to-sort-a-list-of-strings [Accessed: 19 September 2020]
                possible_images = sorted(possible_images)


                slice_address_segments = re.split("/", folder_selected) #split directory address as patient number, scan type etc are labelled by folder names

                self.create_tab(slice_address_segments, notebook_frame, folder_selected, possible_images)  #create the tab with the segements from the file

                #Future Development - Make this dynanmic
                if comparison == True and len(notebook_frame['tabs']) == 1:
                    self.set_comparison() #looks to see if the page needs splitting up after load
                ##**

                self.other_btns.enable_btn("close all tabs") #enable close btn as now tab is present
                self.unlock_comparison_stacks_btn() #enable the load second stack button as will always be one stack open. Future Development - this would be done dynanmically

            else: #if there are no files in the directory that are allowed for the program
                messagebox.showerror("Error Loading " + GROUP_OF_FILES_NAME, "There are no viewable files available within this folder.") #there were no images of the type desired in the folder
        except FileNotFoundError:
            print("Directory not chosen.") #If directory is not chosen by user.
        except:
            print("ERROR, Loading Stack or Slice.") #for general errors

    #Function to remove all tabs that are present on the screen. eg. to start again, or close session
    def remove_tabs(self):
        if len(self.all_tabs) > 0: #if there are tabs then destroy them
            for tab in self.all_tabs:
                tab['tab_pane_frame'].destroy() #destroy each tab frame which is located in the above dict self.all_tabs when it is created.

        self.all_tabs.clear()  #clear the tabs list as none are present now

        for notebook in self.notebook_frames: #clear all tabs from notebooks
            notebook['tabs'].clear()
            if notebook['slice_information'] != None:
                self.remove_and_nullify_slice_information(notebook) #need to nullify the information box located in the header regarding stack info

        self.comparison_open = False #There is no comparison window open
        self.other_btns.disable_btn("close all tabs") #disable close btn as no tabs to close
        self.comparison_open = True #Needs to be True even if there are no comparisons open as will reset screen to just one grid column
        self.unlock_comparison_stacks_btn() #to lock the comparison btn - FUTURE DEVELOPMENT - make more dynamic
        self.set_comparison() #to change the setup of the screen
        self.current_figures.clear() #as no current figures
        self.synchronised_figures.clear() #clear all synchronised figures as there will be now no synchronised figures

    #Updates the viewing information in the Information Box for each slice
    def update_viewing_information(self, notebook):
        #There has to be a tab in existence
        if len(notebook['tabs']) > 1:
            #FUTURE DEVELOPMENT - look at how this tab values can be generated & pass down better, currently just using tab name haha
            text = notebook['notebook'].tab(notebook['notebook'].select(), "text")
            #FabienAndre. (2012) Finding the currently selected tab of Ttk Notebook [Online]. Available at: https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook [Accessed: 19 August 2020]
            text = re.split(" | ", text) #get the name of the tab from the notebook, remember it is split via pipe
            #change currently viewing on tab select not load of scans
            figure_information = {"year": text[0], "scan type": text[2], "patient":text[4]}
            notebook['slice_information'].refresh_information(figure_information) #refresh the information for the notebook informationbox

    #Function for unlocking the comparison stacks buttons
    def unlock_comparison_stacks_btn(self):
        if len(self.all_tabs) > 0:
            self.load_stacks_buttons.enable_all_btns() #load comparison stack button is now enabled if more than 1 tab present
        else:
            self.load_stacks_buttons.change_to_default_states() #load comparison stack button goes back to disabled, load stack to normal

    #Function that looks to swap a tab from one notebook to another & updates relevent lists
    def swap_tab(self, direction, current_notebook, destination_notebook):
        #Cannot just swap tab over as cannot change parent frame in tkinter. I tried creating a change_notebook functionality in tab!
        #A new tab has to be created
        tab_index = current_notebook['notebook'].index("current") #get the current index of the tab in the notebook which will be the same as the tabs list for notebook in dict
        tab = current_notebook['tabs'][tab_index] #get that tab dict which will contain the id
        tab_id = tab['id'] #get id of tab

        self.create_tab(tab['tab_figure_slice_address'], destination_notebook, tab['folder_dir'], tab['sister_slices']) #create new tab for the new tab

        current_notebook['notebook'].forget(current_notebook['notebook'].select()) #remove the tab from the notebook
        current_notebook['tabs'] = [item for item in current_notebook['tabs'] if item['id'] != tab_id] #remove the tab if it has the same id

        #Button & grid styling depending on direction
        #FUTURE DEVELOPMENT - NEED TO MAKE DYNAMIC - only allow the right to left btn active if btn in left hand
        self.swap_tab_btn_status_changer()
        ##**

        #forget the information box if no tabs in
        for notebook_frame in self.notebook_frames:
            if (notebook_frame['slice_information'] != None) and len(notebook_frame['tabs']) == 0:
                self.remove_and_nullify_slice_information(notebook_frame)

        #FUTURE DEVELOPMENT
        #- transfer current slice over as will refresh to start slice
        #- transfer 'state' of figure eg. if polygon selected etc - transfer over
        #- not tested with synchronisation on

    #Function that resets the screen to one notebook, of course comparison_open would be set to false
    def reset_to_one_notebook(self):
        for i in range((len(self.notebook_frames))):
            if i == 0:
                self.tab_area.columnconfigure(i, weight=1) #weight to first column
            if i > 0:
                self.notebook_frames[i]['parent_frame'].grid_forget()
                self.tab_area.columnconfigure(i, weight=0) #second one has to be weight 0 & has to be stated to override
        self.comparison_open = False # comparison is now false as there are no frames on the right hand side

    #A function that changes the swap tb button status according to number of tabs open in each notebook
    #FUTURE DEVELOPMENT - Make this more dynanmic
    def swap_tab_btn_status_changer(self):
        for btns in self.swap_tab_btns: #contains the arrow btns
            if len(btns['right_hand_frame']['tabs']) == 0: #if there are no tabs open in right hand notebook then reset to one notebook
                btns['button_class'].forget_btns() #forget the comparison buttons as not needed as only one notebook open
                self.reset_to_one_notebook() #reset the screen to just one notebook
            elif len(btns['left_hand_frame']['tabs']) == 1: #if there is 1 tab in left hand frame then prevent moving this to the right
                btns['button_class'].disable_btn(">")
            elif len(btns['left_hand_frame']['tabs']) > 1: #if there is >1 tab open in left hand frame then allow this to move to right
                btns['button_class'].enable_btn(">")

    #OTHER METHODS
    #Function that opens the settings config & when closes if the result is that there is a change then refreshes the SliceFigures
    def open_settings_config(self):
        result = PolygonSettings(SETTINGS).send() #create Settings class (ref. in polygon settings class)
        if result and len(self.current_figures) > 0: #if there are current figures and there was a True response from exiting the Settings Window (means there was a change made)
            self.refresh_figures() #refresh all figures

    #This is used to refresh the slice figure class for settings that are configuable. I don't delete the tab due to UX comfort
    def refresh_figures(self):
        for figure in self.current_figures:
            figure.refresh() #call refresh method in SliceFigure class (refreshes the polygons on figure) eg if there was a change to the figure externally like a line thickness change

    #Just a quick method that removes the slice_information box & replaces the value with None
    def remove_and_nullify_slice_information(self, notebook_frame):
        notebook_frame['slice_information'].make_box_go_walkies() #forget the slice_information box which is attached to this notebook
        notebook_frame['slice_information'] = None

    #SYNCHRONISATION METHODS
    #if synchronisation is clicked then this method from SliceFigure is called (parent is passed through when SliceFigure is called)
    #figure_information is passed though of which tab is clicked for synchronisation
    def sync_tabs(self, figure_information):
      #FIND OTHER TABS THAT SATISFY SAME YEAR & PATIENT DATA
      if len(self.current_figures) > 1: #If there are multiple figures present
        figures_to_be_synced = []
        for figure in self.current_figures:
              #don't sync tabs if they are the same scan type of the same patient
              if (figure.figure_information['patient'] == figure_information['patient'] and figure.figure_information['year'] == figure_information['year']):
                  figures_to_be_synced.append(figure) #only append figures to be synced if they have same patient & year details

        #If there are multiple figures to be synced then can continue
        if len(figures_to_be_synced) > 1:
            filedir = self.file_directory + "/" + figure_information['year'] + "/" + figure_information['patient'] + "/01/" + figure_information['scan type'] #locate the folder that is clicked sync on


              #Get the slice transformation matrix for the file where synchronise is clicked FOR STACK A **WRONG**
              # first_slice_matrix = None
              # for item in os.listdir(filename):
              #     if item.endswith('.json') and not item.endswith('_polygon_slice_notes.json'):
              #         first_slice_matrix = TransformationMatrixFinder(filename, item[:-5]).get_transformation_matrix()
              #         break

            #STACK A Information: for each slice with polygons on it get: polygon data, slice number, slice transformation
            stack_information = []
            for item in os.listdir(filedir):
                  if item.endswith('_polygon_slice_notes.json'): #if there is polygons on the slice then there will be a polygon_slice notes file
                      file = filedir + "/" + item #get the json file
                      # print("FILE", file)
                      slice_name = item[: -(len(figure_information['scan type']) + len("_polygon_slice_notes.json") + 1)]
                      # print("Slice", slice_name)
                      json_reader = jsonFileReaderWriter(file, "polygon data")
                      slice_data = json_reader.read_file() #will return [] if no polygon data & only slice notes in file, the jsn reader will add an empty list if the key is not present
                      polygon_data = json_reader.read_key_data() #returns just the polygon data

                      if polygon_data != []: #if there is data then get slice transformation matrix WHAT IF NO MATRIX FILE
                          #GET TRANSFORMATION MATRIX PER SLICE
                          slice_transformation = TransformationMatrixFinder(filedir, item[: -(len("_polygon_slice_notes.json"))])
                          matrix = slice_transformation.get_transformation_matrix() #using slice transformation for each slice
                          #USING FIRST TRANSFORMATION OF STACK A
                          # matrix = first_slice_matrix

                          if matrix != None: #If the matrix is found then returns a value, otherwise will return None
                            slice_data = {"slice_num": int(slice_name[-3:]), "polygon_data": polygon_data, "slice_transformation_matrix": matrix} #Slice name [-3:] gets just the number of the slice
                            stack_information.append(slice_data) #add slice information to a list for this stack

            #For instance in the case of adc or adcq becuase they have no transformation matrix for each slice & becuase the synchronising stack requires a matrix for each slice that has polygons on it. It is not possible.
            #To avoid confusion, it WOULD be possible to synchronise to a adc or adcq as the only transformation matrix used is the first slice and DWI can be used.
            if len(stack_information) > 0:
                synchronised_stack = {"figure": figure_information, "stack": stack_information} #This is the information for the synhcronised stack
                self.synchronised_figures.append(synchronised_stack) #I append this to a list as there could be multiple different syncrhonisations at the same time
                # print(synchronised_stack)

                #Change the button details for each stack & pass the syncrhonised details into each figure
                # try:
                for figure in figures_to_be_synced:
                    figure.sync_btn['text'] = 'Tab Synced' #change button name
                    figure.sync_btn['background'] = colour_scheme['error_font'] #change button colour so it's similar to being 'live'
                    figure.sync_btn['foreground'] = colour_scheme['font_col']
                    figure.sync_tooltip.change_hover_text("Remove Sync") #change hover text

                    figure.synchronised_status = True #this figure is now synchronised
                    figure.synchronise_stack(synchronised_stack) #pass through syncrhonised details

                      # print("SYNCED STACK", synchronised_stack['figure'])
                      # print("\n")
                      # for slice in synchronised_stack['stack']:
                      #     print("\n")
                      #     print("SLICE", slice)

                # except: #if there is any error regarding synchronisation such as if transformation matrices that are needed have not been found
                #     print("ERROR_SYNC_F")
                #     print("There was an error with syncrhonising tabs. Synchronisation not completed. ")  #Theres not two tabs open with the same patient & year. Let user know
                #     messagebox.showerror("Synchronisation not possible", "An error has occured when synchronising. Synchronsing has not been completed", icon='error')
                #     return None


            else: #as there are no transformation matrices for the syncrhonising tab. Please refer to explanation above.
                print("The synchronising tab scan type has no transformation matrices available. ")  #Theres not two tabs open with the same patient & year. Let user know
                messagebox.showerror("Synchronisation not possible", "The synchronising tab's scan type has no transformation matrices available for this year and patient.", icon='error')
                return None

        else:
            print("Needs to be at least two tabs open with the same patient & same year. ")  #Theres not two tabs open with the same patient & year. Let user know
            messagebox.showerror("Synchronisation not possible", "At least two tabs with the same patient and year need to be open to syncrhonise.", icon='error')
            return None
      else:
          print("Needs to be at least two tabs open with the same patient & same year. ") #Theres not two tabs open. Let user know
          messagebox.showerror("Synchronisation not possible", "At least two tabs with the same patient and year need to be open to syncrhonise.", icon='error')
          return None

      #SYNCHRONISE STACKS CODE
          # 1) get slice information for slices with polygons, slice info includes polygon coords & info, slice transformation matrix, slice name
          # 2) get transformation matrix of target stack first slice
          # 3) multiply matrices of each slice A with homogenous coords of polygons
          # 4) find inverse of target stack matrix
          # 5) multiply inverse with 3.
          # 6) new z value is offset of slice num for which matrix was used in target stack

    #If a tab in unsynchronised. Reset btn, & status of tab. Remove synchronisation from the list of synchronisations. Again called by SliceFigure
    def unsync_tabs(self, figure_information):
        for figure in self.current_figures:
            if (figure.figure_information['patient'] == figure_information['patient'] and figure.figure_information['year'] == figure_information['year']): #check validation of details
                #FUTURE DEVELOPMENT - create an original version of this to just be reset. Maybe a class
                figure.sync_btn['text'] = 'Synchronise' #reset all wording
                figure.sync_btn['background'] = colour_scheme['secondary_btn_col']
                figure.sync_btn['foreground'] = colour_scheme['secondary_fg']
                figure.sync_tooltip.change_hover_text("Sync Stacks\nPatient: " + figure_information['patient']) #change the hover tooltip text

                figure.synchronised_status = False
                figure.translated_polygons.clear()
                figure.refresh() #refresh the loading of the polygons as translated polygons might be on view.

        #remove patient & year stack from currently synchronised list
        self.synchronised_figures = [item for item in self.synchronised_figures if item['figure']['patient'] != figure_information['patient'] and item['figure']['year'] != figure_information['year']]
        # print("synhcronised figs", self.synchronised_figures)


#Class for the Figure generated by selecting a folder from the load stacks method. Creates the figure that exists within the tab.
class SliceFigure:
    def __init__(self, tab_frame, folder_selected, slice_list, username, figure_information, parent):
        self.frame = tab_frame #the frame of the tab where the Figure is placed
        self.folder_selected  = folder_selected #directory information of the folder selected
        self.slice_list = slice_list #slices of the sibling in the folder, for interating over by button
        self.username = username #username of individual in session
        self.figure_information = figure_information #figure information eg. patient/scan type/year
        self.parent = parent #parent frame passed through

        self.translated_polygons = []

        self.current_position = 0 #Current position for the slice. Tab always begins at 0
        self.slice_name = self.current_slice_name_getter() #current slice name - in text of label frame when tab loads, changed by arrow btns through slice stack

        original_slice_name = (self.slice_name[:-(len(self.figure_information['scan type']) + 1)]) #the slice number is always before the scan type of this scan type in the filename. I add 1 as there is always an underscore
        self.first_slice_num = int(original_slice_name[-3:]) #convert to int & just get num



        self.intro_label_frm_txt = GROUP_OF_FILES_NAME + ":" #intro text to the label frame, group files name is MRI STACK
        self.synchronised_status = False #This is changed if the figure is synced
        self.selected_polygon = None #this is updated by child classes such as Polygons to then let Notebox know that a polygon is selected

        #start off settings that can be changed
        self.settings = SETTINGS
        self.figure_background = self.get_setting("Figure Background") #the current figure background setting - colour hex value
        self.default_tag_index = self.get_setting("Default Tag") #the index of the current tag in the tag list

        #FRAME inc HEADER & GRAPH
        self.graph_frame = tk.Frame(self.frame, background=colour_scheme['header_bg'])
        self.graph_frame.pack()

        #HEADER
        #FRAME HOLDER
        #FUTURE DEVELOPMENT - there are two frames here, sort it out mate.
        self.graph_frame_header = tk.Frame(self.graph_frame, background=colour_scheme['header_bg'])
        self.graph_frame_header.pack(side="top", fill="x", padx=10, pady=(10, 0))

        for i in range(3): #split out the header of the figure
            self.graph_frame_header.grid_columnconfigure(i, weight=1) #evenly space out the labels

        header_frame = tk.Frame(self.graph_frame_header, bg=colour_scheme['header_bg'])
        header_frame.grid(row=0, column=0, columnspan=3, sticky="WNSE", padx=10)

        #TAG DROPDOWN - START DROPDOWN (INSIDE HEADER - LEFT)
        #FUTURE DEVELOPMENT - make this more understandable to user
        self.polygon_tag_frame = tk.Frame(header_frame, background=colour_scheme['header_bg'])
        self.polygon_tag_frame.pack(side="left")

        self.polygon_tag_var = tk.StringVar(self.frame)
        self.polygon_tags = self.load_tags() #load the current tags to fill the dropdown

        self.polygon_tag_var.set(self.polygon_tags[self.default_tag_index])
        self.polygon_tag_chosen = self.polygon_tag_var.get() #assign variable to default

        self.polygon_tag_lab = tk.Label(self.polygon_tag_frame, text="Current Tag: ", background=colour_scheme['header_bg'], fg=colour_scheme['font_col']) #current assigned tag for drawing, can be changed by default in settings
        self.polygon_tag_lab.grid(row=0, column=0, sticky="W")
        self.polygon_tag_tooltip = HoverToolTip(self.polygon_tag_lab, colour_scheme['hover_bg'], fonts['small_font'], "Choose tag for new polygon") #to make the current tag a little more understandable. That this is the tag for any new polygons to be drawn

        self.polygon_tag_choice = ttk.Combobox(self.polygon_tag_frame, values=self.polygon_tags) #Use ttk. combo box as looks more appealing
        self.polygon_tag_choice.current(self.default_tag_index) #current value in the combo box
        self.polygon_tag_choice.grid(row=0, column=1, sticky="W", padx=5)

        self.polygon_tag_choice.bind("<<ComboboxSelected>>", self.change_tag) #when the tag changed, reassign the variable for the tag

        #MESSAGE LABEL & MESSAGE BOARD BG (INSIDE HEADER - CENTRAL)
        self.message_box = tk.Frame(header_frame, bg=colour_scheme['grey_bg'], relief="ridge", borderwidth=3) #a frame to almost have a the look of a message on a notice board. Positive text as lighter background
        self.message_box.pack(side="left", fill="both", padx=10, expand=True)

        self.information = tk.Label(self.message_box, background=colour_scheme['grey_bg']) #information label
        self.information.pack(pady=10, padx=10)

        #SYNCHRONISE BTN (INSIDE HEADER - RIGHT)
        self.sync_btn = tk.Button(header_frame, text="Synchronise", command=self.synchronise, width=13) #I have set the width of this button as text changes

        if SYNCHRONISATION: #if synchronisation is false then the message board pushes over to the right hand side. For instance for delineating images where sync not wanted
            self.sync_btn.pack(side="right")
            self.sync_tooltip = HoverToolTip(self.sync_btn, colour_scheme['hover_bg'], fonts['small_font'], "Sync Stacks\nPatient: " + self.figure_information['patient']) #tooltip for the synchronise btn

        #GR
        #Graph Frame - label frame containing the figure & toolbar
        self.fig_frame = tk.LabelFrame(self.graph_frame, text="  {} {} ".format(self.intro_label_frm_txt, self.slice_name), background=colour_scheme['header_bg'], foreground=colour_scheme['font_col'])
        self.fig_frame.pack(padx=10, pady=(0, 10))
        #The inner frame changes according to figure_background setting to offer some top & bottom padding to the figure (I have changed the fig size to save space but it removes all top/bottom padding)
        self.fig_frame_inner = tk.Frame(self.fig_frame, background=self.figure_background)
        self.fig_frame_inner.pack()

        #FIGURE, AXIS, CANVAS
        #FUTURE DEVELOPMENT - create figure class to contain all this & compartmenatise it
        self.figure = Figure() #call the matplotlib figure
        self.a = self.figure.add_subplot(111) #only one chart. Other axis settings are within function reset_axis()

        self.figure.patch.set_facecolor(self.figure_background) #patches the facecolour of the figurebackground ilke444. (2020) How to put color behind axes in python? [Online]. Available at: https://stackoverflow.com/questions/60480832/how-to-put-color-behind-axes-in-python [Accessed: 25 July 2020].
        self.figure.subplots_adjust(left=0,right=1,bottom=0,top=1) #This reduces the size of the figure somewhat  user3006135. (2018) How to remove gaps between subplots in matplotlib? [Online]. Available at: https://stackoverflow.com/questions/20057260/how-to-remove-gaps-between-subplots-in-matplotlib [Accessed: 25 July 2020].
        self.canvas = FigureCanvasTkAgg(self.figure, self.fig_frame_inner) #would normally run plot.show() but show in tkinter window here
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10) #pack it to the window

        self.fc = cidPress(self.figure) #class of cid for watching for button clicking
        self.cidHover = cidHover(self.figure) #For the hover over the graph

        #TOOLBAR
        #FUTURE DEVELOPMENT - add all customisation etc into the Toolbar class already created.
        self.toolbar = CustomToolbar(self.canvas, self.fig_frame, self.fc) # self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame) = I have used a CustomToolbar
        self.toolbar.config(background=colour_scheme['header_bg']) #change background of the toolbar ImportanceOfBeingErnest. (2018) How do you set the NavigationToolbar2TkAgg's background to a certain color in Tkinter [Online]. Available at: https://stackoverflow.com/questions/48351630/how-do-you-set-the-navigationtoolbar2tkaggs-background-to-a-certain-color-in-tk [Accessed: 18 July 2020]
        self.toolbar.update() #toolbar needs updating as changes made. See CustomToolbar class
        self.figure.canvas.mpl_connect('figure_leave_event', self.leave_figure) #I put in a fig leave event as I have adjusted the self.mode & set message
        #Matplotlib. Event handling and picking [Online]. Available at: https://matplotlib.org/3.1.1/users/event_handling.html [Accessed: 01 September 2020]
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.toolbar.children['!button6'].pack_forget() #to forget the configure subplots button as not needed

        #TOOLBAR CUSTOM BTNS
        #Frame
        custom_btn_frame = tk.Frame(master=self.toolbar, background=colour_scheme['header_bg'])
        custom_btn_frame.pack(side = "left")

        #Custom Buttons stored in a dict with name, function, default state
        #Any changes to Name key need to be also changed in button_images.py file
        self.custom_btns = [{"name": 'Jump to First Slice', "text": "1", "padding": (5, 1), "description": 'start', "dlft_state": "normal", "command": lambda name="start": self.click_tb_btn('start')},
                            {"name": 'Jump to Last Slice', "text": "END", "padding": (1, 2), "description": 'end', "dlft_state": "normal", "command": lambda: self.click_tb_btn('end')},
                            # {"name": 'Play Slice Slideshow', "text": "PLY", "padding": (5, 5), "description": 'play', "dlft_state": "normal", "command": lambda: self.click_tb_btn('play')},
                            {"name": "Draw Polygon", "text": "DRW", "padding": (0, 2), "description": 'draw', "dlft_state": "normal", "command": lambda name="draw": self.click_tb_btn("draw")},
                            {"name": "Select Polygon", "text": "SEL", "padding": (0, 2), "description": 'select', "dlft_state": "disabled", "command": lambda name="select": self.click_tb_btn("select")},
                            {"name": "Edit Polygon Vertex Locations", "text": "EDIT", "padding": (0, 2), "description": 'edit', "dlft_state": "disabled", "command": None},
                            {"name": "Delete Polygon", "text": "BIN", "padding": (0, 2), "description": 'delete', "dlft_state": "disabled", "command": None},
                            {"name": "Hide Polygons", "text": "ON", "padding": (0, 2), "description": 'hide', "dlft_state": "normal", "command": lambda name="hide": self.click_tb_btn("hide")},
                            {"name": "Edit Polygon Tag", "text": "TAG", "padding": (0, 2), "description": 'edit_tag', "dlft_state": "disabled", "command": None},
                            {"name": "Refresh Polygons", "text": "REF", "padding": (0, 2), "description": 'refresh', "dlft_state": "normal", "command": lambda name="refresh": self.click_tb_btn("refresh")},
                            {"name": "Create Mask", "text": "MASK", "padding": (0, 2), "description": 'create_mask', "dlft_state": "disabled", "command": None}
                            ]

        #FUTURE DEVELOPMENT - Decide on the play btn functionality

        #create the images for the buttons, uses PIL - look at widget_creator_classes file
        images = ConvertImages(custom_btn_images)
        self.imgs_custom_btns = images.prepare_images()

        #assign image to correct btn in dict above
        for item in self.imgs_custom_btns:
            for btn in self.custom_btns:
                if item['name'] == btn['name']:
                    btn['image'] = item['image']
        #Create the btns
        i = 0
        for btn in self.custom_btns:
            if btn['image'] != None: #if it's none then the image was not able to be loaded
                button = tk.Button(master=custom_btn_frame, image=btn['image'], command=btn['command'], state = btn['dlft_state'], width=24, height=24) #height & width same as standard
                btn['show_image'] = True #set that the image can be seen becuase it works
            else:
                print("ERROR with loading an image for toolbar button {}, text used instead.".format(btn['name']))
                button = tk.Button(master=custom_btn_frame, text=btn['text'], command=btn['command'], state = btn['dlft_state'] ) #height & width seem to make it play up
                btn['show_image'] = False #img cannot be seen

            btn['widget'] = button #assign button so can be manipulated at a later stage
            btn['hover_tooltip'] = HoverToolTip(button, colour_scheme['hover_bg'], fonts['small_font'], btn['name']) #setup the hover tooltip for the button & assign to dict
            button.grid(row=0, column=i, padx=btn['padding'])
            i += 1
            #I don't use text for these btns but use images
            #Beck, D, W. (2017) tkinter: how to replace a button with a image? Available at: https://stackoverflow.com/questions/47212078/tkinter-how-to-replace-a-button-with-a-image [Accessed: 09 July 2020].


        #LOAD UP FIGURE WITH SLICE
        try:
            self.create_figure(self.fig_frame) #create the figure
            self.canvas.get_default_filename = lambda: self.current_slice_name_getter() + "_img"  #changes the image placeholder name if image is saved. Used .img to differentiate between files with same name
            #Stop harming monica. (2017) How to change default filename from Matplotlib NavigationToolbar in a PyQt5 application? [Online]. Available at: https://stackoverflow.com/questions/41680007/how-to-change-default-filename-from-matplotlib-navigationtoolbar-in-a-pyqt5-appl [Accessed: 02 September 2020]

            #Following is for Play/Pause functionality *THIS IS CURRENTLY NOT LIVE*
            self.pause = False
            self.clicked = 0

            #Notebox Class is called to make this appear when calling Slice Figure
            self.notebox = Notebox(self.frame, self.username, self.current_slice_name_getter(), self.figure_information, self.folder_selected, self.slice_list)
        except:
            print("Error loading Slice")

        self.synchronised_information = None

        #If tab would be synchonised when it is loaded
        if len(self.parent.synchronised_figures) > 0:
            for sync in self.parent.synchronised_figures:
                if sync['figure']['patient'] == self.figure_information['patient'] and sync['figure']['year'] == self.figure_information['year'] and sync['figure']['scan type'] != self.figure_information['scan type']:

                        ##**THIS is repeated in class above**
                    try:
                        print("SYNC_H", self.figure_information)
                        self.sync_btn['text'] = 'Tab Synced'
                        self.sync_btn['background'] = colour_scheme['error_font']
                        self.sync_btn['foreground'] = colour_scheme['font_col']
                        self.sync_tooltip.change_hover_text("Remove Sync")

                        self.synchronised_status = True
                        self.synchronise_stack(sync) #synchronise stack
                    except: #if there is any error regarding synchronisation such as if transformation matrices that are needed have not been found
                        print("ERROR_SYNC_H")
                        print("There was an error with syncrhonising tabs. Synchronisation not completed. ")  #Theres not two tabs open with the same patient & year. Let user know
                        messagebox.showerror("Synchronisation not possible", "An error has occured when synchronising. Synchronsing has not been completed", icon='error')
                        return None

    #FIGURE, CANVAS, AXIS METHODS
    #Creates figure every time the user clicks the arrow buttons to change the slice
    def create_figure(self, graph_frame):
        self.fig_frame['text'] = "  {} {} ".format(self.intro_label_frm_txt, self.current_slice_name_getter()) #update label frame text for when slice changes
        self.reset_axis() #reset the axis, set grid off, axes off, clear axes etc for new slice (so slices don't sit on top of each )

        #Pull figure & use slice list
        slice_address = self.folder_selected + "/" + self.slice_list[self.current_position]
        read_slice = None

        if (slice_address.endswith(".npy")):
            slice = np.load(slice_address) #load a numpy figure
            read_slice = np.squeeze(slice)
        elif (slice_address.endswith(".png") or slice_address.endswith(".jpg")):
             read_slice = mpimg.imread(slice_address) #for loading an image eg in jpg or png format

        if read_slice.all() != None:
            self.a.imshow(read_slice, cmap=IMG_COLOURMAP) #show the fig, cmap relates to the setting set above. It is set at gray

            #this is for having the filename in the save fig dialog box
            self.canvas.get_default_filename = lambda: self.current_slice_name_getter() + "_img" #used img as ending to differentiate with files of same name. It will automatically look to save as .png

            self.filename = self.folder_selected + "/" + self.current_slice_name_getter() + "_polygon_slice_notes.json" #filename for json data on polygons & polygon notes & also slice notes
            self.jsonFileReaderWriter = jsonFileReaderWriter(self.filename, 'polygon data') #recall jsonfilewriter instance
            self.slice_polygons = Polygons(self.jsonFileReaderWriter, self.current_slice_name_getter(), self.figure, self.a, self.custom_btns, self.fc, self.information, self)

            #reset the tag in the tag box
            self.set_tag_to_default()

            self.canvas.draw() #draw figure
            self.determine_btn_status() #status of standard btns in matplotlib toolbar, eg. if slice was first in stack then disable left arrow btn

    #Function is for leaving the figure cursor, to let self.mode & self.setmessage of CustomToolbar know - see CustomToolbar class
    def leave_figure(self, event):
        self.toolbar.left_figure(event)

    #Function to draw the figure - this is so it can be called by Polygons too.
    def draw_figure(self, figure):
        figure.canvas.draw()

    #update the hover label, passed through the hovertooltip object. Will then update cidhover. It will disconnect previous hover & set new one
    def update_hover(self, class_obj):
        self.cidHover.disconnect() #disconnect old hover
        self.cidHover.connect(lambda e: class_obj.hover(e)) #connect new hover

    #reset the axis by clearing before new slice appears. Done within create_fig
    def reset_axis(self):
        self.a.cla() #clear hover Source: Zwicker D. and spinkus. (2018) When to use cla(), clf() or close() for clearing a plot in matplotlib? [Online]. Available at: https://stackoverflow.com/questions/8213522/when-to-use-cla-clf-or-close-for-clearing-a-plot-in-matplotlib [Accessed: 26 July 2020].
        self.a.grid(False) #remove grid lines
        self.a.axis("off") #removes axis
        self.a.format_coord = lambda x, y: "[{}, {}]".format(str(x)[:4], str(y)[:4])  #I change the coordinates by default here. However it is overriden in the custom toolbar method self.mode anyhow
        #tmdavison. (2016) Disable coordinates from the toolbar of a Matplotlib figure [Online]. Available at: https://stackoverflow.com/questions/36012602/disable-coordinates-from-the-toolbar-of-a-matplotlib-figure [Accessed: 26 July 2020].


    #SYNHCRONISATION METHODS
    #To sync already an open tab. It takes the syncrhonised information regarding the synchrised tab into the method & then translates each polygon for this particular figure
    def synchronise_stack(self, synchronising_stack_information):
        #Double verification almost to check this figure matches the synchronised figure
        if self.figure_information['year'] == synchronising_stack_information['figure']['year'] and self.figure_information['patient'] == synchronising_stack_information['figure']['patient'] and self.figure_information['scan type'] != synchronising_stack_information['figure']['scan type']:

            #GET FIRST SLICE OF STACK B TRANS. MATRIX

            #If scan is any of following then use DWI transformation matrix but keep rest same
            adc_scan_types = ["adc", "adcq", "adcq-res", "adc-res", "cdwi-1400", "cqdwi-1400", "kurtosis", "contrast-tra"]
            alternative_scan_type = "dwi-100_800_1000"

            if self.figure_information['scan type'] in adc_scan_types: #check that the synchronisee tab is not in these, if is then use dwi
                matrix_dir = self.folder_selected[:-len(self.figure_information['scan type'])] + alternative_scan_type #get dwi directory
                matrix_slice_file_used = None #if this is passed through below it will fail Try Except on synchronisation & therefore fail whole process.
                slice_json_file = self.slice_list[0][:-4] #KEPT TO ADC for now

                for item in os.listdir(matrix_dir): #use dwi directory
                    if item.endswith('.json') and not item.endswith('_polygon_slice_notes.json'): #check its not a polygon slice notes file
                        matrix_slice_file_used = item[:-5] #remove the json extension
                        break

            else:
                matrix_dir = self.folder_selected #directory for where the matrix is to be found
                matrix_slice_file_used = self.slice_list[0][:-4] #name of the json file for the first slice of this Figure's stack. Use the first slice's transformation matrix to translate the polygons against
                slice_json_file = self.slice_list[0][:-4] #name of the json file for the first slice of this Figure's stack. Use the first slice's transformation matrix to translate the polygons against

            #GET SLICE NUM  & MATRIX OF FIRST SLICE
            slice_name_of_trans_used_stack_b = (slice_json_file[:-(len(self.figure_information['scan type']) + 1)]) #the slice number is always before the scan type of this scan type in the filename. I add 1 as there is always an underscore
            slice_num_of_trans_used_stack_b = int(slice_name_of_trans_used_stack_b[-3:]) #just get the number & convert to int

            slice_transformation = TransformationMatrixFinder(matrix_dir, matrix_slice_file_used)
            first_slice_matrix = slice_transformation.get_transformation_matrix() #get the matrix for this figure's first slice


            #GET NEW TRANSLATED POLYGONS
            for slicefig in synchronising_stack_information['stack']: #iterate over each slice in the synchroniser stack for slices that contained polygons
                slice_matrix = slicefig['slice_transformation_matrix'] #get the matrix for the slice that the polygon was on in Stack A

                for polygon in slicefig['polygon_data']: #iterate over each polygon
                    #GET NEW COORDINATES FOR EACH POLYGON
                    translater = PolygonTranslater(slice_matrix, first_slice_matrix, polygon['co-ordinates'])
                    translated_polygon = translater.translate_polygon() #get the new translated cooridnates
                    translated_polygon = {"slice": "Translated " + polygon['slice'], "id": "Translated " + str(polygon['id']), "tag": polygon['tag'], "co-ordinates": translated_polygon} #I have included the translated wording for the hovertip

                    self.translated_polygons.append(translated_polygon) #append this translated polygons to a global variable for class. This variable can only be filled by one synchronisation at any one time

            #FIND SLICE NUMBERS USING z VALUE of TRANSLATED COORDINATES OF EACH POLYGON
            for polygon in self.translated_polygons:
                polygon_z_coords = []
                for coord in polygon['co-ordinates']:



                    #IF SLICE NUMBER IS RELATIVE TO TRANSFORMATION SLICE USED OF STACK B:
                    polygon_z_coords.append(round(coord[2]) + slice_num_of_trans_used_stack_b) #z coordinate #round as to get slice number

                    #"BELOW IS WRONG"
                    #IF SLICE NUMBER IS RELATIVE TO TRANSFORMATION SLICE USED FOR ORIGINAL POLYGON ON SLICE A:
                    # original_slice_name = (polygon['slice'][:-(len(synchronising_stack_information['figure']['scan type']) + 1)]) #the slice number is always before the scan type of this scan type in the filename. I add 1 as there is always an underscore
                    # original_slice_num = int(original_slice_name[-3:]) #convert to int & just get num
                    # polygon_z_coords.append(round(coord[2]) + original_slice_num) #z coordinate #round as to get slice number


                #Using set & then list it to make it subscriptble - REMOVE IDENTICAL VALUES - AS PLOTTING WHOLE POLYGON ON EACH SLICE
                polygon_z_coords = list(set(polygon_z_coords))

                #find the missing numbers
                missing_nums = self.find_missing(polygon_z_coords)

                #add missing numbers to the list of slice numbers
                for missing_number in missing_nums:
                    polygon_z_coords.append(missing_number)

                #srt the numbers
                polygon_z_coords = sorted(polygon_z_coords)

                #if there are more than 3 numbers then disregard slice numbers
                if DISREGARD_TRANSLATED_POLYGONS_WITH_GT_3_SLICE_NUMS: #this is a global variable that is set program wide
                    if len(polygon_z_coords) > 3: #this variable could be set program wide
                        polygon_z_coords = []

                # for z in polygon_z_coords:
                polygon['slice_numbers'] = polygon_z_coords #for each polygon add the slice numbers to the polygon dict, this variable has removed the duplicates & is the slice number of the new stack


        #PRINT TRANSLATED COORDINATES
        # print("TRANSLATED POLTGONS", self.translated_polygons)
        # for item in self.translated_polygons:
        #     print(item)
            #     print("\n")

            #As an opened tab may have polygons on screen - Need to add polygons to that axis, don't need to refresh
        self.check_and_send_trans_polygons()

    #Method to find the missing the numbers in a list of integers
    #Future development: add these type of methods to an operations class?
    def find_missing(self, numbers):
        #GeeksforGeeks. Python | Find missing numbers in a sorted range. [Online]. Available at: https://www.geeksforgeeks.org/python-find-missing-numbers-in-a-sorted-list-range/ [Accessed: 14 September 2020].
        return sorted(set(range(int(numbers[0]), int(numbers[-1]))) - set(numbers))
        #Pavel (2014). python "TypeError: 'numpy.float64' object cannot be interpreted as an integer" [Online]. Available at: https://stackoverflow.com/questions/24003431/python-typeerror-numpy-float64-object-cannot-be-interpreted-as-an-integer [Accessed: 14 September 2020].

    #Method that takes in the translated polygons & works out if there are any on the current position slice
    def check_and_send_trans_polygons(self):
        # print("TRANSLATED POLYGONS", self.translated_polygons)

        #if there are polygons to plot
        if len(self.translated_polygons) > 0:
            translated_polygons_drawn = []
            for polygon in self.translated_polygons:
                if (self.current_position + self.first_slice_num) in polygon['slice_numbers']: #if current position of the stack which starts at 0 + the first slice number is the same as one of these slice numbers then add the polygon to list that is to be drawn
                    translated_polygons_drawn.append(polygon)

            #if there are polygons then draw them
            if len(translated_polygons_drawn) > 0:
                self.slice_polygons.draw_polygons(translated_polygons_drawn)
                self.slice_polygons.update_hover_polygons() #update the hover. This does pass down to Polygons and then back up to SliceFigure
                #FUTURE DEVELOPMENT - Improve hover update as it is passing up and down like an uncontrollable yoyo

    #passes figure_information from the class where the sync was made up, will then call eithe sync_tabs or unsync tabs of parent.
    def synchronise(self):
        if not self.synchronised_status:
            #sync
            self.parent.sync_tabs(self.figure_information)
        else:
            #unsync
            self.parent.unsync_tabs(self.figure_information)


    #TAG METHODS
    #Function that loads tags using the TagFileLoader
    def load_tags(self):
        polygon_tags = []

        tags_writer = TagFileLoader(file_locations['tags'])
        tags = tags_writer.return_tags() #get tags

        for tag in tags:
            polygon_tags.append(tag['label'].capitalize()) #capitalise them

        return polygon_tags #return them

    #Called when the tag is changed, this is bound to the dropdown, ensures correct current tag is passed through
    def change_tag(self, event):
        self.polygon_tag_chosen = self.polygon_tag_choice.get()

    def set_tag_to_default(self):
        self.default_tag_index = self.get_setting("Default Tag")
        self.polygon_tag_var.set(self.polygon_tags[self.default_tag_index]) #set the value to the variable
        self.polygon_tag_choice.current(self.default_tag_index) #set the current value of the combo box
        self.change_tag(None) #need to then reassign this as the current tag is changed


    #BUTTON METHODS
    #Button that is called everytime a toolbar button is clicked, sets current position of stack accordingly
    def click_tb_btn(self, btn):
        self.fc.disconnect() #disconnect the CID - see figure classes for cid
        self.toolbar.unclick_pan_zoom() #ensure pan and zoom are not clicked as zoom for instance needs a click on the fig - don't want that interfering with zoom click

        if btn == 2 or btn == 3 or btn == "start" or btn == "end": #change figure commands
            if btn == 2: #2 is left arrow
                self.current_position -= 1 #postion is decrememented
            elif btn == 3: #3 is right arrow
                self.current_position += 1 #postion is incremented
            elif btn == "start": #first slice in stack
                self.current_position = 0
            elif btn == "end": #last slice in stack
                self.current_position = len(self.slice_list) - 1
            self.create_figure(self.fig_frame) #create figure
            self.notebox.update_slice_name(self.current_slice_name_getter()) #update slice name of notebox with new slice name

        #Not change figure commands
        # elif btn == "play":
        #     self.play_slideshow() #play the slideshow method
        elif btn == "draw":
            self.fc.connect(lambda event: self.slice_polygons.draw_btn_click(event, self.polygon_tag_chosen)) #click to draw
        elif btn == "select":
            self.fc.connect(lambda event: self.slice_polygons.select_polygon(event)) #click to select a polygon
        elif btn == "hide":
            self.fc.connect(self.slice_polygons.show_polygons()) #shows polygons or removes from view
        elif btn == "refresh":
            self.fc.connect(self.slice_polygons.load_polygons()) #load polygons just refreshs the polygons on the slice, incomplete polygons are not saved to json

    #Method to determine the status of the standard Matplotlib toolbar btns
    #FUTURE DEVELOPMENT - This is rubbish - make it more dynanmic
    def determine_btn_status(self):
        start_btn = self.custom_btns[0]['widget'] #to start btn
        end_btn = self.custom_btns[1]['widget'] #to end btn
        if self.current_position == 0: #disable left as cannot go left as current position is at start
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="disabled") # 2 is left
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="normal") #3 is right
            start_btn['state'] = "disabled"
            end_btn['state'] = "normal"
        elif (self.current_position == len(self.slice_list) - 1): #disable right as cannot go right as current position is at end
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="normal") # 2 is left
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="disabled") #3 is right
            start_btn['state'] = "normal"
            end_btn['state'] = "disabled"
        else:   #in middle of stack
            self.toolbar.children['!button2'].config(command=lambda: self.click_tb_btn(2), state="normal") # 2 is left
            self.toolbar.children['!button3'].config(command=lambda: self.click_tb_btn(3), state="normal") #3 is right
            start_btn['state'] = "normal"
            end_btn['state'] = "normal"

    #Method that plays the slideshow without any polygons
    def play_slideshow(self):
        #I built this primarily as I was interested in the sleep functionality of python - its not exactly a requirement so have not included it
        #THIS HAS NOT BEEN TESTED RECNTLY AND IS NOT LIVE
        #RealPython. Python sleep(): How to Add Time Delays [Online]. Available at: https://realpython.com/python-sleep/ [Accessed: 14 July 2020].
        self.clicked += 1 #i use a counter
        self.pause = True  #if pause clicked or not uses a boolean
        i = 0
        play_btn = self.custom_btns[2]['btn']
        #iterate through images
        while (self.clicked == 0) or (self.clicked % 2 != 0):
            for slice in self.slice_list:
                self.current_position = i
                self.create_figure(self.fig_frame)
                time.sleep(1.25) #sleep this much time on each slice
                i += 1
        if (self.clicked % 2 == 0):
            pass

        #reset back to first image
        self.current_position = 0 #if paused maybe do this.
        self.create_figure(self.fig_frame)



    #OTHER METHODS
    #Function that refreshes the slice figure if a setting is changed through config settings
    def refresh(self):
        self.settings = SETTINGS #get the up to date settings - WATCH with the settings, the original json file IS NOT changed but the TAGS one is
        #figure background change
        self.figure_background = self.get_setting("Figure Background")
        self.figure.patch.set_facecolor(self.figure_background) #doesn't need canvas draw, resets colour
        self.fig_frame_inner['background'] = self.figure_background #sets background of the inner frame

        #Refresh the tags
        self.set_tag_to_default()
        # self.default_tag_index = self.get_setting("Default Tag")
        # self.polygon_tag_var.set(self.polygon_tags[self.default_tag_index]) #set the value to the variable
        # self.polygon_tag_choice.current(self.default_tag_index) #set the current value of the combo box
        # self.change_tag(None) #need to then reassign this as the current tag is changed

        #load polygons
        self.slice_polygons.load_polygons() #reloads the polygons

        #load new tags & assign to dropdown
        self.polygon_tag_choice['values'] = self.load_tags()

    #Function called by child class Polygons to let this class know which polygon is selected to then update Notebox
    def get_selected_polygon(self, polygon):
        self.selected_polygon = polygon #reassign polygons
        self.notebox.set_selected_polygon(polygon) #set it in notebox so notebox can allow a note to be taken for a selected polygon

    #Function for updating the information label depending on type of message eg. positive or negative
    #FUTURE DEVELOPMENT - create a store of messages & make this further dynanmic
    def update_information(self, text, type):
        self.information['text'] = text #text is passed through
        if type == "positive":
            self.information['fg'] = colour_scheme['positive_font']
        elif type == "warning":
            self.information['fg'] = colour_scheme['error_font']
        else:
            self.information['fg'] = colour_scheme['secondary_fg']

    #Get setting method pulls a setting from self.settings & gets the current value
    def get_setting(self, setting_name):
        return [item['current_value'] for item in self.settings if item['setting'] == setting_name][0]

    #Function that pulls the current slice name from the slice stack & trims off the .npy off the end
    def current_slice_name_getter(self):
        return self.slice_list[self.current_position][:-4]


#POLYGONS CLASS on top of the FIGURE, methods include add vertex, select vertex etc.
#FUTURE DEVELOPMENT - THIS NEEDS MAJOR TRIMMING DOWN & COMPARTMENTALISATION - WAY TOO BIG & MESSY
class Polygons(SliceFigure):
    def __init__(self, file_writer, slice_name, f, a, polygon_buttons, cid, information_label, parent):
        self.file_writer = file_writer #file writer for adding data to slice's json file eg. adding a polygon
        self.slice_name = slice_name #slice name of slice
        self.figure = f
        self.axis = a
        self.fc = cid #mouse click
        self.polygon_buttons = polygon_buttons #buttons referred to toolbar
        self.information = information_label #message on message board
        self.parent = parent

        #TAGS & SETTINGS
        self.refresh_tags() #Tag Checker & pull tags

        #I call the SETTINGS variable that is initialised at the start of program. It is recalled in load_polygons (i.e when the slice is refreshed)
        self.settings = SETTINGS
        #Set the following settings
        self.precision = [item['current_value'] for item in self.settings if item['setting'] == "Precision"][0]
        self.line_thickness = [item['current_value'] for item in self.settings if item['setting'] == "Line Thickness"][0]
        self.select_col = [item['current_value'] for item in self.settings if item['setting'] == "Selected Polygon Colour"][0]

        #OTHER CLASS WIDE VARs
        self.polygon_num = 0 #IDs the polygons for that are drawn - need to be taken from json file
        self.polygons_visible = True #Boolean if poylgons are visible
        self.highlighted_points = [] #stores any highlighted points that are not part of polygons
        self.selected_polygon = None #stores the selected polygon at the time
        self.polygon_info = [] #stores polygons
        self.translated_polygon_info = [] #This stores the information for any translated polygons #remember this is refreshed every slice iteration

        #DRAWING POLYGON CLASS WIDE
        self.co_ordinates = [] #This is filled everytime a polygon is drawn, each coorindate is added
        self.num_of_lines = 0 #incrememnted every time a polygon is drawn

        #LOAD POLYGONS
        self.load_polygons() #load the polygons upon the slice loading

        #FUTURE DEVELOPMENT
        # - adding polygon class wide variables to be removed & add polygon to be given own class
        # - mouse click to be treated same as hover (pass through parent)

    #GENERAL METHODS
    #Following two methods are inherited from SliceFigure (parent)
    def update_information(self, text, type):
        super(Polygons, self).update_information(text, type) #Updates the information label or message that is displayed on the message board

    def draw_figure(self):
        super(Polygons, self).draw_figure(self.figure) #draws the fig to canvas

    #Refresh the tags by uploading the up to date file contents for tags
    def refresh_tags(self):
        tags_writer = TagFileLoader(file_locations['tags'])
        self.tags = tags_writer.return_tags()

    #DRAWING POLYGONS METHODS
    #Draw Polygons method - draws a dict of polygons passed through
    #FUTURE DEVELOPMENT - only used for translation currently, integrated this in self.load_polygons
    def draw_polygons(self, polygons):
        for polygon in polygons:
            xlist, ylist = [], []
            num_of_vertexes = 0
            for x, y, z, w in polygon['co-ordinates']: #FUTURE DEVELOPMENT - make this so it works for x, y too
                xlist.append(x)
                ylist.append(y)
                num_of_vertexes += 1 #caluclate the num of verteces
            xlist.append(polygon['co-ordinates'][0][0]) #rememember to add first co-ordinate for x so it connects up
            ylist.append(polygon['co-ordinates'][0][1])  #rememember to add first co-ordinate for y so it connects up
            #plot on axis
            poly = self.axis.plot(xlist, ylist, color=self.get_colour(polygon['tag']), marker="o", label=polygon['id'], linewidth=self.line_thickness)

            #create polygon object to be used upon edited - try and move away from polygon_info
            polygon_objs = {}
            polygon_objs['slice'] = polygon['slice']
            polygon_objs["id"] = polygon['id']
            polygon_objs["lines"] = poly
            polygon_objs["num"] = num_of_vertexes
            polygon_objs["tag"] = polygon['tag']

            polygon_objs["scatter_points"] = []
            polygon_objs["co-ordinates"] = polygon['co-ordinates']
            self.translated_polygon_info.append(polygon_objs) #pass info into this list here

        #draw to figure
        self.draw_figure()

    #function to load the polygons & draw them to the figure
    #FUTURE DEVELOPMENT -
    #1. Please use self.draw_polygons
    #2. This method has morphed into more of a reset method - construct it appropiatly
    def load_polygons(self):
        #assign polygon_info for slice, file will only contain co-ordinates, takes in full file
        file_info = self.file_writer.read_file()
        if file_info != None:
            file_sorted = self.file_writer.sort_file(file_info, "slice", self.slice_name)
        else:
            file_sorted = []
        #FUTURE DEVELOPMENT - remove this sorting as not needed as polygons have ids now

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

        self.fc.disconnect() #disconnect from the cid just in case a draw btn was clicked or something similar (mouse click)

        #Recall SETTINGS as changes within the session may have been made
        self.settings = SETTINGS
        self.precision = [item['current_value'] for item in self.settings if item['setting'] == "Precision"][0]
        self.line_thickness = [item['current_value'] for item in self.settings if item['setting'] == "Line Thickness"][0]
        self.select_col = [item['current_value'] for item in self.settings if item['setting'] == "Selected Polygon Colour"][0]

        #if polygons present then draw the polygons on the axis
        if len(slice_polygons) > 0:
            #update polygon_num with the num of the last polygon entry. it is default 0 otherwise
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
                self.polygon_info.append(polygon_objs) #assign the polygon information to the class wide variable

            #draw to figure
            self.draw_figure()
        #if else no polygons are present for this slice

        #reset the polygon buttons to default
        #FUTURE DEVELOPMENT - this is simiar to show polygons method - link in & trim down - reset needs to be cleaner
        for button in self.polygon_buttons:
            if button['description'] == "hide":
                button['hover_tooltip'].change_hover_text(button['name']) #change text in tooltip to display that polygons will be shown
                if button['show_image']:
                    for image in self.parent.imgs_custom_btns: #the images have been already converted in the parent so a case of calling that
                        if image['name'] == "Hide Polygons":
                            button['widget']['image'] = image['image']
                else:
                    button['widget']['text'] = button['text'] #change the text for show polygons btn if the image is not used
            else:
                button['widget']['state'] = button['dlft_state'] #set all other buttons to default states

        #MORE RESET CHECKS DONE
        self.check_if_polygons_present() #if polygons present then select button is enabled
        self.check_polygon_selected() #if no polygon selected then edit/remove btns disabled
        self.selected_polygon = None #no selected polygon currently
        self.update_information("Click the pencil to start drawing!", "positive") #messege

        #reset the hover object
        self.hover_obj = PolygonHover(self, self.polygon_info, self.precision, self.figure, self.axis, self.select_col) #calling the hover class
        self.parent.update_hover(self.hover_obj)

        #get the translated polygons & ask draw polygons to draw them if there are any. This is getting a little messy going up and down. Re-organise!
        self.parent.check_and_send_trans_polygons()  #Need to call after original hover, as this resets the hover


    #Draw btn is clicked - calls add vertex method
    #FUTURE DEVELOPMENT - Create add vertex Class to do this
    def draw_btn_click(self, event, tag):
        self.add_vertex(event, tag)

    #used for ID purposes for the polygon counter when one is drawn
    def polygon_counter(self):
        #just increments the polygon num by one
        self.polygon_num += 1
        return self.polygon_num

    #Function to add a vertex & draw a polygon, then save it
    def add_vertex(self, event, tag):
        colour = self.get_colour(tag) #get the colour of the newley drawn polygon

        #reset polygon selected to be None, colours, remove highlighted pts etc
        self.selected_polygon = None
        self.reset_polygon_cols(True) #reset all polygon colours when draw is clicked
        self.check_polygon_selected() #reset polygon selected
        self.remove_highlighted_points()

        #first plot that is made by user
        label = str(self.polygon_num + 1) + " polygon"
        if not(event.xdata == None and event.ydata == None): #in case the user clicks the white border area
            if len(self.co_ordinates) == 0: #for first plot

                self.co_ordinates.append([event.xdata, event.ydata])
                a = self.axis.scatter(event.xdata, event.ydata, s=30, color=colour) #create the scatter point so can be edited and the lines would move ?
                self.draw_figure()
                self.num_of_lines +=1 #increment the number of lines - this is used to then assign the correct recently matplotlib line objs to the polygon

            #For last plot that is made by user eg. the final plot or clicking the first co-ordinate of the polygon
            elif (np.abs(self.co_ordinates[0][0] - event.xdata) < self.precision) and (np.abs(self.co_ordinates[0][1] - event.ydata) < self.precision) and (len(self.co_ordinates) > 2): #np.abs allows the number to be positive only
                #over 2 as have to have at least 3 lines


                #Work on trying to prevent polygon intersect with itself
                #FUTURE DEVELOPMENT - get this to work
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
                    # print("RESULT", result)
                    #If there is no intersection - it is false
                if not intersector_other or result == "yes": #if the user said yes then they override the intersection

                    self.co_ordinates.append([self.co_ordinates[0][0], self.co_ordinates[0][1]]) #re-add the co-ords of the first point

                    coords = self.create_x_y_list(self.co_ordinates) #returns x at index 0, y at 1
                    label = label + "final" ##**CHANGE TO BELOW**
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
                    record = {"id": id, "slice": self.slice_name, "tag": tag, "co-ordinates": self.co_ordinates}
                    self.file_writer.add_record(record)

                    #update information label
                    self.update_information("Polygon with id: {} saved successfully".format(str(id)), "positive")

                    #reset details as polygon has been completed
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
                    a = self.axis.scatter(event.xdata, event.ydata, s=30, color=colour) #plot to the axis
                    self.update_information("Plot plotted successfully.", "positive") #update message

                    coords = self.create_x_y_list(self.co_ordinates) #returns x at index 0, y at 1
                    label = label + "line"
                    v = self.axis.plot(coords[0], coords[1], color=colour, marker="o", label=label, linewidth=self.line_thickness)
                    self.draw_figure()
                    self.num_of_lines +=1 #increment as a line has been added
                else:
                    if intersector_other:
                        self.update_information("Intersection Found with another Polygon. Plot cannot be made", "warning")
        else:
            self.update_information("MRI Slice not clicked.", "warning")


    #SELECT POLYGON METHODS
    #Method that passes up the selected polygon into the parent obj - it is then passed into notebox to be the name of the polygon notes tab etc
    def get_selected_polygon(self):
        self.parent.get_selected_polygon(self.selected_polygon)

    #Function changes the state of the buttons depending on whether there is a polygon selected or not
    def check_polygon_selected(self):
        #FUTURE DEVELOPMENT - make this dynanmic
        #if a polygon is selected or not selected buttons change states accordingly
        if self.selected_polygon != None:
            for button in self.polygon_buttons:
                if button['description'] == "delete":
                    button['widget']['state'] = "normal" #this and all the btns below become alive now
                    button['widget']['command'] = lambda polygon=self.selected_polygon: self.del_btn_click(polygon)
                elif button['description'] == "edit":
                    button['widget']['state'] = "normal"
                    button['widget']['command'] = lambda polygon=self.selected_polygon: self.edit_btn_click(polygon)
                elif button['description'] == "edit_tag":
                    button['widget']['state'] = "normal"
                    button['widget']['command'] = lambda polygon=self.selected_polygon: self.edit_tag(polygon)
                elif button['description'] == "create_mask":
                    button['widget']['state'] = "normal"
                    button['widget']['command'] = lambda polygon=self.selected_polygon: self.create_mask(polygon)

        #if polygon not selected then reset btns back to disabled
        else:
            buttons = ['delete', 'edit', 'edit_tag']
            for button in self.polygon_buttons:
                if button['description'] in buttons:
                    button['widget']['state'] = button['dlft_state']
                    button['widget']['command'] = None #command is reset back to None

    #For when the select btn is clicked, if select btn is clicked then when click graph select polygon is func called
    def select_btn_click(self):
        self.fc.disconnect() #disconnect the mouseclick as click on figure is now searching for vertex
        self.fc.connect(lambda event: self.select_polygon(event))

    #Select a Polygon
    def select_polygon(self, event):
        #clear any outstanding incomplete drawing objs from axis if select btn clicked
        self.reset_polygon_cols(True)
        self.remove_highlighted_points() #remove any highlighted pnts from previous editing

        #I have not cleared the axis when a polygon is selected to rid it of unfinished polygons as the user may be looking to move other polygons out the way to then continue for instance

        #Select Polygon
        polygon_selected = False #polygon selected is false by default
        if not(event.xdata == None and event.ydata == None): #in case the user clicks the white border area
            for d in self.polygon_info: #checks each x, y coordinate
                for x, y in d['co-ordinates']:
                    # print(x, y)
                    # print("prec", self.precision, type(self.precision))
                    if (np.abs(x - event.xdata) < self.precision) and (np.abs(y - event.ydata) < self.precision): #np.abs allows the number to be positive only
                        polygon_selected = True #if the coordinates validate then, a polygon is selected!
                        self.selected_polygon = d #assign selected poylgon
                        self.get_selected_polygon() #send it up to parent class to go in notebox tab etc
                        self.update_information("Polygon {} selected. Click off polygon to deselect.".format(d['id']), "positive") #update messege

                        #Convert colours of selected polygon to selected colour & draw fig
                        self.show_selected_plots(self.selected_polygon['scatter_points'], self.axis.collections, self.select_col)
                        self.show_selected_plots(self.selected_polygon['lines'], self.axis.lines, self.select_col)
                        self.draw_figure()

        #if click elsehwere then deselect all polygons as no polygon is selected
        if not polygon_selected:
            self.update_information("No polygon selected, make sure you click a vertex!", "warning") #tell the user
            self.selected_polygon = None
            self.get_selected_polygon()
            self.reset_polygon_cols(True) #resets the colours back to their original colours

        self.check_polygon_selected() #this amends the button states depending on button selection


    #SHOW POLYGON METHODS
    #A function to show/remove from view polygons, I do call the json to show so they cannot switch here and there if polygon is half complete
    def show_polygons(self):
        self.fc.disconnect() #disconnect from the cid just in case a draw btn was clicked or something similar

        #if polygons are visible then hide them & change btns appropiately
        if self.polygons_visible:
            for button in self.polygon_buttons:
                if button['description'] == "hide":
                    button['hover_tooltip'].change_hover_text("Show Polygons") #change text in tooltip to display that polygons will be shown

                    if button['show_image']: #only use the second image if the first was loaded for consistency
                        for image in self.parent.imgs_custom_btns: #the images have been already converted in the parent so a case of calling that
                            if image['name'] == "Polygons Hidden" and image['image'] != None: #if image is equal to None then there may have been an error in loading that img
                                button['widget']['image'] = image['image']
                    else:
                        button['widget']['text'] = 'OFF' #change the text for show polygons btn if the image is not used
                else:
                    button['widget']['state'] = "disabled" #disable all other buttons if no polygons
            self.clear_axis_data() #clear axis data which draws figure
            self.polygons_visible = False #polygons are now hidden
            self.update_information("Polygons currently hidden.", "warning") #let user know
            self.selected_polygon = None #polygon is not selected as they are hidden
            self.get_selected_polygon() #pass None up to let other classes know

        #If polygons are not visible
        else:
            for button in self.polygon_buttons:
                if button['description'] == "hide":
                    button['hover_tooltip'].change_hover_text(button['name']) #change text in tooltip to display that polygons are to be hidden if clicked
                    if button['show_image']:
                        for image in self.parent.imgs_custom_btns: #the images have been already converted in the parent so a case of calling that
                            if image['name'] == "Hide Polygons":
                                button['widget']['image'] = image['image']
                    else:
                        button['widget']['text'] = button['text'] #change the text for show polygons btn if the image is not used
                else:
                    button['widget']['state'] = button['dlft_state'] #set all other buttons to default states

            self.load_polygons() #load the polygons to figure with button states accordingly
            self.get_selected_polygon() #pass None up
            self.polygons_visible = True #polygons are now visible


    #EDIT POLYGON METHODS
    #For when the edit button is clicked
    def edit_btn_click(self, polygon):
        if self.selected_polygon != None: #if polygon is selected then when click on graph, select_vertex func is called
            self.fc.disconnect() #disconnect the mouse click as select vertex is now in operation if figure is clicked
            self.fc.connect(lambda event: self.select_vertex(event, polygon))
        else:
            print("No polygon selected")

    #Function for the user to select a vertex when they click on the graph
    def select_vertex(self, event, polygon):
        #select vertex to be edited - every click is checked for it's x and y coordinates
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

    #Function for the user to place down a plot when they next click the graph after select_vertex
    def position_vertex(self, event, polygon, vertex_selected, highlighted_point):
        self.remove_highlighted_points() #remove the highlighted_points
        selected_another_polygon_vertex = False
        self.selected_polygon = polygon
        self.check_polygon_selected() #check the polygon that is selected

        #user is to place the vertex in another position but various checks are carried out that ensure this plot is possible

        #In case the user clicks a vertex that is part of another polygon, check
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

        #If the plot is not part of another polygon but is another vertex of the same polygon, check
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

                #check that new position is not creating an intersection - with editing it could be the case of two prospective lines
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

                #If intersects
                result = "no"
                if intersector:
                    self.update_information("Intersection Found with another Polygon. Plot cannot be made", "warning")
                    result = messagebox.askquestion("Intersection Found", "An intersection with another polygon has been found and the plot has not been made.\n\nWould you like to override this?", icon='warning', default='no')
                    print("RESULT", result)
                    #If there is no intersection - it is false
                if not intersector or result == "yes": #PLOT CAN FINALLY BE MOVED!
                    #Remove the current polygon from the graph
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

                    #the polygon remains selected
                    self.show_selected_plots(polygon['scatter_points'], self.axis.collections, self.select_col)
                    self.show_selected_plots(polygon['lines'], self.axis.lines, self.select_col)

                    self.update_information("Edited Plot placed!", "positive") #update the message

                    self.draw_figure()
                    #Hunter, J. (2005) Re: [Matplotlib-users] Deleting lines from a plot [Online]. Available at: https://sourceforge.net/p/matplotlib/mailman/message/9334388/ [Accessed: 17 July 2020]
                    #Matplotlib. Matplotlib.pyplot [Online]. Available at: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.html [Accessed: 17 July 2020]
                else:
                    #this would keep the yellow highlighted point on the existing point when the user tries to click across an intersection
                    highlighted_point = self.create_highlighted_pt(self.axis, self.highlighted_points, polygon['co-ordinates'][index])

                    #Otherwise polygon still remains selected
                    self.show_selected_plots(polygon['scatter_points'], self.axis.collections, self.select_col)
                    self.show_selected_plots(polygon['lines'], self.axis.lines, self.select_col)

                    self.update_information("Intersection found. Plot not possible.", "warning") #update message

                    self.draw_figure()

    #Method creates a highlighted point that is behind the vertex that is passed through
    def create_highlighted_pt(self, axis, pts_list, coord):
        #create a highlighted point to show vertex that is selected
        color = [item['current_value'] for item in self.settings if item['setting'] == "Selected Vertex Colour"][0] #gets updated setting
        size =  int([item['current_value'] for item in self.settings if item['setting'] == "Selected Vertex Size"][0]) #gets updated setting

        highlighted_point = axis.scatter(coord[0], coord[1], s=size, color=color) #forms a highlighted ring
        pts_list.append(highlighted_point) #append to highlighted points list
        self.draw_figure()
        return highlighted_point


    #OTHER METHODS
    #Function to create an x and y list of co_ordinates to be plotted. Often used when plotting polygons as .plot takes an xlist & ylist
    def create_x_y_list(self, coords):
        xlist = []
        ylist = []
        for item in coords:
            xlist.append(item[0])
            ylist.append(item[1])
        return xlist, ylist

    #Function to clear all axis data & draw this to the figure. Used for instance when polygons are hidden
    def clear_axis_data(self):
        self.axis.lines.clear()
        self.axis.collections.clear()
        self.draw_figure()

    #This is a quick fix to update the hover to include translated polygons too.
    #It is called by the parent class as there is not a refresh when translated polygons are added to a figure on screen. Therefore there is no load polygons method call.
    def update_hover_polygons(self):
        polygons = []
        #it essentially adds all the polygons from polygon info & all polygons from translated polygons into one list
        for polygon in self.polygon_info: #polygon info for this slice
            polygons.append(polygon)
        for translated_polygon in self.translated_polygon_info: #translated polygon info for this slice
            formatted_coords = []
            if len(translated_polygon['co-ordinates'][0]) == 4: #Needs to be made more dynanmic
                for x, y, z, w in translated_polygon['co-ordinates']:
                    formatted_coords.append([x, y])
            else:
                for x, y in translated_polygon['co-ordinates']:
                    formatted_coords.append([x, y])

            translated_polygon['co-ordinates'] = formatted_coords
            polygons.append(translated_polygon)

        hover_instance = PolygonHover(self, polygons, self.precision, self.figure, self.axis, self.select_col) #calling the hover class
        self.parent.update_hover(hover_instance)

    #function that pulls in the settings that are saved for polygon tags colours
    def get_colour(self, tag):
        colour = False
        for preset in self.tags:
            #if the label is in the tags list then return the colour, if not return the unknown tag colour
            if preset['label'].capitalize() == tag: #tag needs capitalising
                colour = True
                return preset['colour'] #colour goes with the custom made tag in the settings
        #Return polygons in colours where there are no tags present as in Pink colour - have this setable in the settings
        if not colour:
            return [item['current_value'] for item in self.settings if item['setting'] == "Unknown Tag Colour"][0]

    #FUTURE DEVELOPMENT - Below two methods are dispensible if code corrected elsehwere
    #function that calls the number of current polygons that are saved in the json
    def get_total_polygons(self):
        file_info = self.file_writer.read_file()
        file_sorted = len(self.file_writer.sort_file(file_info, "slice", self.slice_name)) #length would be the number
        return file_sorted

    #if polygons are present then the select button would be enabled
    def check_if_polygons_present(self):
        polygons = self.get_total_polygons()
        for button in self.polygon_buttons:
            if button['description'] == "select" or button['description'] == "hide":
                if polygons == 0: #if there are no polygons on screen after deletion for instance
                    button['widget']['state'] = "disabled"
                else:
                    button['widget']['state'] = "normal"

    #reset the polygon colours back to their originals when for instance one is selected after another has already been selected
    def reset_polygon_cols(self, draw):
        #iterate over each polygon in polygon info & then each matplotlib object that is on the axis
        for polygon in self.polygon_info:
            for plot in self.axis.lines:
                if plot in polygon['lines']:
                    plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
            if len(polygon['scatter_points']) > 0:
                for plot in self.axis.collections:
                    if plot in polygon['scatter_points']:
                        plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func

        #This reset also needs to happen to translated polygon info if there are polygons there too.
        if len(self.translated_polygon_info) > 0:
            for polygon in self.translated_polygon_info:
                for plot in self.axis.lines:
                    if plot in polygon['lines']:
                        plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
                if len(polygon['scatter_points']) > 0:
                    for plot in self.axis.collections:
                        if plot in polygon['scatter_points']:
                            plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func

        if draw:
            self.draw_figure()

    #Function to remove any highlighted points from the figure, eg if one was replaced after editing a point & now needs to be removed eg if a differnt button like draw was clicked
    def remove_highlighted_points(self):
        for item in self.highlighted_points:
            if item in self.axis.collections:
                self.axis.collections.remove(item)
        self.highlighted_points.clear()
        self.draw_figure()

    #Method that colours a particular axis obj if it is polygon objs, a given colour (used to select the polygons)
    def show_selected_plots(self, polygon_objs, axis_objs, select_col):
        #Matplotlib. matplotlib.collections [Online]. Available at: https://matplotlib.org/3.2.1/api/collections_api.html [Accessed: 20 July 2020]#setting the colour
        for plot in axis_objs:
            if plot in polygon_objs:
                plot.set_color(select_col) #select to selected_colour


    #REMOVING METHODS
    #Method for when the delete button is clicked
    def del_btn_click(self, polygon):
        self.remove_highlighted_points() #make sure highlighted points are removed

        #ask confirmation - pass in id
        result = messagebox.askquestion("Delete Polygon", "Are you sure you want to delete Polygon {}?".format(str(polygon['id']), icon='information'))
        #JPvdMerve. (2012) Tkinter askquestion dialog box [Online]. Available at: https://stackoverflow.com/questions/11244753/tkinter-askquestion-dialog-box [Accessed: 16 July 2020]
        if result == "yes": #if result was yes from the dialog box of confirmation
            try:
                #remove plots from axis
                self.remove_plot(polygon['lines'], self.axis.lines)
                self.remove_plot(polygon['scatter_points'], self.axis.collections)
                self.draw_figure() #draw the figure without the deleted plots

                id = polygon['id'] #id of the polygon

                #remove from the json file
                current_data = self.file_writer.read_file() #read up to data file
                self.file_writer.remove_record(current_data, id) #remove the record for polygon from the up to date file

                #remove from dict
                self.polygon_info = [item for item in self.polygon_info if item['id'] != id] #remove from self.polygon info #https://stackoverflow.com/questions/33190779/how-to-delete-a-dictionary-from-a-list-of-dictionaries

                #text to tell user was successfully deleted
                self.update_information("Polygon with Id: {} successfully deleted.".format(str(id)), "positive") #information line to let user know that the polygon has been removed

                self.load_polygons() #re-load polygons & subsquent butn state functions
                self.get_selected_polygon()

            except:
                print("There was an issue deleting the polygon.")
                self.update_information("There was an issue deleting the polygon. Please try again.", "warning")

            self.load_polygons() #re-load polygons & subsquent btn state functions
            self.get_selected_polygon() #pass up selected polygon

    #Removing a plot if it == an obj passed through. remember I add all the objs created to lists so I can distinguish between what is on the axis and which polygon it is related too
    def remove_plot(self, polygon_objs, axis_objs):
        #function to remove a polygon
        for plot in polygon_objs:
            for object in axis_objs:
                if plot == object:
                    axis_objs.remove(plot)

    #removing a polygon, removing both lines & collections from axis that are assigned to that polygon
    def remove_polygon_obj(self, polygon, axis_objs):
        self.remove_plot(polygon['lines'], axis.lines)
        self.remove_plot(polygon['scatter_points'], axis.collections)


    #EDIT TAG METHODS
    #Function to save the change of tag
    def edit_tag(self, polygon):
        #Result is sent back from PolygonTagChanger depending on user input
        result = PolygonTagChanger(polygon, self.tags).send()
        # print("RESULT", result)
        #if result is different to current tag then confirm btn would have had to be clicked
        if result != polygon['tag']:

            #Update the Polygon Info
            for item in self.polygon_info:
                if item['id'] == polygon['id']:
                    item['tag'] = result

            #Update json file unless it cannot be found
            try:
                data = self.file_writer.read_file()
                self.file_writer.update_file(data, polygon['id'], 'tag', result)

            except FileNotFoundError:
                message = "JSON file could not be found."
                error = messagebox.showerror(title="File Not Found", message="JSON file could not be found.")
                print("JSON file could not be found.")


    #MASK METHODS - to create a mask of the polygon
    def create_mask(self, polygon):
        coordinates = self.check_polygon_complete(polygon["co-ordinates"]) #check if the polygon is complete, if not the function adds the first coordinate

        image_file = ImageFinder(self.parent.folder_selected, self.slice_name)
        file = image_file.check_exists() #as using .png file & not numpy array I check if the image exists.

        try:
            if file != None:
                masked_image = PolygonMasker(coordinates, file) #call the masking class
                image = masked_image.apply_mask(MASK_COLOUR_OR_BLACK_WHITE) #apply the mask
                filename = filedialog.asksaveasfile(mode='w', #write
                                                    initialfile="Polygon ID " + str(polygon["id"]) + " Mask " + self.slice_name, #default placeholder save text
                                                    title="Save Mask of Slice: " + self.slice_name +", Polgon: " + str(polygon["id"]), #title of dialog
                                                    defaultextension=".png", #default extension
                                                    filetypes = ((".png File","*.png"), (".jpeg File","*.jpg"),("All Files","*.*"))) #files available
                if filename == None: #returns None if save dialog cancelled
                    return
                else:
                    masked_image.write_image(image, filename.name) #if there is a confirmation of save then write the image
            else:
                print("File could not be found") #as None is returned from the os.exists in ImageFinder
                messagebox.showwarning(title="Error with Masking Image", message="There was an error with producing a mask for slice: " + self.slice_name + ".\n\nA .png file could not be found. ", icon="warning")
        except:
            print("Error with masking image") #Another error as Try Except fails
            messagebox.showwarning(title="Error with Masking Image", message="There was an error with producing a mask for slice: " + self.slice_name + ".", icon="warning")

    #Basic method to check if a polygon that has been passed through is completed **it is not checking to complete the polygon drawing wise
    #Used by masking method only currently
    def check_polygon_complete(self, input_coordinates):
        if input_coordinates[len(input_coordinates) - 1] != input_coordinates[0]:
            output_coordinates = input_coordinates
            output_coordinates.append(input_coordinates[0]) #Need to add the first coordinate on again if does not complete
        else:
            output_coordinates = input_coordinates
        return output_coordinates

#Class for the Note Area upon the Slice Figure. Includes the ADD NOTE tab, SHOW NOTES tabs etc
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
        #BELOW IS NOTE TYPE INFORMATION, inc radio name name, columns for table, table_width
        #Further methods below like creating tabs, radio btns, iterate over this dict
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

        #FUTURE DEVELOPMENT - Dynanmic further with a Notebook class
        #create notebook
        self.note_tab_pane = ttk.Notebook(self.parent_frame)
        self.note_tab_pane.pack(side="bottom", fill="x")

        #create tabs: show notes etc
        i = 0
        for item in self.note_types:
            new_tab = Tab(self.note_tab_pane, colour_scheme['header_bg']) #create tab pane
            inner_tab_frame = new_tab.add_tab(item['name'] + " Notes")
            self.show_note(inner_tab_frame, item['radio_name'])
            self.note_tabs.append({"tab":item['radio_name'], "frame":inner_tab_frame, "tab_index": i}) #store the note tabs for further manipuation of tab obj
            item['tab_frame'] = inner_tab_frame
            i += 1


        #CREATE ADD NOTE TAB
        self.new_tab_add = Tab(self.note_tab_pane, colour_scheme['header_bg']) #create a new tab instance
        self.notes_frame = self.new_tab_add.add_tab("Add Note")
        self.note_tab_pane.select(self.notes_frame) #override the function of selecting the last added tab to select a specfic one i.e the add note tab

        #ADD NOTE TAB CONTENTS
        #CREATE RADIO BTNS
        self.radio_frame = tk.Frame(self.notes_frame, background=colour_scheme['header_bg'])
        self.radio_frame.pack(side="top", fill="x")
        self.note_type = tk.StringVar()
        self.radiobuttons = []
        padding_x = (10, 0) #padding just for the first item

        for item in self.note_types:
            radio = ttk.Radiobutton(self.radio_frame, text=item['radio_name'], value=item['radio_name'], variable=self.note_type, command=self.activiateTextBox)
            radio.pack(side = "left", pady=10, padx=padding_x)
            self.radiobuttons.append({"name": item['radio_name'], "widget": radio}) #store radiobuttons for further manipuation
            padding_x = (50, 0) #change the padding going forwards after first radio button

        self.no_polygon_selected_reset() #disable the selected polygon button if no polygon selected. No polygon is selected to start

        #create Notebox textbox for adding a new note
        self.notebox_frame = tk.Frame(self.notes_frame, bg=colour_scheme['header_bg'])
        self.notebox_frame.pack(fill="x", expand=True)
        self.initial_text = "Select Option Above" #referring to the radio buttons
        self.notebox = TextBox(self.notes_frame, 3, 10, self.initial_text)
        self.notebox.change_notebox_padding(10, 0) #I remove the y padding here but keep it dynamic
        self.notebox_activated_text = "Add a note..." #text for when the notebox is activiated
        self.notebox.disable_notebox() #disable the notebox straight away
        self.contents = self.notebox.read_contents()[:-1]

        #FUTURE DEVELOPMENT - make this bind dynanmic
        self.notebox.notebox.bind("<Button-1>", lambda e: self.watch_for_txtbx_click(self.notebox.read_contents()[:-1]))

        #ADD NOTE BTNS
        self.notebox_btns_frm = tk.Frame(self.notes_frame, background=colour_scheme['header_bg'])
        self.notebox_btns_frm.pack(side="bottom", fill="x", expand=True)
        self.notebox_btn_dict = [{"name": "clear", "command":lambda: self.notebox.clear_notebox(), "default_state": "normal", "side": "left", "width":10},
                                {"name": "add", "command":lambda: self.add_note(), "default_state": "disabled", "side": "right", "width":10}]
        self.notebox_btns = ButtonCreator(self.notebox_btns_frm, self.notebox_btn_dict) #use button creator


    #GENERAL METHODS REGARDING RADIO BUTTONS & TABS
    #A function that changes the text and the status of a radio btn (Polygon btn changes to include id when polygon is selected)
    def change_radio_btn_text_and_status(self, radio_btn_name, state, widget_text):
        for radiobtn in self.radiobuttons:
            if radiobtn['name'] == radio_btn_name:
                radiobtn['widget']['state'] = state
                radiobtn['widget']['text'] = widget_text

    #A function that can alter the name of a Tab header (Polygon Notes is changed to the polygon details & would need to be changed back)
    def set_tab_name(self, tab_name, new_title):
        for item in self.note_tabs: #reset the tab to Polygon Notes
            if item['tab'] == tab_name:
                self.note_tab_pane.tab(item['tab_index'], text=new_title)

    #A function that can customise the note widget text as it normally just says No Notes Made or may provide a table. Customises with label only
    #for instance for polygon notes, it would say No Polygon Selected
    def customise_note_widget_text(self, tab_name, new_label_text):
        for notetype in self.note_types:
            if notetype['radio_name'] == tab_name:
                if 'table_or_error_widget' in notetype:
                    notetype['table_or_error_widget'].destroy()
                    new_label = tk.Label(notetype['table_frame_widget'], text=new_label_text, bg=colour_scheme['header_bg'], fg=colour_scheme['font_col'])
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
            self.no_polygon_selected_reset()


    #ADJUSTING OF NOTES METHODS
    #Method for adding a note to a slice, scan type or polygon
    def add_note(self):
        #Get Values - WOuld like below to work
        formatted_date_time = TimeDate().return_formatted_date_time() #get time date
        possible_note_details = {"note": self.notebox.read_contents()[:-1], "user": self.username, "year": self.figure_information['year'], #possible details for a note to be saved with
                        "patient": self.figure_information['patient'], "scan_type": self.figure_information['scan type'],
                        "slice name": self.slice_name[:-1], "date": formatted_date_time[0], "time": formatted_date_time[1]}

        #iterate over notetypes, which has been selected?
        for notetype in self.note_types:
            if self.note_type.get() == notetype['radio_name']:
                note_details = {}
                for detail_required in notetype['details_required']: #details required for this note are set in the note_types dir
                    note_details[detail_required] = possible_note_details[detail_required]

                #get the file & read it
                file_name = self.folder_selected + "/" + notetype['file_location'] + '.json'
                json_file = jsonFileReaderWriter(file_name, notetype['file_sub_extension']['validator_key']) #look for json file
                json_file.check_and_create() #check if the file is created & if not create it - as note will be added anyway
                data = json_file.read_file() #read file

                #USE my mental algorithm that really isn't needed and is too complex. Requires it to be in a list though as it is recursive.
                listed_data = []
                listed_data.append(data)
                #add data to file - look for sub extensions i.e where to place the data in the file
                jsonNoteAdder(notetype['file_sub_extension'], note_details, listed_data)

                json_file.create_json_file(listed_data[0]) #create new data file

        # #only refresh notes for table that note has been added for
        self.refresh_tab(self.note_type.get())
        # #Reset the tab now a note has been added
        self.reset_add_note_tab()

    #Method for showing the table for each note type in respective tab. If no notes will tell user
    def show_note(self, frame, given_note_type):
        #iterate over note_types to show correct note, given_note_type can be Slice or a Polygon
        for notetype in self.note_types:
            if given_note_type == notetype['radio_name']:
                file_name = self.folder_selected + "/" + notetype['file_location'] + '.json' #Gets the filename
                data_present = False
                if os.path.exists(file_name):
                    json_file = jsonFileReaderWriter(file_name, notetype['file_sub_extension']['validator_key']) #look for json file
                    notes = json_file.read_file() #read file
                    if notes != None:
                        listed_data = []
                        listed_data.append(notes)

                        note_finder = jsonNoteShow(notetype['file_sub_extension'], listed_data) #this class uses the data above to return the notes from the certain depth of json as inputted
                        unformatted_data = note_finder.returned_data

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

                #only create if the frame has not been created before
                if 'table_frame_widget' not in notetype:
                    tb_frame = tk.Frame(frame, bg=colour_scheme['header_bg'])
                    tb_frame.pack(side="top", fill="both", expand=True)
                    notetype['table_frame_widget'] = tb_frame #assign this to the dict

                #if there is data to show
                if data_present:
                    if 'table_or_error_widget' in notetype: #if it is in then it will be within the dict. need to destroy it & replace it with a new table
                        notetype['table_or_error_widget'].destroy()
                    row_btns = [{"name": "remove", "text": "Remove", "function": lambda  args, notetype = given_note_type: self.remove_note(args, notetype), "width": 7}, #btns for the remove & edit functions
                                {"name": "edit", "text": "Edit", "function": lambda args, notetype = given_note_type: self.edit_note(args, notetype), "width": 7}
                                ]

                    table = NoteTable(notetype['table_frame_widget'], notetype['table_col_settings'], formatted_data, notetype['table_width'], 150, row_btns, colour_scheme['header_bg']) #create table using NoteTable functionality
                    notetype['table_or_error_widget'] = table #assign so can be destroyed elsewhere in the class

                #if there is no data to show
                else:
                    if 'table_or_error_widget' in notetype: #if this is there then it needs to be destroyed
                        notetype['table_or_error_widget'].destroy()
                    error_label = tk.Label(notetype['table_frame_widget'], text="No notes have been made.", bg=colour_scheme['header_bg'], fg=colour_scheme['font_col']) #if there are no notes or there was any kind of error then runs this
                    error_label.pack(side="top", fill="both", expand=True, padx=10, pady=10)
                    notetype['table_or_error_widget'] = error_label #assign so can be destroyed elsewhere in the class

    #Method called for when a note is to be edited for either note type
    def edit_note(self, args, given_note_type):
        #loads edit window & recieves result for the new note
        try:
            #args is the current details of the row. the button passes through those details.
            current_note = args[0]['note']
            current_note_id = args[0]['id']
            edit_note = EditNote(current_note, given_note_type, self.folder_selected, self.slice_name).send() #call the edit window. Works in the same way as the settings

            # if confirm button is clicked then note is returned, if cancel clicked None returned
            if edit_note != None:
                for notetype in self.note_types:
                    if given_note_type == notetype['radio_name']:
                        file_name = self.folder_selected + "/" + notetype['file_location'] + '.json' #Gets the filename

                        json_file = jsonFileReaderWriter(file_name, notetype['file_sub_extension']['validator_key']) #look for json file with file extension to just get notes that are within the appropiate key
                        notes = json_file.read_file() #read file to get current notes

                        #to edit the file, I need to use my way too complex algorithm, needs to be in a list as is recursive
                        listed_data = []
                        listed_data.append(notes)

                        jsonNoteEdit(notetype['file_sub_extension'], listed_data, edit_note, current_note_id) #call the edit function & pass through the id as that is the verification that is needed to then edit
                        json_file.create_json_file(listed_data[0]) #create new data file

                        self.refresh_tab(given_note_type) #only refresh if note has actually changed

        except:
            print("Error Editing Note")
            messagebox.showerror("Error Editing Note" , "There was an error editing the note.\n\n Please check a notes file exists.", icon="warning")

    #Method called for when a note is to be removed. Very similar to editing a note above
    def remove_note(self, args, given_note_type):
        try:
            #args pass through the note
            current_note = args[0]['note']
            current_note_id = args[0]['id']

            #ask for confirmation for the deletion
            result = messagebox.askquestion("Delete Note", "Are you sure you want to delete note: {}?".format(str(current_note_id)), icon='question') #if result is True then continue

            if result:
                for notetype in self.note_types:
                    if given_note_type == notetype['radio_name']:
                        file_name = self.folder_selected + "/" + notetype['file_location'] + '.json' #Gets the filename
                        json_file = jsonFileReaderWriter(file_name, notetype['file_sub_extension']['validator_key']) #look for json file
                        notes = json_file.read_file() #read file

                        #to pass it through the delete algorithm, needs to be in a list as recursive
                        listed_data = []
                        listed_data.append(notes)

                        jsonNoteDelete(notetype['file_sub_extension'], listed_data, current_note_id)
                        json_file.create_json_file(listed_data[0]) #create new data file

                        self.refresh_tab(given_note_type) #only refresh if note has actually changed

        except: #if there is a failure for instance no file then don't remove
            print("Error Removing Note")
            messagebox.showerror("Error Removing Note" , "There was an error removing the note.\n\n Please check a notes file exists.", icon="warning")


    #TAB ORIENTED METHODS
    #Method for refreshing the table in a tab
    def refresh_tab(self, tab):
        for item in self.note_tabs: #tabs are located in here
            if item['tab'] == tab:
                self.show_note(item['frame'], item['tab']) #call show note again with specific tab, will destroy & create

    #Function that just automates the self.refresh_tab function above
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
    #When a radio button is clicked, the textbox in ADD NOTE TAB is activated.
    def activiateTextBox(self):
        self.notebox.enable_notebox() #enable it using notebox class
        self.notebox.replace_text(self.notebox_activated_text) #replace the text with new text
        self.notebox_btns.change_to_default_states() #change the add note buttons to default states eg. enable as previously disabled

    #Watches out for a click in the textbox. Placeholder text is removed if found
    def watch_for_txtbx_click(self, notebox_test):
        if (notebox_test == self.notebox_activated_text): #if the present text in the textbox is equal to the insert then remove all text
            self.notebox.clear_notebox() #clear the notebox, can also use .delete("insert linestart", "insert lineend")
            self.notebox_btns.enable_all_btns() #enable Clear & Add btns



#run the MainAPP
#*geometry which is sometimes set here with tkinter applications is set per page frame in MainApp
app = MainApp()
app.mainloop()
