import tkinter as tk
import tkinter.ttk as ttk
import numpy as np, os, json

import matplotlib
matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#https://stackoverflow.com/questions/32188180/from-matplotlib-backends-import-tkagg-importerror-cannot-import-name-tkagg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea
from matplotlib.figure import Figure
import random
from tkinter import messagebox

HOVER_BG = "#ffffe0"
HEADER_BG = "#00004d"
FONT_BG = "#FFFFFF"
MAIN_BG = "#0066cc"
FONT_COL = "#FFFFFF"
ERROR_FONT = "red"

class cidPress():
    #Class for clicking the CID - as the same cid is being used throughout different levels of classes
    #https://stackoverflow.com/questions/58322945/how-to-connect-and-disconnect-matplotlibs-event-handler-by-using-another-class
    def __init__(self, figure):
        self.figure = figure
        self.cidpress = None #variable is declared as disconnect may be called before

        #To connect the cid to the appropiate function, function is passed through eg. drawing or selecting polgyon
    def connect(self, function):
        self.cidpress = self.figure.canvas.mpl_connect('button_press_event', function)

        #To disconnect the cid
    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidpress)

class cidHover():
    def __init__(self, figure):
        self.figure = figure
        self.cidhover = None #variable is declared as disconnect may be called before

        #To connect the cid to the appropiate function, function is passed through eg. hovering over a polygon
    def connect(self, function):
        self.cidhover = self.figure.canvas.mpl_connect('motion_notify_event', function)

        #To disconnect the cid
    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidhover)

#class to see if the proposed line by the user intersects any existing polygons
class PolygonIntersector:
    def __init__(self, existing_polygons, polygon):
        self.existing_polygons = existing_polygons #co-ordinates of an existing polygons
        self.polygon_lines = [] #AB co-ordinates will be added for each line of all polygons already existing

        #for edit polygon, I take in the polygon being editied and have this removed from the self.existing_polygons (so doesn't intersect itself) as the proposed line is not saved yet
        if polygon != None:
            self.id = polygon['id']
            self.existing_polygons = [item for item in self.existing_polygons if item['id'] != self.id]

        #Takes in multiple polygons & iterates over the co-ordinates to create the lines
        for polygon in self.existing_polygons:
            self.polygon_lines.append(self.create_polgon_lines(polygon['co-ordinates']))

    #creates the line A & B co-ordinates for each line of the polygon, line is appended to self.polygon_lines above
    def create_polgon_lines(self, polygon_co_ordinates):
        lines = []
        i = 0
        co_ordinates = []
        for x, y in polygon_co_ordinates: #i convert them all to tuples just for neatness (this is not essential)
            co_ordinates.append((x, y))
        while i < len(co_ordinates):
            if i == len(co_ordinates) - 1: #The first co-ordinate needs to be added again as the polygon joins up
                lines.append([co_ordinates[i], co_ordinates[0]])
            else:
                lines.append([co_ordinates[i], co_ordinates[i + 1]]) #add the co-ordinate A and also the next one along
            i += 1
        return lines

    #calculates if there is an intersection between two lines
    def line_intersect(self, lineA, lineB):
        #https://rosettacode.org/wiki/Find_the_intersection_of_two_lines#Python
        #split up x and y co-ordinates for line A and line B
        Ax1, Ay1, Ax2, Ay2 = lineA[0][0], lineA[0][1], lineA[1][0], lineA[1][1]
        Bx1, By1, Bx2, By2 = lineB[0][0], lineB[0][1], lineB[1][0], lineB[1][1]

        """ returns a (x, y) tuple or None if there is no intersection """
        # difference in y axis for Line b * difference in x axis for line A subtract difference in x axis for line B * difference in y axis for line A
        d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
        if d:
            uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
            uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        else:
            return
        if not(0 <= uA <= 1 and 0 <= uB <= 1):
            return
        x = Ax1 + uA * (Ax2 - Ax1)
        y = Ay1 + uA * (Ay2 - Ay1)

        return x, y

    #function that returns a result if there is an intersection or not
    def find_intersection(self, lineA): #proposed line is passed through here
        intersection = False #assumes there is no intersection
        for polygon in self.polygon_lines:
            for line in polygon:
                intersect = self.line_intersect(lineA, line) #if this returns an intersection then return co-ordinate of intersection, if not returns None
                if intersect != None:
                    intersection = True #intersection is True if there is an intersection co-ordinate
        return intersection

