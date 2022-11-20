import tkinter as tk
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

class inboxEmail(tk.Frame):
    def __init__(self, master, message, maxChar = 20):
        super().__init__(master)
        self.master = master

        messageKeys = message.keys()
        outMessage = {}

        for key in ['from name', 'subject', 'snippet', 'date']:
            outMessage[key] = message[key] if (key in messageKeys) else 'N/A'

        self.fromLabel = tk.Label(master = self, text = outMessage['from name'])
        self.dateLabel = tk.Label(master = self, text = outMessage['date'])


        self.fromLabel.pack(side = 'left',anchor="w")

        self.txtFrame = tk.Frame(master = self)
        self.txtFrame.pack(side = 'left', anchor="w")

        self.subjectLabel = tk.Label(master = self.txtFrame, text = outMessage['subject'])
        self.snippetLabel = tk.Label(master = self.txtFrame, text = outMessage['snippet'])

        self.subjectLabel.grid(row = 0, column = 0)
        self.snippetLabel.grid(row = 0, column = 1)

        self.dateLabel.pack(side = 'right', anchor="e")

        #self.fromLabel.grid(row = 0, column = 0)
        #self.subjectLabel.grid(row = 0, column = 1)
        #self.snippetLabel.grid(row = 0, column = 2)
        #self.dateLabel.grid(row = 0, column= 3)