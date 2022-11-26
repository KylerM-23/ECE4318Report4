import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from gui_components import *

class view_message_GUI(tk.Frame):
    def __init__(self, master, gmail, width =  window_width//2):
        super().__init__(master, width = width)
        self.gmail = gmail                                          #save email service
        self.msgFrame = ScrollFrame(self, w = width)                #create frame to store emails
        self.msgFrame.grid(row = 0, column = 0, sticky='NS')
        self.message = {                                            #default values
                'from name': 'Missing Sender', 
                'from email': 'Missing Email', 
                'to': 'N/A',
                'cc': 'N/A',
                'subject': 'Subject N/A', 
                'date': 'No Date',
                'snippet': ' ', 
                'body': ' '
            }   
        
        self.built = False

        #Create entry objects for the subject, from, to, and cc
        self.subjectLabel = tk.Label(master = self.msgFrame.viewPort, text="", justify = 'left', wraplength=width)        
        self.fromLabel = tk.Label(master = self.msgFrame.viewPort, text="", justify = 'left', wraplength=width)           
        self.toLabel = tk.Label(master = self.msgFrame.viewPort, text="", justify = 'left', wraplength=width)            
        self.ccLabel = tk.Label(master = self.msgFrame.viewPort, text="", justify = 'left', wraplength=width)            

        #Buttons
        self.downloadBtn = tk.Button(master = self.msgFrame.viewPort, text = "Download Attachments", \
            command = self.download)
        
        #create text box for body
        self.bodyLabel = tk.Label(master = self.msgFrame.viewPort, text="", justify='left', wraplength=width)
        
        #Store widgets into lists for iterating
        self.widgets = [self.fromLabel, self.toLabel, self.ccLabel, self.bodyLabel, \
             self.downloadBtn, self.subjectLabel]
        
    def download(self):
        savedir = filedialog.askdirectory()                                         #get folder to save to
        if savedir:
            self.gmail.parse_parts(self.message['parts'], savedir,self.message)   #download attachments
            messagebox.showinfo("Attachments", "Download Complete")                     #Status Complete

    def cleartxt(self):                 #clear values to default
        self.subjectLabel['text'] =''
        self.fromLabel['text'] = ''
        self.toLabel['text'] = ''
        self.ccLabel['text'] = 'N/A'
        self.bodyLabel['text'] = ''

    def updateDisplay(self, message):   #update GUI data and reset view
        self.cleartxt()
        if not self.built:              #only build if not build
            self.build()
        self.message = message
        self.subjectLabel['text'] = message['subject']
        self.fromLabel['text'] = 'From: ' + message['from name']
        self.toLabel['text'] = 'To: ' + message['to']
        if (self.message['cc'] != 'N/A'):
            self.ccLabel['text'] = 'CC: ' + message['cc']
        self.bodyLabel['text'] = message['body']
        self.msgFrame.resetView() 

    def build(self): #display components on the screen and resize GUI
        self.subjectLabel.grid(row = 0 , column = 0, sticky='W')
        self.fromLabel.grid(row = 1, column = 0, sticky='W')
        self.toLabel.grid(row = 2, column = 0, sticky='W')
        if (self.message['cc'] != 'N/A' and self.message['cc'] != ''):
            self.ccLabel.grid(row = 3, column = 0, sticky='W')
        self.downloadBtn.grid(row = 4, column=0, sticky='W')
        self.bodyLabel.grid(row = 5, column = 0, sticky='W')
        self.msgFrame.ResizeFrame() 

    def hide(self):
        for w in self.widgets:                              #hide other widgets
            w.grid_remove()
            
    def destroy(self):
        for w in self.widgets:                              #destroy other widgets
            w.destroy()
        tk.Frame.destroy(self)                              #destroy frame