import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox

class EntryField(tk.Frame):
    def __init__(self, master, field, width = 100):
        super().__init__(master, width = width)
        self.field_label = tk.Label(master = self, text=field + '\t')
        self.field_entry = tk.Entry(master = self, width = int(width*.8))
    
    def build(self):
        self.field_label.grid(row = 0,column = 0)
        self.field_entry.grid(row = 0, column=1, sticky='WE')
        self.field_entry.delete(0, tk.END )
    
    def reset(self):
        self.field_entry.delete(0, tk.END )
        
    def hide(self):
        self.field_label.grid_remove()
        self.field_entry.grid_remove()
    
    def getData(self):
        return self.field_entry.get()

class inboxEmail:
    def __init__(self, master, row = 0, maxChar = 80, w = 150):
        self.master = master
        self.maxChar = maxChar
        self.row = row
        self.fromLabel = tk.Label(master = self.master, width=int(w*.20), anchor = 'w')
        self.dateLabel = tk.Label(master = self.master, width=int(w*.10), anchor='e')
        self.subjectLabel = tk.Label(master = self.master, width=int(w*.25), anchor = 'w')
        self.snippetLabel = tk.Label(master = self.master, width=int(w*.45), anchor = 'w')

    def build(self):
        self.fromLabel.grid(row = self.row, column = 0)
        self.subjectLabel.grid(row = self.row, column = 1)
        self.snippetLabel.grid(row = self.row, column = 2)
        self.dateLabel.grid(row = self.row, column = 3)
        

    def refresh(self, message):
        outMessage = message

        outMessage['subject'] = outMessage['subject'] if (len (outMessage['subject']) < self.maxChar//3) \
                                                else (outMessage['subject'][0:self.maxChar//3] + '...')
        outMessage['snippet'] = outMessage['snippet'] if (len (outMessage['snippet']) < self.maxChar) \
                                                else (outMessage['snippet'][0:self.maxChar] + '...')

        self.fromLabel['text'] = outMessage['from name']
        self.dateLabel['text'] = outMessage['date']
        self.subjectLabel['text'] = outMessage['subject']
        self.snippetLabel['text'] = outMessage['snippet']
        

class send_GUI(tk.Frame):
    def __init__(self, master, gmail, width =  100):
        super().__init__(master, width = width)
        self.gmail = gmail
        self.title = tk.Label(master = self, text="Compose Email")
        self.attachments =[]
        
        self.to_entry = EntryField(master = self, field = 'To:', width = width)
        self.subject_entry = EntryField(master = self, field = 'Subject:', width = width)
        self.cc_entry = EntryField(master = self, field = 'CC:', width = width)
        self.bcc_entry = EntryField(master = self, field = 'BCC:', width = width)
        
        self.body = tk.Text(master = self)
        self.control_frame = tk.Frame(master = self)
        self.delete_bttn = tk.Button(master = self.control_frame, text = "Delete", command = self.delete_txt)
        self.send_bttn = tk.Button(master = self.control_frame, text = "Send", command = self.send_email)
        self.attach_bttn = tk.Button(master = self.control_frame, text = "Add Attachments", command = self.select_attachemnt)
        self.del_attach_bttn = tk.Button(master = self.control_frame, text = "Remove Attachments", command = self.del_attachment)
        self.view_attach_bttn = tk.Button(master = self.control_frame, text = "View Attachments", command = self.show_attachments)
        
        self.entryfields = [self.to_entry, self.subject_entry,self.cc_entry, self.bcc_entry]
        self.widgets = [self.title, self.body, self.control_frame, self.delete_bttn, self.send_bttn, self.attach_bttn,\
            self.del_attach_bttn, self.view_attach_bttn]
        
    def del_attachment(self):
        self.attachments = []

    def show_attachments(self):
        outStr = "The following files are attached:" if  len(self.attachments) > 0 else "There are no files."
        for fp in self.attachments:
            outStr += "\n" + str(fp)
        messagebox.showinfo("Attachments", outStr)

    def build(self):
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
        self.delete_txt()
        
    def select_attachemnt(self):
        fp = list(askopenfilenames(filetypes=[ ("All Files", "*.*")]))
        if not fp:
            return
        for fileName in fp:
            if fileName not in self.attachments:
                self.attachments.append(fileName)

    def send_email(self):
        message = {
            'to': self.to_entry.getData().replace(" ", ""),
            'subject': self.subject_entry.getData(),
            'body': self.body.get(1.0, tk.END),
            'cc': self.cc_entry.getData().replace(" ", "" ),
            'bcc': self.bcc_entry.getData().replace(" ", "" ),
            }
        
        self.delete_txt()
        self.gmail.send_message(message)
        
    def delete_txt(self):
        self.attachments = []
        for field in self.entryfields:
            field.reset()
        self.body.delete(1.0, tk.END)
    
    def hide_widgets(self):
        self.to_entry.hide()
        self.subject_entry.hide()
        self.cc_entry.hide()
        self.bcc_entry.hide()
        
        for w in self.widgets:
            w.grid_remove()
            
    def destroy(self):
        for w in self.widgets:
            w.destroy()
        tk.Frame.destroy(self)