# custom toolbar with changed hover text
class CustomToolbar(NavigationToolbar2Tk):
    #https://stackoverflow.com/questions/23172916/matplotlib-tkinter-customizing-toolbar-tooltips
    def __init__(self, canvas_, parent_):
        self.clicked = None
        self.toolitems = (
            ('Home', 'Reset Slice View', 'home', 'home'),
            ('Back', 'Previous Slice', 'back', 'back'),
            ('Forward', 'Next Slice', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'Configure Subplots', 'subplots', 'configure_subplots'), #subplots is not included in this figure
            ('Save', 'Save Slice', 'filesave', 'save_figure'),
            )
        NavigationToolbar2Tk.__init__(self, canvas_, parent_)

    def pan(self):
        #https://stackoverflow.com/questions/23172916/matplotlib-tkinter-customizing-toolbar-tooltips
        NavigationToolbar2Tk.pan(self)

        if self.clicked != "PAN":
            self.clicked = "PAN"
            self.mode = "PAN CLICKED" #<--
        else:
            self.clicked = None
            self.mode = "PAN UNCLICKED"
        self.set_message(self.mode)

    def zoom(self):
        NavigationToolbar2Tk.zoom(self)

        if self.clicked != "ZOOM":
            self.clicked = "ZOOM"
            self.mode = "ZOOM CLICKED" #<--- whatever you want to replace "zoom rect" goes here
        else:
            self.clicked = None
            self.mode = "ZOOM UNCLICKED"
        self.set_message(self.mode)

    def save(self):
        NavigationToolbar2Tk.ToolSaveFigure(self)
        print("hello")

    def left_figure(self, event):
        self.mode = ""
        self.set_message(self.mode)

    def mouse_move(self, event):
        NavigationToolbar2Tk.mouse_move(self, event)
        if event.inaxes and event.inaxes.get_navigate():

            data = [event.xdata, event.ydata] #I have done the quick algorithm on the left becuase it then always goes to 1.dp.
            formatted_data = []               #This looks better than a standard slice but also does not jig the figure around at all still even in ZOOM is clicked
            for item in data:
                if str(item)[3] == ".":
                    short_ver = str(item)[:5]
                else:
                    short_ver = str(item)[:4]
                formatted_data.append(short_ver)


            self.mode = "[{}, {}]".format(formatted_data[0], formatted_data[1])
            self.set_message(self.mode)
            if self.clicked == "ZOOM":
                self.set_message(self.mode + " | ZOOM")
            if self.clicked == "PAN":
                self.set_message(self.mode + " | PAN")
        else:
            self.mode = ""
            self.set_message(self.mode)


class PolygonHover:
    def __init__(self, parent, polygon_info, precision, figure, axis, selected_colour): #takes in the polygon info, & then precision, figure, axis values
        self.parent = parent
        self.polygon_info = polygon_info
        self.precision = precision
        self.fig = figure
        self.ax = axis
        self.selected_polygon_colour = selected_colour

    def hover(self, event):
        #https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib
        hovered_over = False
        if event.xdata != None:
            for polygon in self.polygon_info:
                for x, y in polygon['co-ordinates']:
                    if (np.abs(x - event.xdata) < self.precision) and (np.abs(y - event.ydata) < self.precision):
                        print("IM HERE", self.polygon_info)
                        hovered_over = True
                        #clear all existing labels
                        self.ax.artists.clear()
                        string = "Id: {} \nTag: {} \nx: {} \ny: {}".format(polygon['id'], polygon['tag'], str(x)[:6], str(y)[:6]) #as coordinates can be quite long
                        # string = "Id: 4 \nTag: Anatomical \nx: {} \ny: {}".format(str(x), str(y))
                        self.offsetbox = TextArea(string, minimumdescent=False)
                        self.ab = AnnotationBbox(self.offsetbox, (0,0), xybox=(50., 50.), xycoords='data',
                                boxcoords="offset points", pad=0.5)
                                #Arrow Style: arrowprops=dict(arrowstyle='->, head_width=.5', color='white', linewidth=1, mutation_scale=.5
                        # add it to the axes and make it invisible
                        self.ax.add_artist(self.ab)

                        #change the colour of the lines
                        for line in polygon['lines']:
                            for plt in self.ax.lines:
                                if line == plt:
                                    plt.set_color("blue")

                        # get the figure size
                        w, h = self.fig.get_size_inches()*self.fig.dpi
                        ws = (event.x > w/2.)*-1 + (event.x <= w/2.)
                        hs = (event.y > h/2.)*-1 + (event.y <= h/2.)
                        # if event occurs in the top or right quadrant of the figure,
                        # change the annotation box position relative to mouse.
                        self.ab.xybox = ( 50 *ws,  50 *hs)
                        # make annotation box visible
                        self.ab.set_visible(True)
                        # place it at the position of the hovered scatter point
                        self.ab.xy =(x, y)

            if not hovered_over:
                #clear existing labels
                self.ax.artists.clear()
                #change the colour of the lines
                self.parent.reset_polygon_cols(False) #but not selected polygon if one
                if self.parent.selected_polygon != None:
                    self.parent.show_selected_plots(self.parent.selected_polygon['scatter_points'], self.ax.collections, self.selected_polygon_colour)
                    self.parent.show_selected_plots(self.parent.selected_polygon['lines'], self.ax.lines, self.selected_polygon_colour)
                # for line in self.ax.lines:
                #     line.set_color("red") #WILL NEED TO IMPORT TAG FILE LOADER COLOUR THING
            #draw to graph canvas
            # self.fig.canvas.draw_idle()
            self.fig.canvas.draw()
        else:
                #clear existing labels
            self.ax.artists.clear()
        #change the colour of the lines
            self.parent.reset_polygon_cols(False)
            if self.parent.selected_polygon != None:
                self.parent.show_selected_plots(self.parent.selected_polygon['scatter_points'], self.ax.collections, self.selected_polygon_colour)
                self.parent.show_selected_plots(self.parent.selected_polygon['lines'], self.ax.lines, self.selected_polygon_colour)
            # for line in self.ax.lines:
            #     line.set_color("red") #WILL NEED TO IMPORT TAG FILE LOADER COLOUR THING
    #draw to graph canvas
            # self.fig.canvas.draw_idle()
            self.fig.canvas.draw()

    def change_selected_colour(self, new_col):
        self.selected_polygon_colour = new_col

    def update_precision_value(self, new_precision_val):
        self.precision = new_precision_val

    def update_polygon_info(self, new_polygon_info):
        self.polygon_info = new_polygon_info
