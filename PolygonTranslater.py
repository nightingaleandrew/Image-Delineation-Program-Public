#multipling product by inverse of second slice
import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from storage_classes import jsonFileWriter, jsonFileReaderWriter

#Class that reads a json file to find the transformation matrix
class TransformationMatrixFinder:
    def __init__(self, folder, slice_name): #folder selected contains the json files, slice_name has to be a json file
        self.folder = folder
        self.slice_name = slice_name
        self.datakey = 'transf_slice2patient'

    def get_transformation_matrix(self):
        try:
            file_reader = jsonFileReaderWriter(self.folder + "/" + self.slice_name + '.json', self.datakey)
            file_contents = file_reader.read_file()
            print(file_contents)
            return file_contents[self.datakey]
        except:
            print("ERROR, finding Transformation Matrix")
            return None

#Class that translates a polygon from slice to another slice
class PolygonTranslater:
    def __init__(self, slice_a_matrix, slice_b_matrix, polygon_coords):
         #multiply the homogenous coordinates of the original slice  by transformation of that slice
        self.slice_a_matrix = slice_a_matrix
        self.slice_b_matrix = slice_b_matrix
        self.polygon_coords = polygon_coords

    #Multiplies a a homogenous coordinate matrix of n amount of vertexes by a transformation matrix
    def multiply_hcoord_by_transformation(self, coords, trans_matrix):
        #https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
        new_matrix = []
        for coord in coords:
            new_coord = np.matmul(trans_matrix, coord)
            new_matrix.append(new_coord)
        return new_matrix

    #Finds the inverse of a matrix
    def find_inverse(self, matrix):
        #https://moonbooks.org/Articles/How-to-calculate-the-inverse-of-a-matrix-in-python-using-numpy-/
        inverse = np.linalg.inv(matrix)
        return inverse

    #Creates a homogenous coordinate from a 2D (x,y)
    def make_homog(self, coords):
        for coord in coords:
            coord.append(0) #the z value
            coord.append(1) #the w value
        return coords

    #Translate the polygon to find the new coords for the new slice
    def translate_polygon(self):
        self.homogenous_coords = self.make_homog(self.polygon_coords) #make the coords homogenous
        self.product_of_matrix_slice1_homog = self.multiply_hcoord_by_transformation(self.homogenous_coords, self.slice_a_matrix) #make the
        self.inverse_slice_2 = self.find_inverse(self.slice_b_matrix)
        self.product = self.multiply_hcoord_by_transformation(self.product_of_matrix_slice1_homog, self.inverse_slice_2)

        return self.product

class ShowFigure:
    def __init__(self):
        pass

    def create_fig(slice_add, frame, polygon_cords):
        figure = Figure()
        axis = figure.add_subplot(111) #only one chart
        axis.grid(False)

        # axis.axis("off")
        slice = np.load(slice_add)
        axis.imshow(np.squeeze(slice), cmap='gray')
        canvas = FigureCanvasTkAgg(figure, frame) #would normally run plot.show() but show in tkinter window
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        xlist, ylist = [], []
        if len(polygon_cords[0]) > 2:
            for x, y, z, w in polygon_cords:
                xlist.append(x)
                ylist.append(y)
        else:
            for x, y in polygon_cords:
                xlist.append(x)
                ylist.append(y)
        axis.plot(xlist, ylist, color="#FFFFFF",  marker="o")


#mapping polygons over
# axial_slice_1 = r"C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\t2-axial\PR150_01_0006_002_t2-axial.npy"
folder_axial = r"C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\t2-axial"
slice_name_1 = "PR150_01_0006_002_t2-axial"

slice_1 = TransformationMatrixFinder(folder_axial, slice_name_1)
slice_1_matrix = slice_1.get_transformation_matrix()

# axial_slice_1_matrix = [[0.80000001192093, 0.0, 0.0, -11.716755628586],
#                         [0.0, 0.80000001192093, 0.0, -26.395897686481646],
#                         [0.0, 0.0, 3.600002288818999, -61.190799713135],
#                         [0.0, 0.0, 0.0, 1.0]]
dwi_slice_1 = r"C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\dwi-100_800_1000\PR150_01_0007_002_dwi-100_800_1000.npy" #slice 2 if dwi
dwi_slice_1_transformation_matrix = [[2.0, 0.0, 0.0, -11.716754913330007],
                                    [0.0, 2.0, 0.0, -26.39589691162],
                                    [0.0, 0.0, 3.5999984741210014, -46.790798187256],
                                    [0.0, 0.0, 0.0, 1.0]]

dwi_slice_3 = r"C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\dwi-100_800_1000\PR150_01_0007_003_dwi-100_800_1000.npy" #slice 2 if dwi
dwi_slice_3_trans = [[2.0, 0.0, 0.0,-11.716754913330007],
                [0.0, 2.0, 0.0, -26.39589691162],
                [0.0, 0.0, 3.600002288818999, -43.190799713135],
                [0.0, 0.0, 0.0, 1.0]]

axial_slice_1_polygon_coords = [[78.78125, 116.675],
                                [40.3, 20.5],
                                [110.225, 106.19375],
                                [104.85, 118.825],
                                [78.78125, 116.675]]

translater = PolygonTranslater(slice_1_matrix, dwi_slice_3_trans, axial_slice_1_polygon_coords) #put the parameters through the class
product = translater.translate_polygon() #the new coordinates
print(product)

for item in product:
    print(item[2])

#Show the figures in tkinter
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

figure = ShowFigure.create_fig(folder_axial + "/" + slice_name_1 + ".npy", frame, axial_slice_1_polygon_coords)
figure_2 = ShowFigure.create_fig(dwi_slice_3, frame, product)

root.mainloop()
