##This is the README for MSc Computing 1920-CMT400 Dissertation for 1970929 ##
#Delineating regions of interest in MRI/S prostate scans for cancer diagnosis #

**STRUCTURE OF & VIEWING THE PROJECT**
- Run the program through main.py
- This runs a tkinter interface that takes advantage of the Tkinter framework.

**Instructions**
1) Please check and confirm the filename for loading the stacks within file_locations.py file. Please point this to the 'proc' folder.
    eg. r"C:/Users/Andrew/Documents/data/proc"
2) Run main.py
3) If a password is required then please check main.py (hard coded password is: "" (no char))

**IMPORTS USED**
- Below are the imports I have used and would be best to have installed to be able to run the main.py file.
Py
- import numpy
- import csv, json
- import random, re, os
- import time, datetime
- import cv2 (opencv)

Tk
- import tkinter (from tkinter, ttk, messagebox, colorchooser, filedialog are imported)
- import PIL (from PIL, ImageTk, Image are imported)

Matplotlib
- import matplotlib
#The below relates to the backend of matplotlib used#
- matplotlib.use("TkAgg") #backend of matplotlib
- from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
- from matplotlib.figure import Figure

**FOLDER SUMMARIES IN DIR:**
#images
- Contains image files used for the buttons. If these are not found then a text replacement is used.


**.json FILE SUMMARIES IN DIR:**
#config.py 
- Contains configurable variables for the program for instance if password required required or not.

#settings.json
- Contains default settings used for the program such as precision or line thickness
- Settings can be changed here and imported in, if mistakes are made such as key text changes then the program will default to the default setting

#tags.json
- Contains default tags used for the program, if these are changed then the changed ones are imported.
- Tags can be changed within the program. If so, the JSON file is amended.


**.py FILE SUMMARIES IN DIR:**
#styles.py
- Contains the styles for the file including colourscheme and fonts. Please note tkinter ttk styles are within the MainApp class currently.

#file_locations.py
- Contains the locations for the tag file, settings files if they are moved. Also contains the main directory for finding stacks.

#button_images.py
- contains the image locations & zoom quantities for each image
- Also contains information regarding reference and licence

#main.py
- central file that is run for the program to run. Contains MainApp, PageOne, StartPage, Polygons class etc & also central variables.

#widget_creator_classes.py
- Contains classes that look to create widgets such as InformationBox, ButtonCreator, Login

#figure_custom_classes.py
- Contains classes that look to amend the figure and axes such as PolygonIntersector, cidPress

**storage_classes.py
- Contains classes that relate to storing data including jsonFileWriter and a Database class that I have kept for now

**check_json_files.py
- Classes that take in the format of a json file such as settings, tags & uses defaults hardcoded in if they are not in the correct format.

**SetSettings.py
- Contains a class relating to the settings and ensuring that the program runs even if the settings json file is not found or amended incorrectly.

**window_classes.py
- Contains classes that relate to layout of the application or top level windows

**other_windows.py
- Contains classes regarding other classes such as EditNote or PolygonSettings

**other.py
- Contains classes or functions that are very general such as a Hex Validator or a colour chooser for images

**PolygonTranslater
- Contains the classes that are related to the polygon translation & synchronisation functionality - Translater & MatrixFinder


** KNOWN ISSUES/BUGS ** (ids link to report Going Forwards section)
- ID 1: Hover tooltip for polygon information still shows when polygons hidden on slice
  Current Result: When the polygons have been hidden from view, the hover tooltips are still apparent on the figure if the vertex position is hovered over.
  Expected Result: Tooltips should not be visible.

- ID 2: Stack stated as synchronised when not synchronised
  Current Result: When the synchronisation has failed for a particular stack but other target stacks available are synchronised then the button of the failed stack still remains synchronised status.
  Expected Result: If the synchronisation has failed then, for that stack it should not appear synchronised. No changes should be made to the status of the button for failed stacks.

- ID 3: Adding, Removing, Editing polygon under synchronisation does not replicate changes in synchronised target stacks unless there is de-sync & re-sync. 
  Current Result: If the radiologist edits, adds or removes a polygon from the synchroniser stack then the polygon does not replicate in the target stacks. This change does not even happen under figure refresh of the target stack. It requires a cancellation of the synchronisation & a re-synchronisation.
  Expected Result:The polygon changes should immediately transfer over to all target stacks.

- ID 4: numpy.linalg.LinAlgError occurs when synchronising stacks
  Current Result: If two stacks are loaded for instance t2-axial & adc-res and synchronise is clicked on t2-axial is clicked then a “numpy.linalg.LinAlgError: Last 2 dimensions of the array must be square error”
  Expected Result: Synchronisation should occur correctly – or fail, if failure is the correct result.

- ID 5: Not possible to change point location in certain cases when editing vertex location.
  Current Result: Upon editing the vertex of a polygon, when selected the new plot position, the plot does not move. Message updates to say it was successful.
  Expected Result: Plot should move.

- ID 6: Synchronisation between Contrast-tra & t1-axial brings up no matrix available error despite matrices available for P139
  Current Result: Upon synchronising the two stacks mentioned above, an error dialog box appears saying that synchronisation was not possible due to no matrix for either stack being available
  Expected Result: Matrices are available and stacks should synchronise.


**OTHER NOTES:**
- All referencing regarding code are within the .py files where the code is first used.
- Notes of Future Development are mentioned throughout the code - these are for phase II development. They relate to Trello board & Report GoingForwards

**LEARNING**
- For understanding tkinter and it's application using Python, I conducted a couple of tutorials before I started building. These included:
#Source: Sentdex (2014) GUIs with tkinter (intermediate) [Video]. Available: https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk [Accessed: 01 July 2020].
#Source: Codemy.com (2019) Python GUI's With TKinter [Video]. Available at: https://www.youtube.com/playlist?list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV [Accessed: 30 June 2020].
