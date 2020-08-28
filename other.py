#script for classes that are concerning adjusting things

from PIL import ImageTk, Image
from PIL import Image as PIL_image, ImageTk as PIL_imagetk

import time, datetime, re

#This class converts the images for the matplotlib toolbar buttons
#I pull the actual images within the main file in SliceFigure
#Uses PIL
class ConvertImages:
    def __init__(self, dict):
        self.dict = dict #takes in a dict that has a key:value with 'name': name, 'file': filelocation & zoom: zoom amount

    def prepare_images(self):
        for image in self.dict:
            try:
                image['image'] = self.convert_image(image['file'], image['zoom']) #filelocation & zoom needed for good resolution
                #adds image['image'] to this dict & returns it to the parent
            except:
                print("ERROR with loading an image for button {}, is file location '{}' correct?".format(image['name'], image['file']))
                image['image'] = None #if there is an error then just return None, if none then will not display anything
        return self.dict

    #function for converting an image so it can be displayed, also takes a zoom parameter
    def convert_image(self, image, zoom):
        #https://stackoverflow.com/questions/58411250/photoimage-zoom
        call_img = PIL_imagetk.PhotoImage(file=image) #uses PIL
        zoom_img = call_img._PhotoImage__photo.subsample(zoom)
        return zoom_img

#A class that can get a date time stamp and also return a non-formatted or formatted version of it
class TimeDate:
    def __init__(self):
        self.date_time_stamp = self.get_time_stamp()

    #A function that calulcates the date stamp
    def get_time_stamp(self):
        #https://timestamp.online/article/how-to-get-current-timestamp-in-python
        #https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
        ts = time.time()
        readable = datetime.datetime.fromtimestamp(ts).isoformat()

        date_time = re.split("T", readable)
        date_stamp = date_time[0]
        time_stamp = date_time[1][:5]

        day = date_stamp[8:]
        month = date_stamp[5:7]
        year = date_stamp[:4]
        date_stamp_adjust = day + "-" + month + "-" + year

        final_stamp = date_stamp_adjust + " " + time_stamp
        return final_stamp

    def get_time_date_stamp(self):
        return self.date_time_stamp

    def return_formatted_date_time(self):
        date_time_stamp = self.get_time_stamp()
        date = re.split(" ", date_time_stamp)[0]
        time = re.split(" ", date_time_stamp)[1]
        return date, time

#A class that manipulates a piece of information to make a string. Maybe I can build this out
class StringMaker:
    def __init__(self):
        pass

    #A method that adds the pipes in for the title of the tabs
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

class HexValidator:
    def __init__(self):
        pass

    def validate_value(self, value):
        #supports both 3 and 6 digit forms of hex
        #https://stackoverflow.com/questions/20275524/how-to-check-if-a-string-is-an-rgb-hex-string
        hex = re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$')
        value = bool(hex.match(value))
        return value
