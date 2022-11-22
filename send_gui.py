import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
from gui_components import *

class send_GUI(tk.Frame):
    def __init__(self, master, gmail, width =  100):
        super().__init__(master, width = width)
        self.gmail = gmail                                          #save email service
        self.title = tk.Label(master = self, text="Compose Email")  #title for compose email
        self.attachments = []                                       #list for attachments    
        
        #Create entry objects
        self.to_entry = EntryField(master = self, field = 'To:', width = width)
        self.subject_entry = EntryField(master = self, field = 'Subject:', width = width)
        self.cc_entry = EntryField(master = self, field = 'CC:', width = width)
        self.bcc_entry = EntryField(master = self, field = 'BCC:', width = width)

        #create text box for body
        self.body = tk.Text(master = self)

        #controls for the send GUI
        self.control_frame = tk.Frame(master = self) #frame to store
        
        #Buttons
        self.delete_bttn = tk.Button(master = self.control_frame, text = "Delete", command = self.delete_txt)
        self.send_bttn = tk.Button(master = self.control_frame, text = "Send", command = self.send_email)
        self.attach_bttn = tk.Button(master = self.control_frame, text = "Add Attachments", command = self.select_attachemnt)
        self.del_attach_bttn = tk.Button(master = self.control_frame, text = "Remove Attachments", command = self.del_attachment)
        self.view_attach_bttn = tk.Button(master = self.control_frame, text = "View Attachments", command = self.show_attachments)
        
        #Store widgets into lists for iterating
        self.entryfields = [self.to_entry, self.subject_entry,self.cc_entry, self.bcc_entry]
        self.widgets = [self.title, self.body, self.control_frame, self.delete_bttn, self.send_bttn, self.attach_bttn,\
            self.del_attach_bttn, self.view_attach_bttn]
        
    def select_attachemnt(self):
        fp = list(askopenfilenames(filetypes=[ ("All Files", "*.*")]))  #get file path
        if not fp:                                                      
            return
        for fileName in fp:                                             #for each filename    
            if fileName not in self.attachments:                        #add if it is a
                self.attachments.append(fileName)                       #new file

    def del_attachment(self):
        self.attachments = [] #clear list

    def show_attachments(self):
        #Create a message window showing that no files are selected or which were chosen
        outStr = "The following files are attached:" if  len(self.attachments) > 0 else "There are no files."
        for fp in self.attachments:
            outStr += "\n" + str(fp)
        messagebox.showinfo("Attachments", outStr)

    def build(self): #display components on the screen
        self.title.grid(row = 0,column = 0)
        
        self.to_entry.grid(row= 1, column = 0, sticky ='WE')
        self.subject_entry.grid(row= 2, column = 0, sticky ='WE')
        self.cc_entry.grid(row= 3, column = 0, sticky ='WE')
        self.bcc_entry.grid(row= 4, column = 0, sticky ='WE')
        
        for field in self.entryfields:
            field.build()
            
        self.body.grid(row = 5, column=0, sticky ='WE')
        self.control_frame.grid(row= 6, column = 0, sticky ='WE')
        self.send_bttn.grid(row= 0, column = 0, sticky ='WE')
        self.delete_bttn.grid(row = 0, column = 1, sticky ='WE')
        self.attach_bttn.grid(row = 0, column = 2, sticky ='WE')
        self.del_attach_bttn.grid(row = 0, column = 3, sticky ='WE')
        self.view_attach_bttn.grid(row = 0, column = 4, sticky ='WE')
        self.delete_txt() #reset text

    def send_email(self):
        message = {
            'to': self.to_entry.getData().replace(" ", ""), #create dictionary with 
            'subject': self.subject_entry.getData(),        #data from the GUI
            'body': self.body.get(1.0, tk.END),
            'cc': self.cc_entry.getData().replace(" ", "" ),
            'bcc': self.bcc_entry.getData().replace(" ", "" ),
            }
        
        self.gmail.send_message(message, self.attachments)  #send email
        self.delete_txt()                                   #reset GUI
        
    def delete_txt(self):
        self.attachments = []                               #clear attachments
        for field in self.entryfields:                      #reset fields
            field.reset()
        self.body.delete(1.0, tk.END)                       #delete body
    
    def hide_widgets(self):
        for field in self.entryfields:                      #hide entry
            field.hide()
        for w in self.widgets:                              #hide other widgets
            w.grid_remove()
            
    def destroy(self):
        for field in self.entryfields:                      #delete entry
            field.delete()
        for w in self.widgets:                              #destroy other widgets
            w.destroy()
        tk.Frame.destroy(self)                              #destroy frame