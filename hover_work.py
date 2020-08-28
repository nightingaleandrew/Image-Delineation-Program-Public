# import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea
import matplotlib
matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

from check_json_files import SetSettings, TagFileLoader

root = tk.Tk()

class Annotation:
    def __init__(self, frame):
        self.frame = frame

        TAGS_DATA_FILENAME = r".\tags.json"
        settings_data_filename = r".\settings.json"


        tags_writer = TagFileLoader(TAGS_DATA_FILENAME)
        self.tags = tags_writer.return_tags()

        settings_file = SetSettings(settings_data_filename)
        self.settings = settings_file.settings #These are the settings that are used for the program while it is live.

        image = r'C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\t2-axial\PR150_01_0006_002_t2-axial.npy'
        #graph details
        self.polygon_info = [{"id": 1, "tag": "Anatomical", "co-ordinates": [(23, 56), (45, 23), (29, 90), (23, 56)]},
                            {"id": 2, "tag": "Suspicious", "co-ordinates": [(80, 60), (120, 110), (90, 23), (66, 19), (80, 60)]}]

        # self.co_ordinates = [(23, 56), (45, 23), (29, 90), (23, 56)]
        # self.x = [23, 45, 29, 23]
        # self.y = [56, 23, 90, 56]
        self.precision = 5

        # create figure and plot scatter
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        img_arrayOne = np.load(image) #load the image
        img = np.squeeze(img_arrayOne) #comes up a blue/green otherwise
        self.ax.imshow(img, cmap="gray")
        self.ax.grid(False) #remove the default gridlines
        self.ax.axis("off") #take axes off

        for polygon in self.polygon_info:
            x, y = [], []
            for coord in polygon['co-ordinates']:
                x.append(coord[0])
                y.append(coord[1])
            line = self.ax.plot(x, y, color="red", marker="o")
            polygon['lines'] = line
            polygon['scatter_points'] = []

            self.fig.canvas = FigureCanvasTkAgg(self.fig, self.frame) #would normally run plot.show() but show in tkinter window
     #canvas.show does not work anymore
            self.fig.canvas.get_tk_widget().pack(side=tk.LEFT, fill="x", expand=True)


            #calls hover class
            hovering_work = PolygonHover(self, self.polygon_info, self.precision, self.fig, self.ax, "blue") #calling the hover class
            self.fig.canvas.mpl_connect('motion_notify_event', lambda e: hovering_work.hover(e) ) #calls hover method on the motion notify event, do not need to change the hover class

            self.fig.canvas.draw()

    # self.xybox=(50., 50.)
    #reset the polygon colours back to their originals when for instance one is selected after another has already been selected
    def reset_polygon_cols(self):
        for polygon in self.polygon_info:
            for plot in self.ax.lines:
                if plot in polygon['lines']:
                    plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
            if len(polygon['scatter_points']) > 0:
                for plot in self.ax.collections:
                    if plot in polygon['scatter_points']:
                        plot.set_color(self.get_colour(polygon['tag'])) #uses get colour tag func
        # self.draw_figure()
        self.fig.canvas.draw()

    #function that pulls in the settings that are saved for polygon tags colours
    def get_colour(self, tag):
        colour = False
        for preset in self.tags:
            if preset['label'].capitalize() == tag: #tag needs capitalising
                colour = True
                return preset['colour'] #colour goes with the custom made tag in the settings
        #Return polygons in colours where there are no tags present as in Pink colour - have this setable in the settings
        if not colour:
            return [item['current_value'] for item in self.settings if item['setting'] == "Unknown Tag Colour"][0]

#To Do:
#WILL NEED TO IMPORT TAG FILE LOADER COLOUR THING for default colours
#CHECK POLYGON INFO LOOKS LIKE

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
                self.parent.reset_polygon_cols()
                # for line in self.ax.lines:
                #     line.set_color("red") #WILL NEED TO IMPORT TAG FILE LOADER COLOUR THING
            #draw to graph canvas
            # self.fig.canvas.draw_idle()
            self.fig.canvas.draw()
        else:
                #clear existing labels
            self.ax.artists.clear()
        #change the colour of the lines
            self.parent.reset_polygon_cols()
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

annotate = Annotation(root)

root.mainloop()
