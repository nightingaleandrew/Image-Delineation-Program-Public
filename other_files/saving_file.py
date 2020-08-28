#practice saving file, as I cannot seem to manipulate the tkinter save dialog 
a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")),
            defaultextension='.png', title="Window-2")
plt.savefig(a)
