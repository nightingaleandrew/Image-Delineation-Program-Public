#File for classes regarding the figure. For instance Hover, MouseClick or Intersector.

#imports
# import tkinter as tk
# import tkinter.ttk as ttk
import numpy as np, os

import matplotlib
matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#Harry. (2020) from matplotlib.backends import _tkagg ImportError: cannot import name _tkagg [Online]. Available at: https://stackoverflow.com/questions/32188180/from-matplotlib-backends-import-tkagg-importerror-cannot-import-name-tkagg [Accessed 08 July 2020].
from matplotlib.offsetbox import AnnotationBbox, TextArea
from matplotlib.figure import Figure

#Class for clicking the CID (mouse click)- as the same cid is being used throughout different levels of classes
class cidPress():
    #ImportanceOfBeingErnest (2019) How to connect and disconnect matplotlib's event handler by using another class? [Online]. Available at  https://stackoverflow.com/questions/58322945/how-to-connect-and-disconnect-matplotlibs-event-handler-by-using-another-class [Accessed 07 July 2020].
    def __init__(self, figure):
        self.figure = figure
        self.cidpress = None #variable is declared as disconnect may be called before

    #To connect the cid to the appropiate function, function is passed through eg. drawing or selecting polgyon
    def connect(self, function):
        self.cidpress = self.figure.canvas.mpl_connect('button_press_event', function)

    #To disconnect the cid or mouse click
    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidpress)

#Class for hovering over the graph (mouse move)- with the intention of bringing up polygon data in a hover box
class cidHover():
    #Matplotlib. Event handling and picking [Online]. Available at: https://matplotlib.org/3.1.1/users/event_handling.html [Accessed 03 August 2020].
    def __init__(self, figure):
        self.figure = figure
        self.cidhover = None #variable is declared as disconnect may be called before

    #To connect the cid to the appropiate function, function is passed through eg. hovering over a polygon
    def connect(self, function):
        self.cidhover = self.figure.canvas.mpl_connect('motion_notify_event', function) #using the motion notify event

    #To disconnect the cid
    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidhover)

#class to see if the proposed line by the user intersects any existing polygons.
#This is used for preventing an override between the polygons on the figure. User can look to override this if wanted
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
        for x, y in polygon_co_ordinates: #I convert them all to tuples just for neatness (this is not essential)
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
        #Rosettacode. Find the intersection of two lines [Online]. Available at: https://rosettacode.org/wiki/Find_the_intersection_of_two_lines#Python [Accessed 19 July 2020].

        #split up x and y co-ordinates for line A and line B
        Ax1, Ay1, Ax2, Ay2 = lineA[0][0], lineA[0][1], lineA[1][0], lineA[1][1]
        Bx1, By1, Bx2, By2 = lineB[0][0], lineB[0][1], lineB[1][0], lineB[1][1]

        # difference in y axis for Line b * difference in x axis for line A subtract difference in x axis for line B * difference in y axis for line A
        d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
        if d:
            uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
            uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
        else:
            return None #return None as none intersection
        if not(0 <= uA <= 1 and 0 <= uB <= 1):
            return None #return none as no intersection
        x = Ax1 + uA * (Ax2 - Ax1)
        y = Ay1 + uA * (Ay2 - Ay1)
        return x, y #return x, y tuple of intersection pt

    #function that returns a result if there is an intersection or not
    def find_intersection(self, lineA): #proposed line is passed through here
        intersection = False #assumes there is no intersection
        for polygon in self.polygon_lines:
            for line in polygon:
                intersect = self.line_intersect(lineA, line) #if this returns an intersection then return co-ordinate of intersection, if not returns None
                if intersect != None:
                    intersection = True #intersection is True if there is an intersection co-ordinate
        return intersection

