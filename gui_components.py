import tkinter as tk
import platform

window_width = 1280
window_height = 720
window_geometry = str(window_width)+'x'+str(window_height)

class EntryField(tk.Frame):
    def __init__(self, master, field):
        super().__init__(master)
        self.field_label = tk.Label(master = self, text=field + '\t')#create label
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
        self.viewPort = tk.Frame(self.canvas, width=w, height = h)                  #place a frame on the canvas
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #set canvas to scroll

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of frame
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left and fill
        self.canvas_window = self.canvas.create_window((0,0), window=self.viewPort, #create window sticky to northwest
        anchor="nw", tags="self.viewPort")                                          #add view port frame to canvas
        self.viewPort.bind("<Configure>", self.ResizeFrame)                         #resize scrollbar when it changes.
        self.viewPort.bind('<Enter>', self.onEnter)                                 #bind scroll when the cursor enters the frame
        self.viewPort.bind('<Leave>', self.onLeave)                                 #unbind scroll when the cursor leaves the frame
        self.ResizeFrame()                                                          #get the initial size

    def onMouseWheel(self, event):                                                  # cross platform scroll wheel event
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    
    def onEnter(self, event):                                                      #bind scroll when the cursor enters the frame
        if platform.system() == 'Linux':                                           #wheel scroll for linux
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:                                                                      #wheel scroll for othe platforms
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
    
    def onLeave(self, event):                                                      #unbind scroll when the cursor leaves the frame
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

    def resetView(self):                    #move view to the top
        self.canvas.yview_moveto('0')

    def ResizeFrame(self, event = None):    #Reset the scroll region to the size of the frame   
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))    

