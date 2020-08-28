import os, json, re
from storage_classes import jsonFileWriter
from other import HexValidator
#This function allows the settings json file to be amended by the user and mistakes be made. The program will revert to defaults I have coded below.
#Eg. if the user removes one of the settings or inputs the wrong value (eg. not a boolean for configiable or not an int for default_value with type number)
#In the JSON only the config & default_value variables are able to be adjusted
#This is dynanimc to the extent that the hardcoded settings below are adjusted - another setting can be added here easily though!
# settings_data_filename = r"C:\Users\Andrew\Documents\dissertation\tkinter\settings.json"

class SetSettings:
    def __init__(self, settings_data_filename):
        self.settings_data_filename = settings_data_filename
        self.settings = self.prepare_settings()

    def prepare_settings(self):
        #Default settings I have provided
        SETTINGS = [{"setting": "Precision", "category": "polygons", "configuable": True, "default_value": 5, "type": "number", "task": "Change Precision"},
                        {"setting": "Line Thickness", "category": "polygons", "configuable": True, "default_value": 4, "type": "number", "task": "Change Line Thickness"},
                        {"setting": "Unknown Tag Colour", "category": "polygons", "configuable": True, "default_value": "#FFC0CB", "type": "color", "task": "Choose Unknown Tag Colour"},
                        {"setting": "Selected Polygon Colour", "category": "polygons", "configuable": True, "default_value": "#0000FF", "type": "color", "task": "Choose Selected Polygon Colour"},
                        {"setting": "Selected Vertex Colour", "category": "polygons", "configuable": True, "default_value": "#C2B280", "type": "color", "task": "Choose Selected Vertex Colour"},
                        {"setting": "Selected Vertex Size", "category": "polygons", "configuable": True, "default_value": 125, "type": "number", "task": "Choose Selected Vertex Size"},
                        {"setting": "Figure Background", "category": "polygons", "configuable": True, "default_value": "#C8C8C8", "type": "color", "task": "Choose Figure Background Colour"},
                        {"setting": "Default Tag", "category": "tags", "configuable": True, "default_value": 0, "type": "dropdown", "task": "Choose Default Tag"}
                        ]
        try:
            #Find file
            settings_writer = jsonFileWriter(self.settings_data_filename, SETTINGS, None) #read the json file for settings, if not found the program reverts to the default settings above
            settings_data = settings_writer.read_file() #read file for settings

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
                                print("ERROR WITH settings.json: " + SETTINGS[i]['setting'] + " default value is not a number.")
                        if (SETTINGS[i]["type"] == "color"):
                            #Ensure that value is HEX value
                            if HexValidator().validate_value(value):
                                SETTINGS[i]['default_value'] = value #assign the value if is validated hex string
                            else:
                                #Keep default value if not colour
                                print("ERROR WITH settings.json: " + SETTINGS[i]['setting'] + " default_colour value is not a HEX.")

                        #Get config value for the setting
                        config = [item['configuable'] for item in settings_data if item['setting'] == SETTINGS[i]['setting']][0]
                        if (config == 'True' or config == 'False'): #If the config value is True or False
                            if config == 'True':
                                config_value = True
                            elif config == 'False':
                                config_value = False
                            SETTINGS[i]['configuable'] = config_value #re-assign value
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
                    settings_writer.create_json_file(SETTINGS) #append the default settings to the file if nothing there

        except FileNotFoundError:
            #use default settings above if file not found
            print("ERROR WITH settings.json: " + "Cannot find JSON File")

            #I add these to the settings for temp use when program is live.
            #Current value is changed for when the value is different to default but default is remembered
            #Temp value is the temp value that is chosen by the user when polygon settings is open
        for setting in SETTINGS:
            setting['current_value'] = setting['default_value']
            setting['temp_value'] = None
            # setting['widget'] = None

        #Return the settings for the program
        return SETTINGS

#Class that checks for the Tags file, if not one then creates it, prevents errors
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
                # validated_value = HexValidator.validate_value(tag['colour'])
                if type(tag['label']) == str and type(tag['colour']) == str and HexValidator().validate_value(tag['colour']):
                    checked_tags.append(tag)
                else:
                    print("Incorrect Value used for tag: " + str(tag) + " within " + self.filename + ". Tag not loaded.")
            except KeyError:
                print("Incorrect Key used for tag: " + str(tag) + " within " + self.filename + ". Tag not loaded.")
        return checked_tags
