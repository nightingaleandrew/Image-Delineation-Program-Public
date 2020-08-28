import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

root = tk.Tk()

class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

frame = tk.Frame(root, bg="brown")
frame.pack(side="left", fill="both", expand=True)

xscrollbarframe = tk.Frame(frame, bg="blue")
xscrollbarframe.pack(side="bottom", expand=False, fill="x")

vscrollbarframe = tk.Frame(frame, bg="yellow")
vscrollbarframe.pack(side="right", expand=False, fill="y")

canvas = tk.Canvas(frame, bg="red")
canvas.pack(side="left", anchor="nw", expand=True, fill="both")



vscrollbar = tk.Scrollbar(vscrollbarframe, orient=tk.VERTICAL)
vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

xscrollbar = tk.Scrollbar(xscrollbarframe, orient=tk.HORIZONTAL)
xscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

xscrollbar.config(command=canvas.xview, bg="yellow")
vscrollbar.config(command=canvas.yview, bg="yellow")

canvas.config(yscrollcommand=vscrollbar.set, xscrollcommand=xscrollbar.set)

# reset the view
canvas.xview_moveto(0)
canvas.yview_moveto(0)

# create a frame inside the canvas which will be scrolled with it
interior = tk.Frame(canvas,  bg="green")
interior_id = canvas.create_window(0, 0, window = interior, anchor=tk.NW)

# track changes to the canvas and frame width and sync them,
# also updating the scrollbar
def _configure_canvas(event):
    # print(interior.winfo_reqwidth())
    # print(interior.winfo_reqwidth())
    if canvas.winfo_reqwidth() != canvas.winfo_width():
        # update the inner frame's width to fill the canvas
        canvas.itemconfigure(interior_id, width=canvas.winfo_width())

    # if canvas.winfo_reqheight() != canvas.winfo_height():
    #     # update the inner frame's width to fill the canvas
    #     canvas.itemconfigure(interior_id, height=canvas.winfo_height())
canvas.bind('<Configure>', _configure_canvas)

def _configure_interior(event):
    # update the scrollbars to match the size of the inner frame
    size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
    canvas.config(scrollregion="0 0 %s %s" % size)
    if interior.winfo_reqwidth() != canvas.winfo_width():
        # update the canvas's width to fit the inner frame
        canvas.config(width=interior.winfo_reqwidth())

    if interior.winfo_reqwidth() != canvas.winfo_width():
        # update the canvas's width to fit the inner frame
        canvas.config(width=interior.winfo_reqwidth())

    # if interior.winfo_reqheight() != canvas.winfo_height():
    #     # update the canvas's width to fit the inner frame
    #     canvas.config(height=interior.winfo_reqheight())
interior.bind('<Configure>', _configure_interior)


label = tk.Label(interior, text="Hello")
label.pack()
image_file = r"C:\Users\Andrew\Documents\DummyApp\images\click\dingy_skipper.jpg"

img = ImageTk.PhotoImage(Image.open(image_file))
image = tk.Label(interior, image=img)
image.pack()

root.mainloop()
