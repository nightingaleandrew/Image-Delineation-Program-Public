#multipling product by inverse of second slice
import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg") #backend of matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

def multiply_xyzw_by_transformation(coords, trans_matrix):
    new_matrix = []
    for coord in coords:
        new_cords = []
        for row in trans_matrix:
            new_val = (row[0] * coord[0]) + (row[1] * coord[1]) + (row[2] * coord[2]) + (row[3] * coord[3])
            new_cords.append(new_val)
        new_matrix.append(new_cords)
    return new_matrix

def find_inverse(matrix):
    #https://moonbooks.org/Articles/How-to-calculate-the-inverse-of-a-matrix-in-python-using-numpy-/
    inverse = np.linalg.inv(matrix)
    return inverse

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
axial_slice_1 = r"C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\t2-axial\PR150_01_0006_002_t2-axial.npy"
axial_slice_1_matrix = [[0.80000001192093, 0.0, 0.0, -11.716755628586],
                    [0.0, 0.80000001192093, 0.0, -26.395897686481646],
                    [0.0, 0.0, 3.600002288818999, -61.190799713135],
                    [0.0, 0.0, 0.0, 1.0]]

axial_slice_1_polygon_coords = [[78.78125, 116.675],
                            [40.3, 20.5],
                            [110.225, 106.19375],
                            [104.85, 118.825],
                            [78.78125, 116.675]]

axial_slice_1_polygon_coords_homog = [[78.78125, 116.675, 0, 1],
                            [40.3, 20.5, 0, 1],
                            [110.225, 106.19375, 0, 1],
                            [104.85, 118.825, 0, 1],
                            [78.78125, 116.675, 0, 1]]

dwi_slice_1 = r"C:\Users\Andrew\Documents\dissertation\data\proc\2018\PR150\01\dwi-100_800_1000\PR150_01_0007_002_dwi-100_800_1000.npy" #slice 2 if dwi
dwi_slice_1_transformation_matrix = [[2.0, 0.0, 0.0, -11.716754913330007],
                                    [0.0, 2.0, 0.0, -26.39589691162],
                                    [0.0, 0.0, 3.5999984741210014, -46.790798187256],
                                    [0.0, 0.0, 0.0, 1.0]]

product_of_matrix_slice1_homog = multiply_xyzw_by_transformation(axial_slice_1_polygon_coords_homog, axial_slice_1_matrix) #multiply the homogenous coordinates of the original slice  by transformation of that slice
print("product_of_matrix_slice1_homog", product_of_matrix_slice1_homog)
# manual = [[63.0250009391458, 93.3400013908745, 0, -4001.80201693483],
#             [32.2400004804135, 16.4000002443791, 0, -1012.3011544049],
#             [88.1800013139845, 16.4000002443791, 0, -1831.59529173377],
#             [83.8800012499095, 84.9550012659282, 0, -4030.58118760109],
#             [63.0250009391458, 95.0600014165045, 0, -4058.55319696076]]

inverse_slice_2 = find_inverse(dwi_slice_1_transformation_matrix)
# print("inverse", inverse_slice_2)

product = np.matmul(manual, inverse_slice_2)
print(product)

#load the first slice with polygon
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

create_fig(axial_slice_1, frame, axial_slice_1_polygon_coords)
create_fig(dwi_slice_1, frame, product)

root.mainloop()


print(product)
