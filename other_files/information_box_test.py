#Class for a box of information with labels & dynamic updates
import tkinter as tk
from tkinter import ttk
#
# class InformationBox:
#     def __init__(self, parent_frame, pack_side, rows, header, info, background_col, font_col, automatic):
#         self.parent_frame = parent_frame #parent frame of the label frame
#         self.pack_side = pack_side #uses packing as default
#         self.padding = 10 #padding set centrally
#         self.rows = rows #number of rows wanted by user
#         self.header = header #title of the label frame
#         self.info = info #information through dict format to be contained
#         self.background_col = background_col #background col of label frame
#         self.font_col = font_col #font col of the label frame
#
#         self.dict = [] #this dict is used to store the information from intialisation
#
#         #parent label frame box for contents: I have created the label frame inside the class rather than outside as containing frames is less likely than just labels
#         self.content_frame = tk.LabelFrame(self.parent_frame, text = self.header.capitalize() + " :  ", foreground=self.font_col, bg=self.background_col, pady=self.padding, padx=self.padding)
#         self.content_frame.pack(side=self.pack_side, pady=self.padding, padx=self.padding)
#
#         #if no frames are to be contained inside then it can be created as the frame does not need to be passed out again
#         if automatic:
#             self.create_insides(self.info)
#
#     #pass out the frame to be the parent of inner frames that are then created outside
#     def get_parent_label_frame(self):
#         return self.content_frame
#
#     #create labels and info labels - can either be done through init or not
#     def create_insides(self, info):
#         row = 0
#         column = 0
#         padx = (0, 0)
#         for key, value in info.items():
#             label_header = tk.Label(self.content_frame, text=key.capitalize() + ": ", foreground=self.font_col, bg=self.background_col).grid(row=row, column=column, sticky="W", padx=padx)
#             #if a frame is passed through then add it in
#             if (type(value) == tk.Frame):
#                 value.grid(row=row, column=column + 1, sticky="W")
#                 label_dict = {"name": key, "value": value, "widget": value, "type": "frame"}
#             #else just stringify & add in as a label
#             else:
#                 label = tk.Label(self.content_frame, text= str(value), foreground=self.font_col, bg=self.background_col)
#                 label.grid(row=row, column=column + 1, sticky="W")
#                 label_dict = {"name": key, "value": value, "widget": label, "type": "text"}
#             self.dict.append(label_dict)
#
#             if row != self.rows:
#                 row += 1
#             if row == self.rows:
#                 column += 2
#                 row = 0
#                 padx = (25, 0)
#
#     #reset the text labels created to not applicable, better than re-creating widget
#     def reset_to_na(self):
#         for line in self.dict:
#             if line['type'] == "text":
#                 line['widget']['text'] = "n/a"
#                 line['value'] = "n/a"
#
#     #Takes in a dict of key value pairs for the current ones already installed & if label widgets, changes the text
#     def state_information(self, information):
#         for key, value in information.items():
#             for line in self.dict:
#                 if ((line['name'] == key) and (line['type'] == "text")):
#                     line['widget']['text'] = value
#                     line['value'] = value
#
#     #Pulls a detail from the dictionary
#     def pull_detail(self, label):
#         detail = None
#         for line in self.dict:
#             if ((line['name'] == label) and (line['type'] == "text")):
#                 detail = line['value']
#         return detail #if returns None then not present
#
#     #forgets the whole frame
#     def make_box_go_walkies(self):
#         self.content_frame.pack_forget()
#
#     #Changes the formatting to grid for the frame
#     def change_to_grid(self, row, col, sticky, columnspan):
#         self.make_box_go_walkies()
#         self.content_frame.grid(row=row, column=col, sticky=sticky, columnspan=columnspan, padx=self.padding, pady=self.padding)
