##This is the README for MSc Computing 1920-CMT400 Dissertation for 1970929 ##
#Delineating regions of interest in MRI/S prostate scans for cancer diagnosis #

**STRUCTURE OF & VIEWING THE PROJECT**
- Run the program through main.py
- This runs a tkinter interface that takes advantage of the Tkinter framework.
- The password to enter is: " " (a single space)

**IMPORTS USED**
- Below are the imports I have used and would be best to have installed to be able to run the main.py file.
Py
- import numpy
- import csv, json
- import random, re, os
- import time, datetime

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
#settings.json
- Contains default settings used for the program such as precision or line thickness
- Settings can be changed here and imported in, if mistakes are made such as key text changes then the program will default to the default setting

#tags.json
- Contains default tags used for the program, if these are changed then the changed ones are imported.
- Tags can be changed within the program. If so, the JSON file is amended.


**.py FILE SUMMARIES IN DIR:**
#widget_creator_classes.py
- Contains classes that look to create widgets such as InformationBox, ButtonCreator, Login

#button_images.py
- contains the image locations & zoom quantities for each image
- Also contains information regarding reference and licence

#figure_custom_classes.py
- Contains classes that look to amend the figure and axes such as PolygonIntersector, cidPress

**storage_classes.py
- Contains classes that relate to storing data including jsonFileWriter and a Database class that I have kept for now

**SetSettings.py
- Contains a class relating to the settings and ensuring that the program runs even if the settings json file is not found or amended incorrectly.

**TopLevelWin.py
- Contains classes that relate to layout of the application or top level windows

**other.py
- Contains classes or functions that are very general such as a Hex Validator or a colour chooser for images

**other_windows.py
- Contains classes regarding other classes such as EditNote or PolygonSettings


**OTHER NOTES:**
- All referencing regarding code are within the .py files where the code is first used.
