import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, colorchooser, filedialog
import re

HOVER_BG = "#ffffe0"
HEADER_BG = "#00004d"
FONT_BG = "#FFFFFF"
MAIN_BG = "#0066cc"
FONT_COL = "#FFFFFF"
ERROR_FONT = "red"
LARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 14)
SMALL_FONT = ("Verdana", 10)

from storage_classes import jsonFileWriter
from window_classes import TopLevelWin
from widget_creator_classes import TextBox, InformationBox, ButtonCreator, Tab, NoteTable, ColourSquare, ToggledFrame, HoverToolTip
# from PolygonTagChanger import
# from toggle_frame import ToggledFrame
from check_json_files import TagFileLoader

TAGS_DATA_FILENAME = r".\tags.json"

#Class for a tab & tab pane
class PolygonSettings:
    def __init__(self, settings):
        self.settings = settings

        self.settings_win = TopLevelWin("Polygon Settings", MAIN_BG, self)
        self.settings_win.create_header(HEADER_BG, MEDIUM_FONT, FONT_COL, "Change Polygon Settings")
        self.win_main_frame = self.settings_win.create_main(MAIN_BG)

        #Load the current set of tags from the tags file
        self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        self.tags = self.tags_writer.return_tags()

        self.tabs = []

         #create instance of toggled frame
        settings_tab = ToggledFrame(self.win_main_frame, "Polygon Settings", MAIN_BG, self)
        settings_tab.pack(fill="x", expand=1, pady=10, padx=10, anchor="n")
        self.tabs.append(settings_tab) #append to the list of tabs

        #This is for the reset defaults for the settings
        other_btns_frm = tk.Frame(settings_tab.get_sub_frame(), bg=MAIN_BG)
        other_btns_frm.pack(fill="x")
        reset_defaults_btn_dict = [{"name": "reset defaults", "command":lambda cat = "polygons": self.reset(cat), "side":"right", "default_state": "normal", "width":15}]
        reset_defaults_btn = ButtonCreator(other_btns_frm, reset_defaults_btn_dict)

        #This is for all the settings
        frame = tk.Frame(settings_tab.get_sub_frame(), bg=MAIN_BG)
        frame.pack(fill="x")

        i, j = 0, 0
        for item in self.settings:
            if item['configuable'] == True and item['category'] == "polygons":
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
                    button = tk.Button(frame, text="Change", command=lambda task=item['task'], setting=item['setting'], current_val = item['current_value'] : self.change_setting_colour(task, setting, current_val))
                    button.grid(row=i, column=j + 1, sticky="W")
                    square = ColourSquare(frame, i, j+2, item['current_value'])
                    item['colour_square_frame'] = square
                i += 1

        #Tags Toggle frame, can add a tag, change the colour & remove tag, also view all tags
        tags_tab = ToggledFrame(self.win_main_frame, "Tags", MAIN_BG, self)
        tags_tab.pack(fill="x", expand=1, pady=10, padx=10, anchor="n")
        self.tabs.append(tags_tab) #append to the list of tabs

        self.tags_frame = tk.Frame(tags_tab.get_sub_frame(), bg=MAIN_BG)
        self.tags_frame.pack(fill="x")

        self.add_tag_frame = tk.LabelFrame(self.tags_frame, text=" Add New Tag: ", background=MAIN_BG, fg=FONT_COL)
        self.add_tag_frame.grid(row=0, column=0, sticky="NSWE", padx=10, pady=10)

        self.error_msg = tk.Label(self.add_tag_frame, background=MAIN_BG, fg="red") #Error message that appears when tag already exists/no tag is added

        self.tag_entry = tk.Entry(self.add_tag_frame, highlightbackground = "red", highlightcolor = "red", highlightthickness = 0)
        self.tag_entry.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10)
        self.tag_entry.insert(tk.END, "Tag Label...")
        self.tag_entry.bind("<Button-1>", lambda e: self.watch_for_txtbx_click(self.tag_entry.get())) #bind function on the event of clicking the text box

        #Button that picks the colour
        self.colour_pick = tk.Button(self.add_tag_frame, text="Pick Colour", command=lambda: self.pick_colour_for_tag("Choose Tag Colour"), state="disabled")
        self.colour_pick.grid(row=2, column=0, padx=10, pady=10)

        self.colour_frame = ColourSquare(self.add_tag_frame, 2, 1, None)

        self.tag_form_btn_frame = tk.Frame(self.add_tag_frame, bg=MAIN_BG)
        self.tag_form_btn_frame.grid(row=3, column=0, columnspan=2)
        self.tag_form_buttons_dict = [{"name": "clear", "command": lambda function=self.clear_tag: function(), "side":"left", "default_state": "disabled", "width":10},
                                    {"name": "add", "command": lambda function=self.add_tag: function(), "side":"right", "default_state": "disabled", "width":10}]
        self.tag_form_buttons = ButtonCreator(self.tag_form_btn_frame, self.tag_form_buttons_dict)

        self.added_tag = {"label": None, "colour": None}

        self.create_tags_table(self.tags_frame)

        #create default tags label frame for setting a default tag for speed
        frame = tk.LabelFrame(self.tags_frame, text=" Set Default Tag: ", background=MAIN_BG, fg=FONT_COL)
        frame.grid(row=2, column=0, sticky="NSWE", padx=10, pady=10)

        i, j = 0, 0
        for item in self.settings:
            if item['configuable'] == True and item['category'] == "tags":
                label = tk.Label(frame, text=item['setting'] + ": ", padx=10, pady=10, bg=MAIN_BG, fg=FONT_COL)
                label.grid(row = i, column = j, sticky="W")
                if item['type'] == "dropdown":
                    if item['setting'] == "Default Tag":
                        values = self.load_tags()
                        var = tk.StringVar(frame)
                        choice = ttk.Combobox(frame, values=values) #Use ttk. combo box as looks more appealing
                        choice.current(item['current_value']) #current value in the combo box
                        choice.grid(row=0, column=1, sticky="W", padx=5)
                        var.set(values[item['current_value']])
                        item['variable'] = var
                        item['combobox'] = choice
                        item['values'] = values
                        choice.bind("<<ComboboxSelected>>", lambda e, setting = item['setting'], values=values: self.change_tag(e, setting, values))

                        text = "If altered will alter all open tabs."
                        HoverToolTip(choice, HOVER_BG, SMALL_FONT, text) #add in a hover to let user know that all open tabs will alter too

        #cancel & confirm buttons
        self.settings_win.add_controls()
        self.value = False

    #Polygon Setting Functions
    #This is used for the Polygon Settings toggle frame to determine if there are only digits entered
    def only_numeric_input(self, digit):
        # checks if entry's value is an integer or empty and returns an appropriate boolean
        if digit.isdigit() or digit == "":  # if a digit was entered or nothing was entered
            return True
        return False

    #Function that loads the tags, there is a similar function in the Slice Figure class
    def load_tags(self):
        polygon_tags = []

        tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        tags = tags_writer.return_tags()

        for tag in tags:
            polygon_tags.append(tag['label'].capitalize())

        return polygon_tags

    #Called when the tag is changed, this is bound to the dropdown, ensures correct current tag is passed through
    def change_tag(self, event, setting, values):
        for item in self.settings:
            if item['configuable'] == True and item['category'] == "tags":
                if item['type'] == 'dropdown' and item['setting'] == setting:
                    item['temp_value'] = values.index(item['combobox'].get())

    #Refresh the tags dropdown list for dropdowns according to the setting
    def refresh_tags_list(self, setting):
        for item in self.settings:
            if item['configuable'] == True and item['category'] == "tags":
                if item['type'] == 'dropdown' and item['setting'] == setting:
                    new_values = self.load_tags()
                    item['values'] = new_values
                    item['combobox']['values'] = new_values

    def reset(self, category):
        for item in self.settings: #change values to default values
            if item['category'] == category: #only do for category as polygons & tag settings split up
            #I use temp value as if then confirm has been selected, the program knows something may have changed
                item['temp_value'] = item['default_value'] #reset the settings to their default value
                if item['type'] == "number":
                    item['widget'].delete(0, tk.END) #clear entry box
                    item['widget'].insert(tk.END, item['temp_value']) #refil entry box
                elif item['type'] == "color":
                    item['colour_square_frame'].set_colour(item['temp_value'])  #reset the colour sqaure
                elif item['type'] == 'dropdown':
                    item['combobox'].current(item['temp_value'])
                    item['variable'].set(item['values'][item['temp_value']])

    def change_setting_colour(self, task, setting, current_col):
        for item in self.settings:
            if item['setting'] == setting:
                if item['temp_value'] != None:
                    current_col = item['temp_value']
        colour = colorchooser.askcolor(title = task, color=current_col)

        for item in self.settings:
            if item['setting'] == setting:
                item['temp_value'] = colour[1]
                item['colour_square_frame'].set_colour(colour[1])
        #https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front

    #Tags Functions
    def create_tags_table(self, frame):
        table_frame = tk.Frame(frame, background=MAIN_BG)
        table_frame.grid(row=1, column=0, sticky="NSEW")
        col_settings = [{"column": "label", "wraplength":75, "side": "left", "width": 11, "fill": False},
                        {"column": "colour", "wraplength":50, "side": "left", "width": 7, "fill": True}
                        ]

        row_btns = [{"name": "remove", "text": "X", "function":lambda args: self.remove_tag(args), "width": 3},
                    {"name": "edit", "text": "Edit", "function": lambda args: self.change_tag_colour(args), "width": 3}
                    ]
        table = NoteTable(table_frame, col_settings, self.tags, 205, 150, row_btns, HEADER_BG)

    def change_tag_colour(self, *args):
        print("ARGS", args)
        print("ARGS", args[0][0])
        colour = colorchooser.askcolor(title = "Change Colour: Tag {}".format(args[0][0]['label']), color=args[0][0]['colour'])
        if colour != None:
            #add tag to JSON file - Use jsonFileWriter for this as not checking contents

            for tag in self.tags:
                if (tag['label'] == args[0][0]['label']) and (tag['colour'] == args[0][0]['colour']):
                    tag['colour'] = colour[1]

            self.tag_writer = jsonFileWriter(TAGS_DATA_FILENAME, self.tags, None)
            self.tag_writer.create_json_file(self.tags) #will overwrite json file with new tag colour
            #call again to get updated
            self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
            self.tags = self.tags_writer.return_tags()
            #update table
            self.create_tags_table(self.tags_frame)
            self.value = True #A tag's colour has been changed

    def remove_tag(self, *args):
        result = messagebox.askquestion("Delete Tag", "Are you sure you want to delete Tag: {}?".format(args[0][0]['label']), icon='question')
        if result:
            #update json to remove tag
            self.tags = [item for item in self.tags if item['label'] != args[0][0]['label'] and item['colour'] != args[0][0]['colour']] ##**DOESN@T SEEM TO WORK|

            self.tag_writer = jsonFileWriter(TAGS_DATA_FILENAME, self.tags, None)
            self.tag_writer.create_json_file(self.tags) #will overwrite json file with new tag colour

            #call again to get updated
            self.tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
            self.tags = self.tags_writer.return_tags()
            #update table
            self.create_tags_table(self.tags_frame)

            #refresh the default tags list
            self.refresh_tags_list('Default Tag')
            self.value = True #A tag has been removed so outside tabs will need to be refreshed with the new tags list


    def watch_for_txtbx_click(self, text):
        if (text == "Tag Label...") or (text == "Add..."): #if the present text in the textbox is equal to the insert then remove all text
            self.tag_entry.delete(0, 'end') #https://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
        self.colour_pick['state'] = "normal"

    def clear_tag(self):
        self.tag_entry.delete(0, 'end')
        self.tag_entry.insert(tk.END, "Tag Label...")
        self.tag_entry['highlightthickness'] = 0

        self.colour_pick['state'] = "disabled" #disable the colour pick btn
        self.colour_frame.remove() #remove the colour frame, it comes back using set colour when pick colour btn is clicked
        self.error_msg.grid_forget() #forget the error msg

        #Change label & colour to None
        for key, value in self.added_tag.items():
            value = None

        self.tag_form_buttons.change_to_default_states() #change clear & add to default

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

                # self.error_msg.grid_forget()
                self.clear_tag() #clear the new tag to be added
                self.create_tags_table(self.tags_frame) #refresh the table
                self.value = True #A change has been made & therefore the wider tabs would need to be reset
        else:
            print("No Label Entered.")
            self.tag_entry['highlightthickness'] = 2 #highlight the box in red to alert user, done this instead of warning label
            self.error_msg['text'] = "Tag Name Required."
            self.error_msg.grid(row=0, column=0, padx=10, columnspan=2, sticky="W")
            self.tag_entry.insert(tk.END, "Add...")
            self.tag_entry.bind("<Button-1>", lambda e: self.watch_for_txtbx_click(self.tag_entry.get())) #bind function on the event of clicking the text box
            #highlight entry box

    #When the Pick Colour btn is clicked, following function is called to allow user to choose colour. Depending on choice unlocks next stage of btns etc
    def pick_colour_for_tag(self, task):
        colour = colorchooser.askcolor(title = task)

        #if cancel is clicked then None is returned, only unlock if a colour is returned
        #colour[1] is the hex value
        if colour[1] != None:
            self.colour_frame.set_colour(colour[1]) #set the colour which grids also the square
            self.added_tag['colour'] = colour[1] #assign the colour to the colour in the dict
            self.tag_form_buttons.enable_all_btns() #enable all the btns
        return colour[1]

    #Overall Methods
    #I only wnat one tab to be open
    def tab_toggle_open(self, title):
        #iterates over tabs to see who are open
        for tab in self.tabs:
            if( (tab.title != title) and tab.open() == 1): #if tab that is not opened but is open then closes tab
                tab.toggle_button.invoke() #clicks the button #https://stackoverflow.com/questions/26842515/how-to-execute-python-tkinter-button-without-clicking-mouse
                tab.close() #closes the tab if open but is not the tab that is opened

    #Function that sends result to parent window
    def send(self):
        self.settings_win.wait()  #waits for the window to be exited now to do anything further
        print("VALUE", self.value)
        return self.value #returns self.value which is bool, if True then item has been changed

    #Function for confirming the selection of the window to close it
    def confirm_selection(self):
        for item in self.settings:
            if (item['type'] == 'number') and (item['current_value'] != int(item['widget'].get())):
                item['temp_value'] = int(item['widget'].get()) #remember get from an entry box returns a String
        for item in self.settings:
            if item['temp_value'] != None: #item has been changed
                item['current_value'] = item['temp_value']
                self.value = True #an item has been changed so let program know to refresh tabs

        self.settings_win.close_window() #close_window

    #A cancel selection method required by base class if anything required upon cancellation
    def cancel_selection(self):
         if self.settings_win != None:
             for item in self.settings:
                 item['temp_value'] = None #reset the temp values to None, better here than doing it when class loads
         self.settings_win.close_window()

