#This script contains two classes that load data from json files.
#The two json files are created so they can be edited by the user outside the program but if edited wrongly then they will be set to defaults within the program.
#I have done this so the user can permently reset settings rather than do it just for one session

#It is also for if the files are removed or cannot be found. The program will still run.

import os, json, re
from storage_classes import jsonFileReaderWriter #so a json file can be read
from other import HexValidator

#As said above, the settigns file can be ammended & mistakes can be made. The program will revert to hard coded defaults
#Eg. if the user removes one of the settings or inputs the wrong value (eg. not a boolean for configiable or not an int for default_value with type number)
#In the JSON only the config & default_value variables are able to be adjusted
#This is dynanimc to the extent that the hardcoded settings below are adjusted - another setting can be added here easily though!

#If there are errors then the user is let know through the terminal

class SetSettings:
    def __init__(self, settings_data_filename):
        self.settings_data_filename = settings_data_filename #settings file name is passed through in Main - it is stored in the filenames file
        self.settings = self.prepare_settings()

    def prepare_settings(self):
        #Hardcoded default settings I have provided
        SETTINGS = [{"setting": "Precision", "category": "polygons", "configuable": True, "default_value": 2, "type": "number", "task": "Change Precision"},
                        {"setting": "Line Thickness", "category": "polygons", "configuable": True, "default_value": 4, "type": "number", "task": "Change Line Thickness"},
                        {"setting": "Unknown Tag Colour", "category": "polygons", "configuable": True, "default_value": "#FFC0CB", "type": "color", "task": "Choose Unknown Tag Colour"},
                        {"setting": "Selected Polygon Colour", "category": "polygons", "configuable": True, "default_value": "#0000FF", "type": "color", "task": "Choose Selected Polygon Colour"},
                        {"setting": "Selected Vertex Colour", "category": "polygons", "configuable": True, "default_value": "#FFFF00", "type": "color", "task": "Choose Selected Vertex Colour"},
                        {"setting": "Selected Vertex Size", "category": "polygons", "configuable": True, "default_value": 125, "type": "number", "task": "Choose Selected Vertex Size"},
                        {"setting": "Figure Background", "category": "polygons", "configuable": True, "default_value": "#C8C8C8", "type": "color", "task": "Choose Figure Background Colour"},
                        {"setting": "Default Tag", "category": "tags", "configuable": True, "default_value": 0, "type": "dropdown", "task": "Choose Default Tag"}
                        ]
        try:
            #Find file
            settings_writer = jsonFileReaderWriter(self.settings_data_filename, "settings") #read the file
            settings_data = settings_writer.read_key_data() #just reads the data under key settings

            #if there is data in the file
            if len(settings_data) > 0:
                #Compare each value in the settings & ensure that correct data is provided for config & default_value
                i = 0
                for setting in settings_data:
                    try:
                        value = [item['default_value'] for item in settings_data if item['setting'] == SETTINGS[i]['setting']][0]
                        if (SETTINGS[i]["type"] == "number"):
                            #Ensure that the value is an integer for default value
                            try:
                                value = int(value)
                                SETTINGS[i]['default_value'] = value #assign the value if is integer
                            except ValueError:
                                #Keep default value if not integer
                                print("ERROR WITH settings.json: " + SETTINGS[i]['setting'] + " default value is not a number.") #I print this to let the user know there is an error upon load
                        if (SETTINGS[i]["type"] == "color"):
                            #Ensure that value is HEX value
                            if HexValidator().validate_value(value):
                                SETTINGS[i]['default_value'] = value #assign the value if is validated hex string
                            else:
                                #Keep default value if not colour
                                print("ERROR WITH settings.json: " + SETTINGS[i]['setting'] + " default_colour value is not a HEX.")

                        #Get config value for the setting
                        config = [item['configuable'] for item in settings_data if item['setting'] == SETTINGS[i]['setting']][0]
                        if (config == True or config == False): #If the config value is True or False
                            SETTINGS[i]['configuable'] = config #re-assign value
                        else:
                            print("ERROR WITH settings.json: " + SETTINGS[i]['setting'] + " config value is not a Boolean.")
                    except IndexError:
                        #Where the setting is not available. Default value from this list is kept.
                        print("ERROR WITH settings.json: " + SETTINGS[i]['setting'] + " is not present in JSON File.")
                    except KeyError:
                        #Where setting is not called setting or default_value or configuable. Default value is kept.
                        print("ERROR WITH settings.json: " + SETTINGS[i]['setting'] + " is not formatted correctly in JSON File.")
                    i += 1
            else:
                print("ERROR WITH settings.json: " + "No settings found in file. Default settings used.")
                # settings_writer.create_json_file({"settings": SETTINGS}) #append the default settings to the file if nothing there
                settings_writer.write_file(SETTINGS)

        except FileNotFoundError:
            #use default settings above if file not found
            print("ERROR WITH settings.json: " + "Cannot find JSON File")

            #I add these to the settings for temp use when program is live.
            #Current value is changed for when the value is different to default but default is remembered
            #Temp value is the temp value that is chosen by the user when polygon settings is open
        for setting in SETTINGS:
            setting['current_value'] = setting['default_value']
            setting['temp_value'] = None

        #Return the settings for the program
        return SETTINGS

#Class that checks for the Tags file, if not one then creates it, prevents errors.
# Works slightly differnetly as the tags file can be adjusted when inside the program
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
            self.tag_file_writer = jsonFileReaderWriter(self.filename, "tags") #read the tags file
            self.tags = self.tag_file_writer.read_key_data() #read the data under key 'tags'

            if len(self.tags) == 0:
                #if no tags then re-input with default tags
                self.tag_file_writer.write_file(self.defaults)
                #file is just default tags currently
                self.tags = self.defaults
                print("ERROR WITH TAGS FILE, Tags not present. Default tags added.") #Let the user know
            else:
                self.tags = self.check_tags(self.tags)
                print("Tags Present & checked.") #Let the user know

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
                if type(tag['label']) == str and type(tag['colour']) == str and HexValidator().validate_value(tag['colour']):
                    checked_tags.append(tag)
                else:
                    print("Incorrect Value used for tag: " + str(tag) + " within " + self.filename + ". Tag not loaded.") #let the user know
            except KeyError:
                print("Incorrect Key used for tag: " + str(tag) + " within " + self.filename + ". Tag not loaded.")
        return checked_tags
