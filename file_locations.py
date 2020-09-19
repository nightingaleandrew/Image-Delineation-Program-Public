#File locations for files that are used by the system. The file directory needs to be change before program usage.

#I have contained them here for easy manipualtion. For instance it is easy to change the stacks_directory without opening the main files.


                #Refers to the file where the tags for the polygons are saved. The tags in this file are loaded into the program
file_locations = {"tags": r"./tags.json",
                #Refers to the file where the settings for the polygons are located. The settings arr loaded into the program
                "settings": r"./settings.json",
                #Refers to where the load stacks button open file dialog points to. The stacks can then be loaded in from there.
                "stacks_directory": r"C:/Users/Andrew/Documents/dissertation/data/proc"}