#Class that controls the polygon tag changer
class PolygonTagChanger:
    def __init__(self, polygon, tags):
        self.polygon = polygon
        self.tags = tags

        self.current_tag = self.polygon['tag'] #current tag that is passed through, combo list is set to this
        self.value = self.current_tag #this is used to pass the value of the tag back out the class to parent

        #Get the tags to fill the dropdown list                                                                                                         # }
        self.polygon_tags = []
        for tag in self.tags:
            self.polygon_tags.append(tag['label'].capitalize())

        #details for the creation of the window, using TopLevel Class
        self.window = TopLevelWin("Change Tag", MAIN_BG, self)
        self.window.create_header(HEADER_BG, MEDIUM_FONT, FONT_COL, "Change Tag for Polygon {}".format(self.polygon['id']))
        #Get & Fill the main frame
        self.win_main_frame = self.window.create_main(MAIN_BG)

        #polygon id, slice, tag, colour block for colour comparison
        self.polygon_info = InformationBox(self.win_main_frame, "left", 3, "polygon", None, MAIN_BG, FONT_COL, False)
        label_frame = self.polygon_info.get_parent_label_frame()

        #Mini frame that contains the colour block & tag (DO HAVE TO PASS THROUGH WITH INCORRECT )
        self.tag_frame = tk.Frame(label_frame, background=MAIN_BG)

        self.tag = tk.Label(self.tag_frame, text=self.polygon['tag'], background=MAIN_BG, fg=FONT_COL)
        self.tag.grid(row=0, column=0, sticky="W")
        self.colour_sq = ColourSquare(self.tag_frame, 0, 2, self.get_tag_col(self.polygon['tag']))
        # self.colour_sq.set_colour(self.get_tag_col(self.polygon['tag']))

        self.polygon_items = {"id": self.polygon['id'], "slice":self.polygon['slice'], "current tag": self.tag_frame}
        self.polygon_info.create_insides(self.polygon_items) #Manually I create the insides as it contains an inner frame
        self.polygon_info.change_to_grid(0, 0, "NSWE", 2) #InformationBox has default pack setting

        #mini frame that contains the drop down menu for changing the tag
        self.tag_change_frame = tk.Frame(self.win_main_frame, background=MAIN_BG)
        self.tag_change_frame.grid(row=1, column=0, pady=10, padx=10)

        self.dropdown_label = tk.Label(self.tag_change_frame, text="Change Tag: ", background=MAIN_BG, fg=FONT_COL).grid(row=1, column=0, sticky="W", padx=10, pady=10)
        self.polygon_tag_choice = ttk.Combobox(self.tag_change_frame, values=self.polygon_tags)
        self.polygon_tag_choice.current(self.index_current_tag()[0])
        self.polygon_tag_choice.grid(row=1, column=1, sticky="W", padx=10, pady=10)
        self.polygon_tag_choice.bind("<<ComboboxSelected>>", self.activiate_confirm_btn) #if the tag is changed then the confirm btn is activiated

        #If the tag is not present in the current list of tags then let user know
        if not self.index_current_tag()[1]:
            label = tk.Label(self.tag_change_frame, text="Tag: " + self.current_tag + " is not currently available.\n If switched it would need to be re-added.", fg="red", background=MAIN_BG)
            label.grid(row=0, column=0, sticky="W", padx=10, pady=10, columnspan=2)

        #Controls are set by the TopLevelWin class - Cancel & Confirm buttons
        self.window.add_controls()
        self.window.disable_confirm_btn() #disable the confirm btn unless the dropdown is clicked

    #find the index of the current_tag in the tags that are provided by settings
    def index_current_tag(self):
        if self.current_tag in self.polygon_tags:
            index = self.polygon_tags.index(self.current_tag)
            tag_present = True #if tag is not present
        else:
            index = 0 #if the tag is not in the new tags list then return 0, a information label will also be stated
            tag_present = False #if tag is not present
        return index, tag_present

    #function to activiate the confirmation btn
    def activiate_confirm_btn(self, event):
        self.window.enable_confirm_btn() #enable the confirm button

    #if confirm is clicked then tag is reset to current_tag that was passed through initially
    def confirm_selection(self):
        self.value = self.polygon_tag_choice.get()
        self.window.close_window()

    #A cancel selection method required by base class if anything required upon cancellation
    def cancel_selection(self):
        self.window.close_window()

    #this returns the variable for the current_tag & waits for the window to close to do this(win will close when either cancel or confirm are clicked)
    def send(self):
        self.window.wait() #waits for the window to be exited now to do anything further
        return self.value

    #I have created this for identification purposes for the colour, eg. might be easier to identify polygons on the slice
    def get_tag_col(self, current_tag):
        tag_found = False
        # for tag in self.settings['tags']:
        for tag in self.tags:
            if tag['label'].capitalize() == current_tag:
                tag_found = True
                return tag['colour'].capitalize()
        if not tag_found:
            return "beige" # pass through background col if tag not found

#Class that controls the construction & receiving of the Editing Note Window
class EditNote:
    def __init__(self, note, note_type, folder_selected, slice_name):
        self.note = note #the contents of the note
        self.note_type = note_type #whether note is slice, polygon, scan_type etc
        self.folder_selected = folder_selected
        self.slice_name = slice_name
        self.new_note = None #for when the new note comes through if so

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
        self.window.add_controls() #remember confirm & cancel btns


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
