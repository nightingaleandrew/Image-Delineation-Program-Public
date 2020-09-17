#script for classes that are concerning miscellaneous functions
#This follows the compartmenatislation design pattern I begin to follow in the project.I have kept them all in here for organisation purposes.

#Classes include ConvertImages for the images on Matplotlib buttons, TimeDate to pull datetime stamps, HexValidator to validate hex strings, PolygonMasker to produce a mask for polygon on figure

#Imports
from PIL import ImageTk, Image
from PIL import Image as PIL_image, ImageTk as PIL_imagetk
import time, datetime, re, cv2, os
import numpy as np

#This class converts the images for the matplotlib toolbar buttons
#I pull the actual images within the button_images.py This file contains the file, name & zoom quantity
#Uses PIL
class ConvertImages:
    def __init__(self, dict):
        self.dict = dict #takes in a dict that has a key:value with 'name': name, 'file': filelocation & zoom: zoom amount

    #Function that creates an image that can be then applied to the button when it is added. It creates image key value pair to the inputted dict from button_images
    def prepare_images(self):
        for image in self.dict:
            try:
                image['image'] = self.convert_image(image['file'], image['zoom']) #filelocation & zoom needed so can see whole image properly in button
                #adds image['image'] to this dict & returns it to the parent
            except:
                print("ERROR with loading an image for button {}, is file location '{}' correct?".format(image['name'], image['file']))
                image['image'] = None #if there is an error then just return None, if none then will not display anything
        return self.dict

    #function for converting an image so it can be displayed, also takes a zoom parameter
    def convert_image(self, image, zoom):
        #Vermeulen, B. (2019) PhotoImage zoom [Online]. Available at  https://stackoverflow.com/questions/58411250/photoimage-zoom [Accessed 09 July 2020].
        call_img = PIL_imagetk.PhotoImage(file=image) #uses PIL
        zoom_img = call_img._PhotoImage__photo.subsample(zoom)
        return zoom_img #return the zoomed image

#A class that can get a date time stamp and also return a non-formatted or formatted version of it
class TimeDate:
    def __init__(self):
        self.date_time_stamp = self.get_time_stamp() #calls the timestamp so when class is called, function runs

    #A function that calulcates the date stamp & returns a final version
    def get_time_stamp(self):
        #Timestamp To Date Converter. How To Get Current Timestamp In Python [Online]. Available at  https://timestamp.online/article/how-to-get-current-timestamp-in-python [Accessed 03 July 2020].
        #Timestamp To Date Converter. How To Convert Timestamp To Date and Time in Python [Online]. Available at  https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python [Accessed 03 July 2020].

        ts = time.time() #basic timestamp in s format from epoch - very long number!
        readable = datetime.datetime.fromtimestamp(ts).isoformat() #get readable format for the above stamp

        #Below I make it a readable format for program
        date_time = re.split("T", readable)
        date_stamp = date_time[0]
        time_stamp = date_time[1][:5]

        day = date_stamp[8:]
        month = date_stamp[5:7]
        year = date_stamp[:4]
        date_stamp_adjust = day + "-" + month + "-" + year

        final_stamp = date_stamp_adjust + " " + time_stamp
        return final_stamp

    #Return the date time stamp produced by self.get_time_stamp()
    def get_time_date_stamp(self):
        return self.date_time_stamp

    #Function that returns a further formatted version, splits off date and time to two seperate values
    def return_formatted_date_time(self):
        date_time_stamp = self.get_time_stamp()
        date = re.split(" ", date_time_stamp)[0]
        time = re.split(" ", date_time_stamp)[1]
        return date, time

#A class that manipulates a piece of information to make a string. Could contain various different format methods
class StringMaker:
    def __init__(self):
        pass

    #A method that adds the pipes in for the title of the tabs. Splits the values in a given dict & splits with pipe.
    def title_formatter(self, information):
        title = "" #empty string
        i = 0
        for key, value in information.items(): #for each key, value pair
            if i == len(information) - 1:
                title += str(value) #add in the value
            else:
                title += str(value) + " | " #add in value with a space & pipe as there will be another value after
            i += 1
        return title #return the new string