# custom toolbar as I change the hover text for default buttons, I also change the text in bottom right if zoom clicked
#This further customises the bottom right coordinates to create more space for buttons
class CustomToolbar(NavigationToolbar2Tk):
    #ebarr. Matplotlib/Tkinter - customizing toolbar tooltips [Online]. Available at: https://stackoverflow.com/questions/23172916/matplotlib-tkinter-customizing-toolbar-tooltips [Accessed 29 July 2020].

    def __init__(self, canvas_, parent_, mouse_click):
        self.clicked = None
        self.mouse_click = mouse_click
        self.toolitems = (
            ('Home', 'Reset Slice View', 'home', 'home'), #My tooltips are 2nd here
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
    #Pan Function for toolbar, I adjust it so it disconnects the mouse click eg. if draw was clicked & also flash a message bottom right to let user know.
    def pan(self):
        NavigationToolbar2Tk.pan(self)

        if self.clicked != "PAN":
            self.clicked = "PAN"
            self.mode = "PAN CLICKED"
        else:
            self.clicked = None
            self.mode = "PAN UNCLICKED"
        self.set_message(self.mode) #the message in the bottom right hand corner to user

        self.mouse_click.disconnect() #disconnect the mouse click on zoom click (edit or draw may be clicked)

    #Zoom Function for toolbar, I adjust it so it disconnects the mouse click eg. if draw was clicked & also flash a message bottom right to let user know.
    def zoom(self):
        NavigationToolbar2Tk.zoom(self)

        if self.clicked != "ZOOM":
            self.clicked = "ZOOM"
            self.mode = "ZOOM CLICKED" #Says "zoom rect" by default - Let User know Zoom is clicked
        else:
            self.clicked = None
            self.mode = "ZOOM UNCLICKED" #Says "zoom rect" by default - Let User know Zoom is unclicked
        self.set_message(self.mode) #the message in the bottom right hand corner to user

        self.mouse_click.disconnect() #disconnect the mouse click on zoom click (edit or draw may be clicked)

    #This is a function that unclicks pan or zoom if they are clicked. If draw is clicked then wanting to zoom in to continue. It will now not draw when figure is selected to zoom.
    def unclick_pan_zoom(self):
        if self.clicked != None:
            if self.clicked == "ZOOM":
                self.zoom() #invoke each method as in clicking it
            elif self.clicked == "PAN":
                self.pan()

    #This is called by the main.py for when the cursor leaves the figure. It resets the message to nothing to let the user know that cursor is left
    def left_figure(self, event):
        self.mode = ""
        self.set_message(self.mode)

    #For mouse move, I change the coordinates format. Have to make sure that it's formatted nicely so I structure it to 1.dp.
    def mouse_move(self, event):
        NavigationToolbar2Tk.mouse_move(self, event)
        #ImportanceOfBeingErnest. matplotlib imshow formatting from cursor position [Online]. Available at: https://stackoverflow.com/questions/47082466/matplotlib-imshow-formatting-from-cursor-position [Accessed 01 September 2020].
        if event.inaxes and event.inaxes.get_navigate():

            #This below can be made a lot better. Need to re-work to make it a lot cleaner
            data = [event.xdata, event.ydata] #I have done the quick algorithm on the left becuase it then always goes to 1.dp.
            formatted_data = []               #This looks better than a standard slice but also does not jig the figure around at all still even in ZOOM is clicked
            for item in data:

                dp_index = str(item).find(".") #use this for reconstruction

                if len(str(item)) > 3:
                    if str(item)[3] == ".":
                        if len(str(item)) < 5:
                            short_ver = str(item)
                        else:
                            short_ver = str(item)[:5]
                    else:
                        short_ver = str(item)[:4]
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

#A class to show the polygon details in the hover label when the mouse moves above a polygon vertex
class PolygonHover:
    def __init__(self, parent, polygon_info, precision, figure, axis, selected_colour): #takes in the polygon info, & then precision, figure, axis values
        self.parent = parent
        self.polygon_info = polygon_info
        self.precision = precision
        self.fig = figure
        self.ax = axis
        self.selected_polygon_colour = selected_colour

    def hover(self, event):
        # print("HOVER INFO", self.polygon_info)
        #ImportanceOfBeingErnest (2017) Possible to make labels appear when hovering over a point in matplotlib? [Online]. Available at: https://stackoverflow.com/questions/7908636/possible-to-make-labels-appear-when-hovering-over-a-point-in-matplotlib [Accessed 03 August 2020].
        hovered_over = False #Using a Boolean for hovered over true or not as it is on mouse move motion event, so need to destroy the bbox when not over it
        if event.xdata != None: #None if the cursor is not on the figure.
            for polygon in self.polygon_info:
                for x, y in polygon['co-ordinates']:
                    if (np.abs(x - event.xdata) < self.precision) and (np.abs(y - event.ydata) < self.precision): #if hovered over a point part of a polygon

                        #Build hover label with info
                        hovered_over = True #change to true
                        self.ax.artists.clear() #clear all existing labels
                        string = "Slice: {} \nId: {} \nTag: {} \nx: {} \ny: {}".format(polygon['slice'], polygon['id'], polygon['tag'], str(x)[:6], str(y)[:6]) #as coordinates can be quite long

                        self.offsetbox = TextArea(string, minimumdescent=False)
                        self.ab = AnnotationBbox(self.offsetbox, (0,0), xybox=(50., 50.), xycoords='data', boxcoords="offset points", pad=0.5)
                        #arrowprops=dict(arrowstyle='->, head_width=.5', color='white', linewidth=1, mutation_scale=.5 #Could use Arrow
                        self.ax.add_artist(self.ab) #add box to axis

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

            self.fig.canvas.draw()
        else:
                #clear existing labels
            self.ax.artists.clear()
        #change the colour of the lines
            self.parent.reset_polygon_cols(False)
            if self.parent.selected_polygon != None:
                self.parent.show_selected_plots(self.parent.selected_polygon['scatter_points'], self.ax.collections, self.selected_polygon_colour)
                self.parent.show_selected_plots(self.parent.selected_polygon['lines'], self.ax.lines, self.selected_polygon_colour)

            self.fig.canvas.draw()

    #If selected polygon colour needs changing by settings change
    def change_selected_colour(self, new_col):
        self.selected_polygon_colour = new_col

    #If precision value needs to be updated by settings change
    def update_precision_value(self, new_precision_val):
        self.precision = new_precision_val

    def update_polygon_info(self, new_polygon_info):
        self.polygon_info = new_polygon_info
