import tkinter as tk

window_width = 1280
window_height = 720
window_geometry = str(window_width)+'x'+str(window_height)

class EntryField(tk.Frame):
    def __init__(self, master, field):
        super().__init__(master)
        self.field_label = tk.Label(master = self, text=field + '\t')       #create label
        self.field_entry = tk.Entry(master = self)   #create entry
    
    def build(self):  #display components
        self.field_label.pack(side= 'left')
        self.field_entry.pack(side= 'left', fill = 'x',expand=True, padx=10)
        self.field_entry.delete(0, tk.END )
    
    def reset(self):    #delete data from field
        self.field_entry.delete(0, tk.END )
        
    def hide(self):     #remove from grid to hide
        self.field_label.pack_forget()
        self.field_entry.pack_forget()

    def delete(self):   #destroy
        self.field_label.destroy()
        self.field_entry.destroy()
    
    def getData(self):  #return data
        return self.field_entry.get()


#credits: https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
#modifications were made for use in the application

class ScrollFrame(tk.Frame):
    def __init__(self, parent, w = window_width, h = window_height):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, borderwidth=0, width = w, height= h)          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, width=w, height = h)                  #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of frame
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((0,0), window=self.viewPort, #create window sticky to northwest
        anchor="nw", tags="self.viewPort")                                          #add view port frame to canvas
        self.viewPort.bind("<Configure>", self.ResizeFrame)                       #bind an event whenever the size of the viewPort frame changes.
        #self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the canvas frame changes.
        self.ResizeFrame()                                                          #get the initial size

    def ResizeFrame(self, event = None):  #Reset the scroll region to the size of the frame                                           
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                