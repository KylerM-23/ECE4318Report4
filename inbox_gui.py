import tkinter as tk
from view_message_gui import *

class inboxEmail(tk.Frame): #individual emails
    def __init__(self, master, rootGUI, row = 0, w = 150):
        super().__init__(master)
        self.master = master
        self.maxChar = w//2                                 #set the max characters
        self.row = row                                      #the row the email belongs in
        self.message = None
        self.grid(row = row, column=0, sticky ='N')
        self.rootGUI = rootGUI                              #base frame

        #create the labels for the information
        self.fromLabel = tk.Label(master = self, width=int(w*.15), anchor = 'w',justify = 'left')
        self.dateLabel = tk.Label(master = self, width=int(w*.05), anchor = 'e', justify = 'left')
        self.subjectLabel = tk.Label(master = self, width=int(w*.2), anchor = 'w', justify = 'left')
        self.snippetLabel = tk.Label(master = self, width=int(w*.2), justify = 'left', anchor = 'w', wraplength=int(w*1))

        self.viewBtn = tk.Button(master=self, text = 'View', command=self.viewMsg)
        self.delBtn = tk.Button(master=self, text = 'Delete', command=self.deleteMsg)

    def build(self): #place elements on the screen
        self.viewBtn.grid(row = 0, column = 0)
        self.fromLabel.grid(row = 0, column = 1)
        self.subjectLabel.grid(row = 0, column = 2)
        self.snippetLabel.grid(row = 0, column = 3)
        self.dateLabel.grid(row = 0, column = 4)
        self.delBtn.grid(row = 0, column= 5)

        
    def refresh(self, message):
        self.message = message  #save message

        #truncate the subject and snippet if too long
        subj = message['subject'] if (len (message['subject']) < self.maxChar//3) \
                                  else (message['subject'][0:self.maxChar//3] + '...')
        snip = message['snippet'] if (len (message['snippet']) < self.maxChar) \
                                  else (message['snippet'][0:self.maxChar] + '...')

        #set the text for the labels with the associated text
        self.fromLabel['text'] = message['from name']
        self.dateLabel['text'] = message['date']
        self.subjectLabel['text'] = subj
        self.snippetLabel['text'] = snip

    def viewMsg(self):
        self.rootGUI.updateMessageView(self.message)    #update GUI
    
    def deleteMsg(self):
        self.rootGUI.closeMessageView()                 #close open msg
        self.rootGUI.delMessage(self.message)           #delete message

class inboxGUI(tk.Frame):
    def __init__(self, master, gmail, width = window_width//2 +100):
        super().__init__(master)
        self.master = master
        self.gmail = gmail                              #save service
        self.inbox_emails = []                          #save emails
        self.emailFrame = ScrollFrame(self, w = width)  #create and displayframe to store emails
        self.emailFrame.grid(row = 0, column = 0, sticky='NSEW')
        self.view_msg_GUI_Frame = view_message_GUI(self, self.gmail)
        self.email_amount = 10                          #set max num of emails
        self.messageOpen = False                        #status of message window
        self.email_list = self.gmail.getMessages(labels = ['INBOX'], \
            amount = self.email_amount)
        self.build_inbox_mail()                         #build the GUI
        
    def build_inbox_mail(self):
        for i in range(len(self.email_list)):           #create emails and add to list
            mail = inboxEmail(master = self.emailFrame.viewPort, rootGUI=self, row = i)
            self.inbox_emails.append(mail)             
        self.refresh_email()                            #get newest messages
        for email_obj in self.inbox_emails:             #display the emails
            email_obj.build()
        
    def refresh_email(self):                            #get inbox emails
        self.email_list = self.gmail.getMessages(labels = ['INBOX'], amount = self.email_amount)
        for i, email_obj in enumerate(self.inbox_emails):#refresh emails with new info
            email_obj.refresh(self.email_list[i])
        self.emailFrame.resetView()                     #reset inbox view to top

    def updateMessageView(self, msg):
        self.master.hideSend()                          #hide send window
        self.messageOpen = True                         #change status
        self.gmail.mark_as_read(msg)
        self.view_msg_GUI_Frame.grid(row = 0, column=1, sticky='N', padx=(10, 10))
        self.view_msg_GUI_Frame.updateDisplay(msg)      #place and update GUI

    def delMessage(self, msg):
        self.gmail.delete_message(msg)
        self.refresh_email()
        
    def closeMessageView(self): 
        if self.messageOpen:                            #if a message is open                        
            self.view_msg_GUI_Frame.grid_remove()       #remove GUI from the grid
            self.view_msg_GUI_Frame.hide()              #hide components
            self.messageOpen = False                    #change status
        