#A class that validates a given Hex value. I have done this as in the json file for settings, a user could amend the hex codes for the tags for instance. This ensures they are correct.
class HexValidator:
    def __init__(self):
        pass

    #The validate function. Supporting both 3 and 6 digit forms of hex
    def validate_value(self, value):
        #Pieters, M. How to check if a string is an rgb hex string [Online]. Available at https://stackoverflow.com/questions/20275524/how-to-check-if-a-string-is-an-rgb-hex-string [Accessed 23 July 2020].
        hex = re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$') #using regex to find if either 3 or 6 digits that contain either number or letters with hash at start
        value = bool(hex.match(value))
        return value

#Below two classes are used for the polygon mask functionality.
#Class that looks for an image. Polygon mask uses the .png images that are in the dir. Needs to check that the file exists
class ImageFinder:
    def __init__(self, file_dir, slice_name):
        self.file_dir = file_dir #folder director that the slice is within
        self.slice_name = slice_name #name of the slice within that dir (can take .npy or none)

        self.file = self.file_dir + r"/" + self.slice_name #add both together
        self.change_extension() #change the extension to .png rather than .npy or none

    #Method that checks & changes if need to the file extension. Ensures that it is .png
    def change_extension(self):
        if self.file.endswith(".npy"): #if the slice extension ends with .npy then swap with .png
            self.file = self.file[:-4]
            self.file = self.file + ".png"
        elif self.file.endswith(".png"): #already ends with .png
            pass
        else: #if slice name does not end with any extension, add .png
            self.file = self.file + ".png"

    #Check file exists. If is then return filename, if not then return None
    def check_exists(self):
        #Guru99. Python Check if File or Directory Exists [Online]. Available at https://www.guru99.com/python-check-if-file-exists.html [Accessed 05 September 2020].
        if os.path.exists(self.file):
            return self.file
        else:
            print("Image file does not exist.")
            return None

#Class that creates a mask that just shows the polygon on a black background.
class PolygonMasker:
    def __init__(self, polygon_coordinates, image_file):
        self.polygon_co_ordinates = polygon_coordinates #takes in coordinates
        self.image_file = image_file #takes in .png file
        self.crop_width_height = (128, 128) #crop dimensions as using png rather than numpy array

    #As I am using the png rather than the numpy array, the png needs to be cropped. I use this to crop the array from the centre to dimensions of 128, 128
    def crop_center(self, img, cropx, cropy):
        y, x, z = img.shape
        startx = x//2-(cropx//2) #need to find top left of crop box and bottom right - dividing by 2 makes it centre.
        starty = y//2-(cropy//2)
        return img[starty:starty+cropy,startx:startx+cropx].copy() #.copy creates a new image rather than changing original

    #Function to read the image
    def read_image(self, image_file):
        image = cv2.imread(image_file) #read image into cv2
        return image

    #Function that applies a mask np.zeros to the same size img & then adjusts it show polygon contours
    def apply_mask(self, colour):
        #user1361529. (2019) Blackout image except for polygons provided as coordinates in OpenCV (Python) [Online]. Available at https://stackoverflow.com/questions/54466916/blackout-image-except-for-polygons-provided-as-coordinates-in-opencv-python [Accessed 07 September 2020].
        image = self.read_image(self.image_file) #read the image
        image = self.crop_center(image, self.crop_width_height[0], self.crop_width_height[1]) #crop the image

        contours = np.array(self.polygon_co_ordinates, dtype=np.int32) #find contours for polygon

        mask = np.zeros(image.shape, dtype=np.uint8) #get a black mask - vals of 0 for same size of image, polygon is white here

        if colour:
            cv2.fillPoly(mask, pts=[contours], color=(255,255,255)) #apply mask, 255 pushes colour values through
            mask = cv2.bitwise_and(image, mask) # apply the mask

        return mask #return the masked version of the image

    #Function to write the image, could be used with a save dialog box etc
    def write_image(self, masked_image, filename):
        cv2.imwrite(filename, masked_image) #write image to filename dir

#If i need to black/white mask
#Katerina. (2019) Create mask by coordinates of multiple convex polygons [Online]. Available at https://stackoverflow.com/questions/37905271/create-mask-by-coordinates-of-multiple-convex-polygons [Accessed 07 September 2020].
