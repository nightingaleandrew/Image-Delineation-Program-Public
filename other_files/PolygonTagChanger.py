import tkinter as tk
from tkinter import ttk
import re

HOVER_BG = "#ffffe0"
HEADER_BG = "#00004d"
FONT_BG = "#FFFFFF"
MAIN_BG = "#0066cc"
FONT_COL = "#FFFFFF"
ERROR_FONT = "red"

#fonts
LARGE_FONT = ("Verdana", 18)
MEDIUM_FONT = ("Verdana", 14)
SMALL_FONT = ("Verdana", 10)

from toggle_frame import ToggledFrame
from TopLevelWin import TopLevelWin
from widget_creator_classes import TextBox, InformationBox, ButtonCreator, Tab, CreateToolTip, ToolTip, NoteTable, ColourSquare
from figure_custom_classes import cidPress, PolygonIntersector, CustomToolbar

from button_images import custom_btn_images
from storage_classes import jsonFileWriter, Database
from other import ConvertImages
