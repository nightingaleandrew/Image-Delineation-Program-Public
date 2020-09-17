#This file contains two classes regarding the translation of polygons:
#1) TransformationMatrixFinder to find a matrix for a particular slice
#2) PolygonTranslater to translate a polygon from one transformation matrix to another

#imports
import numpy as np
from storage_classes import jsonFileReaderWriter #used for reading the matrix of a slice

#Class that reads a json file to find the transformation matrix for that slice
class TransformationMatrixFinder:
    def __init__(self, folder, slice_name): #folder selected contains the json files, slice_name has to be a json file
        self.folder = folder
        self.slice_name = slice_name
        self.datakey = 'transf_slice2patient'

    #Method for getting the transformation matrix from the reader
    def get_transformation_matrix(self):
        try:
            file_reader = jsonFileReaderWriter(self.folder + "/" + self.slice_name + '.json', self.datakey)
            file_contents = file_reader.read_file()
            return file_contents[self.datakey] #pass through the matrix using the datakey method
        except:
            print("ERROR, finding Transformation Matrix")
            return None

#Class that translates a polygon from one slice to another using two slice transformation matrices
#for process, see method .translate_polygon()
class PolygonTranslater:
    def __init__(self, slice_a_matrix, slice_b_matrix, polygon_coords):
         #bring the two matrices in & ensure they are in the correct format
        self.slice_a_matrix = np.matrix(slice_a_matrix)
        self.slice_b_matrix = np.matrix(slice_b_matrix)

        self.polygon_coords = polygon_coords #get the polygon coordinates

    #Multiplies a set of homogenous coordinate matrix of n amount of vertexes by a transformation matrix
    def multiply_hcoord_by_transformation(self, coords, trans_matrix):
        #Numpy. numpy.matmul [Online]. Available at: https://numpy.org/doc/stable/reference/generated/numpy.matmul.html [Accessed: 03 September 2020]
        new_matrix = []
        for coord in coords:
            new_coord = np.matmul(np.array(trans_matrix), coord) #for each coordinate multiply by transformation matrix
            new_matrix.append(new_coord) #create new matrix
        return new_matrix

    #Finds the inverse of a matrix
    def find_inverse(self, matrix):
        #Daidalos (2019) How to calculate the inverse of a matrix in python using numpy ? [Online]. Available at: https://moonbooks.org/Articles/How-to-calculate-the-inverse-of-a-matrix-in-python-using-numpy-/ [Acessed 03 September 2020]
        inverse = np.linalg.inv(matrix) #find the inverse
        return inverse

    #Creates a homogenous coordinate from a 2D (x,y) I simply just add 0 for z and 1 for w
    def make_homog(self, coords):
        for coord in coords:
            coord.append(0) #the z value
            coord.append(1) #the w value
        return coords

    #Translate the polygon to find the new coords for the new slice
    def translate_polygon(self):
        self.homogenous_coords = self.make_homog(self.polygon_coords) #make the coords homogenous
        self.product_of_matrix_slice1_homog = self.multiply_hcoord_by_transformation(self.homogenous_coords, self.slice_a_matrix) #make the
        self.inverse_slice_b = self.find_inverse(self.slice_b_matrix)
        self.product = self.multiply_hcoord_by_transformation(self.product_of_matrix_slice1_homog, self.inverse_slice_b)

        #Process
        #1. Take in matrix for Slice of which polygon is on, 2D co-ordinates of polygon & first slice's transformation matrix of stack to be translated to
        #2. Make 2D coordinates homogenous, 0 for z value & 1 for w
        #3. Multiple cooridnates of polygon with slice A transformation
        #4. Find inverse of slice B transformation
        #5. Multiple product of coordinates & slice A transformation with inverse of B transformation to find new coordinates

        return self.product
