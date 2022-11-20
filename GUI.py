import tkinter as tk
from email_class import email_handler
from gui_components import *

'''
{
    from: 'email', 
    subj:   ''
    body: ''
    time: DateTime obj
}
'''
class inboxGUI(tk.Frame):
    def __init__(self, master, gmail):
        super().__init__(master)
        self.master = master
        self.gmail = gmail
        self.inbox_emails = []
        self.emailFrame = tk.Frame(master = self)
        self.emailFrame.grid(row = 0, column = 0)
        self.inbox_mail()
        

    def inbox_mail(self):
        email_amount = 25
        email_list = self.gmail.getMessages(labels = ['INBOX'], amount = email_amount)
        for i, email in enumerate(email_list):
            #print(email)
            mail = inboxEmail(master = self.emailFrame, message = email)
            self.inbox_emails.append(mail)
            mail.grid(row=i, column=0)

class emailGUI(tk.Frame):
    gmail = email_handler()
    widgets = []
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.inbox_GUI_Frame = inboxGUI(self, self.gmail)
        self.send_GUI_Frame = send_GUI(self, self.gmail)
        
        self.ctrl_frame = tk.Frame(self)
        self.make_send_bttn = tk.Button(master = self.ctrl_frame, text = "Send", command = self.createSend)
        self.del_send_bttn = tk.Button(master = self.ctrl_frame, text = "Del Send", command = self.destroySend)
        self.ctrl_frame.grid(row= 0, column = 0, sticky ='WE')
        
        self.make_send_bttn.grid(row= 0, column = 0, sticky ='WE')
        self.del_send_bttn.grid(row= 0, column = 1, sticky ='WE')
        self.inbox_GUI_Frame.grid(row = 1, column=0, sticky='WE')

    def createSend(self):
        self.send_GUI_Frame.grid(row = 1,column = 1)
        self.send_GUI_Frame.build()
        
    def destroySend(self):
        self.send_GUI_Frame.grid_remove()
        self.send_GUI_Frame.hide_widgets()
        
    def destroy(self):
        for w in self.widgets:
            w.destroy()
        tk.Frame.destroy(self)

class send_GUI(tk.Frame):
    def __init__(self, master, gmail, width =  100):
        super().__init__(master, width = width)
        self.gmail = gmail
        self.title = tk.Label(master = self, text="Email Send")
        
        self.to_entry = EntryField(master = self, field = 'To:', width = width)
        self.subject_entry = EntryField(master = self, field = 'Subject:', width = width)
        self.cc_entry = EntryField(master = self, field = 'CC:', width = width)
        self.bcc_entry = EntryField(master = self, field = 'BCC:', width = width)
        
        self.body = tk.Text(master = self)
        self.control_frame = tk.Frame(master = self)
        self.delete_bttn = tk.Button(master = self.control_frame, text = "Delete", command = self.delete_txt)
        self.send_bttn = tk.Button(master = self.control_frame, text = "Send", command = self.send_email)
        
        self.entryfields = [self.to_entry, self.subject_entry,self.cc_entry, self.bcc_entry]
        self.widgets = [self.title, self.body, self.control_frame, self.delete_bttn, self.send_bttn]
        
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
        self.delete_txt()
        
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
    
if __name__ == '__main__':
    window = tk.Tk()
    
    GUI = emailGUI(master = window)
    
    GUI.grid(row = 0,column = 0)
    window.mainloop()