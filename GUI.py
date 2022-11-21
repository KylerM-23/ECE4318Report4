import tkinter as tk
from email_class import email_handler
from gui_components import *


class inboxGUI(tk.Frame):
    def __init__(self, master, gmail):
        super().__init__(master)
        self.master = master
        self.gmail = gmail
        self.inbox_emails = []
        self.emailFrame = tk.Frame(master = self)
        self.emailFrame.grid(row = 0, column = 0)
        self.email_amount = 15
        self.email_list = self.gmail.getMessages(labels = ['INBOX'], amount = self.email_amount)
        self.build_inbox_mail()
        

    def build_inbox_mail(self):
        for i in range(len(self.email_list)):
            mail = inboxEmail(master = self.emailFrame, row = i)
            self.inbox_emails.append(mail)

        self.refresh_email()

        for email_obj in self.inbox_emails:
            email_obj.build()
        
    def refresh_email(self):
        self.email_list = self.gmail.getMessages(labels = ['INBOX'], amount = self.email_amount)
        for i, email_obj in enumerate(self.inbox_emails):
            email_obj.refresh(self.email_list[i])

class emailGUI(tk.Frame):
    gmail = email_handler()
    widgets = []
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.inbox_GUI_Frame = inboxGUI(self, self.gmail)
        self.send_GUI_Frame = send_GUI(self, self.gmail)
        
        self.ctrl_frame = tk.Frame(self)
        self.refresh_inbox_bttn = tk.Button(master = self.ctrl_frame, text = "Refresh", command = self.inbox_GUI_Frame.refresh_email)
        self.make_send_bttn = tk.Button(master = self.ctrl_frame, text = "Send", command = self.createSend)
        self.del_send_bttn = tk.Button(master = self.ctrl_frame, text = "Del Send", command = self.destroySend)
        self.ctrl_frame.grid(row= 0, column = 0, sticky ='WE')
        
        self.refresh_inbox_bttn.grid(row= 0, column = 0, sticky ='WE')
        self.make_send_bttn.grid(row= 0, column = 1, sticky ='WE')
        self.del_send_bttn.grid(row= 0, column = 2, sticky ='WE')
        self.inbox_GUI_Frame.grid(row = 1, column=0, sticky='NSWE', padx=(10, 10))

    def createSend(self):
        self.send_GUI_Frame.grid(row = 1,column = 2, sticky = 'N')
        self.send_GUI_Frame.build()
        
    def destroySend(self):
        self.send_GUI_Frame.grid_remove()
        self.send_GUI_Frame.hide_widgets()
        
    def destroy(self):
        for w in self.widgets:
            w.destroy()
        tk.Frame.destroy(self)
    
if __name__ == '__main__':
    window = tk.Tk()
    
    GUI = emailGUI(master = window)
    
    GUI.grid(row = 0,column = 0)
    window.mainloop()