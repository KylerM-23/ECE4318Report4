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
    def __init__(self, master, message, maxChar = 30, w = 150):
        super().__init__(master)
        self.master = master

        messageKeys = message.keys()
        outMessage = {}

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)

        for key in ['from name', 'subject', 'snippet', 'date']:
            outMessage[key] = message[key] if (key in messageKeys) else 'N/A'
            print(repr(outMessage[key]))

        for key in ['subject', 'snippet']:
            outMessage[key] = outMessage[key] if (len (outMessage[key]) < maxChar) \
                                                else outMessage[key][0:maxChar] + '...'


        self.fromLabel = tk.Label(master = self, text = outMessage['from name'], width=int(w/4.5), anchor='w')
        self.dateLabel = tk.Label(master = self, text = outMessage['date'], width=int(w/6), anchor='e')
        self.fromLabel.grid(row = 0, column = 0)
        self.dateLabel.grid(row = 0, column = 2)

        self.txtFrame = tk.Frame(master = self)
        self.txtFrame.grid(row = 0, column= 1, sticky= 'WE')

        self.subjectLabel = tk.Label(master = self.txtFrame, text = outMessage['subject'], anchor='w')
        self.snippetLabel = tk.Label(master = self.txtFrame, text = outMessage['snippet'], anchor='e')

        self.subjectLabel.pack(side=tk.LEFT)
        self.snippetLabel.pack(side=tk.RIGHT)