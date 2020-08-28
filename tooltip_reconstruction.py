#practice tooltip reconstruction
import tkinter as tk

root = tk.Tk()


##TOOLTIP Methods & Classes
# #A function that creates the tooltip
# def CreateToolTip(widget, text, hover_background, small_font):
#     #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
#     toolTip = ToolTip(widget, hover_background, small_font)
#     def enter(event): #to show tooltip
#         toolTip.showtip(text) #call showtip
#     def leave(event):
#         toolTip.hidetip() #hide tooltip
#     widget.bind('<Enter>', enter) #upon entry of mouse
#     widget.bind('<Leave>', leave) #upon leave of mouse

#Custom Tooltip to match the other Matplotlib toolbar buttons
class HoverToolTip:
    #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
    def __init__(self, widget, hover_background, hover_font_size, text):
        self.widget = widget
        self.text, self.tipwindow = None, None
        self.hover_background = hover_background
        self.hover_font_size = hover_font_size
        self.text = text

        self.create_tip()

    def create_tip(self):
        self.widget.bind('<Enter>', self.enter_mouse) #upon entry of mouse
        self.widget.bind('<Leave>', self.leave_mouse) #upon leave of mouse

    def enter_mouse(self, event):
        self.showtip(self.text) #call showtip

    def leave_mouse(self, event):
        self.hidetip() #hide tooltip

    def showtip(self, text):
        self.text = text
        x, y, cx, cy = self.widget.bbox("insert") #All 0 at this stage
        x = x + self.widget.winfo_rootx() + 26 #root of the widget on the x axis, 0 = left
        y = y + cy + self.widget.winfo_rooty() + 0 #root of the widget on the y axis, 0 = top
        self.tipwindow = tk.Toplevel(self.widget) #create toplevel widget
        self.tipwindow.wm_overrideredirect(1) #cannot be overrided = https://effbot.org/tkinterbook/wm.htm#wm.Wm.wm_overrideredirect-method
        self.tipwindow.wm_geometry("+%d+%d" % (x, y)) #geometry of toplevel widget
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                    background=self.hover_background, relief=tk.SOLID, borderwidth=1,
                    font=self.hover_font_size) #styling
        label.pack(ipadx=3) #padding

    def hidetip(self):
        self.tipwindow.destroy()

    def change_hover_text(self, new_text):
        self.text = new_text


frame = tk.Frame(root, width=1000, height=100)
frame.pack()

button = tk.Button(frame, text="hover over me")
button.pack(side="top", padx=10, pady=10)
# CreateToolTip(button, "Hovered", "beige", 12)
tooltip_hover = HoverToolTip(button, "beige", 12, "Hovered")

button.config(command=lambda text="Andrew": tooltip_hover.change_hover_text(text))

root.mainloop()
