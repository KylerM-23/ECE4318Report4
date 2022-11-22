import tkinter as tk

class EntryField(tk.Frame):
    def __init__(self, master, field, width = 100):
        super().__init__(master, width = width)
        self.field_label = tk.Label(master = self, text=field + '\t')       #create label
        self.field_entry = tk.Entry(master = self, width = int(width*.8))   #create entry
    
    def build(self):  #display components
        self.field_label.grid(row = 0,column = 0)
        self.field_entry.grid(row = 0, column=1, sticky='WE')
        self.field_entry.delete(0, tk.END )
    
    def reset(self):    #delete data from field
        self.field_entry.delete(0, tk.END )
        
    def hide(self):     #remove from grid to hide
        self.field_label.grid_remove()
        self.field_entry.grid_remove()

    def delete(self):   #destroy
        self.field_label.destroy()
        self.field_entry.destroy()
    
    def getData(self):  #return data
        return self.field_entry.get()

class inboxEmail:
    def __init__(self, master, row = 0, maxChar = 80, w = 150):
        self.master = master
        self.maxChar = maxChar #set the max characters
        self.row = row  #save which row the email belongs in
        self.message = None

        #create the labels for the information
        self.fromLabel = tk.Label(master = self.master, width=int(w*.20), anchor = 'w')
        self.dateLabel = tk.Label(master = self.master, width=int(w*.10), anchor='e')
        self.subjectLabel = tk.Label(master = self.master, width=int(w*.25), anchor = 'w')
        self.snippetLabel = tk.Label(master = self.master, width=int(w*.45), anchor = 'w')

    def build(self): #place elements on the screen
        self.fromLabel.grid(row = self.row, column = 0)
        self.subjectLabel.grid(row = self.row, column = 1)
        self.snippetLabel.grid(row = self.row, column = 2)
        self.dateLabel.grid(row = self.row, column = 3)
        
    def refresh(self, message):
        self.message = message  #save message
        outMessage = message    #create out messgae

        #truncate the subject and snippet if too long
        outMessage['subject'] = outMessage['subject'] if (len (outMessage['subject']) < self.maxChar//3) \
                                                else (outMessage['subject'][0:self.maxChar//3] + '...')
        outMessage['snippet'] = outMessage['snippet'] if (len (outMessage['snippet']) < self.maxChar) \
                                                else (outMessage['snippet'][0:self.maxChar] + '...')

        #set the text for the labels with the associated text
        self.fromLabel['text'] = outMessage['from name']
        self.dateLabel['text'] = outMessage['date']
        self.subjectLabel['text'] = outMessage['subject']
        self.snippetLabel['text'] = outMessage['snippet']
        

class inboxGUI(tk.Frame):
    def __init__(self, master, gmail):
        super().__init__(master)
        self.master = master
        self.gmail = gmail      #save service
        self.inbox_emails = []  #save emails
        self.emailFrame = tk.Frame(master = self) #create and displayframe to store emails
        self.emailFrame.grid(row = 0, column = 0)
        self.email_amount = 15                    #retrieve a max of 15 emails

        #get INBOX emails
        self.email_list = self.gmail.getMessages(labels = ['INBOX'], amount = self.email_amount)
        self.build_inbox_mail() #build the GUI
        
    def build_inbox_mail(self):
        for i in range(len(self.email_list)): #for all emails
            mail = inboxEmail(master = self.emailFrame, row = i) #create email
            self.inbox_emails.append(mail)                       #add to list   
        
        self.refresh_email()#get newest messages
        
        for email_obj in self.inbox_emails: #display the emails
            email_obj.build()
        
    def refresh_email(self):               
        #get inbox emails
        self.email_list = self.gmail.getMessages(labels = ['INBOX'], amount = self.email_amount)
        for i, email_obj in enumerate(self.inbox_emails): #for all emails, refresh them with new info
            email_obj.refresh(self.email_list[i])