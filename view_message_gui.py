import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from gui_components import *

class view_message_GUI(tk.Frame):
    def __init__(self, master, gmail, width =  100):
        super().__init__(master, width = width)
        self.gmail = gmail                                          #save email service
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
        
        #Create entry objects
        self.subjectLabel = tk.Label(master = self, text="", justify = 'left')        #email subject
        self.fromLabel = tk.Label(master = self, text="", justify = 'left')           #email from
        self.toLabel = tk.Label(master = self, text="", justify = 'left')             #email to
        self.ccLabel = tk.Label(master = self, text="", justify = 'left')             #email cc

        #Buttons
        self.downloadBtn = tk.Button(master = self, text = "Download Attachments", \
            command = self.download)
        
        #create text box for body
        self.bodyLabel = tk.Label(master = self, text="", justify='left', wraplength=500)        #email subject
        
        #Store widgets into lists for iterating
        self.widgets = [self.fromLabel, self.toLabel, self.ccLabel, self.bodyLabel, self.subjectLabel]
        
    def download(self):
        if self.message == {}:
            return
        self.gmail.parse_parts(self.message['parts'], filedialog.askdirectory(),self.message['id'])
        messagebox.showinfo("Attachments", "Download Successful")

    def updateDisplay(self, message):
        self.message = message
        self.subjectLabel['text'] = message['subject']
        self.fromLabel['text'] = 'From: ' + message['from name']
        self.toLabel['text'] = 'To: ' + message['to']
        self.ccLabel['text'] = 'CC: ' + message['cc']
        self.bodyLabel['text'] = message['body']

    def build(self): #display components on the screen
        self.subjectLabel.grid(row = 0 , column = 0, sticky='W')
        self.fromLabel.grid(row = 1, column = 0, sticky='W')
        self.toLabel.grid(row = 2, column = 0, sticky='W')
        if (self.message['cc'] != 'N/A'):
            self.ccLabel.grid(row = 3, column = 0, sticky='W')
        self.downloadBtn.grid(row = 4, column=0, sticky='W')
        self.bodyLabel.grid(row = 5, column = 0, sticky='W')

    def hide(self):
        for w in self.widgets:                              #hide other widgets
            w.grid_remove()
            
    def destroy(self):
        for w in self.widgets:                              #destroy other widgets
            w.destroy()
        tk.Frame.destroy(self)                              #destroy frame