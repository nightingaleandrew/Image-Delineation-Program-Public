import tkinter as tk
from tkinter import ttk
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

from storage_classes import jsonFileWriter, Database
from TopLevelWin import TopLevelWin
# from information_box_test import InformationBox
from widget_creator_classes import ColourSquare, InformationBox

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
