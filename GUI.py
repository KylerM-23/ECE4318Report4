import tkinter as tk
from email_class import email_handler

class emailGUI(tk.Frame):
    gmail = email_handler()
    widgets = []
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.send_GUI_Frame = send_GUI(self, self.gmail)
        self.ctrl_frame = tk.Frame(self)
        self.make_send_bttn = tk.Button(master = self.ctrl_frame, text = "Send", command = self.createSend)
        self.del_send_bttn = tk.Button(master = self.ctrl_frame, text = "Del Send", command = self.destroySend)
        self.ctrl_frame.grid(row= 0, column = 0, sticky ='WE')
        self.make_send_bttn.grid(row= 0, column = 0, sticky ='WE')
        self.del_send_bttn.grid(row= 1, column = 0, sticky ='WE')

    def createSend(self):
        self.send_GUI_Frame.grid(row = 0,column = 1)
        self.send_GUI_Frame.build()
        
    def destroySend(self):
        self.send_GUI_Frame.grid_remove()
        self.send_GUI_Frame.hide_widgets()
        
    def destroy(self):
        for w in self.widgets:
            w.destroy()
        tk.Frame.destroy(self)
        
class send_GUI(tk.Frame):
    def __init__(self, master, gmail):
        super().__init__(master)
        self.gmail = gmail
        self.title = tk.Label(master = self, text="Email Send")
        self.to_entry = tk.Entry(master = self)
        self.subject_entry = tk.Entry(master = self)
        self.body = tk.Text(master = self)
        self.control_frame = tk.Frame(master = self)
        self.delete_bttn = tk.Button(master = self.control_frame, text = "Delete", command = self.delete_txt)
        self.send_bttn = tk.Button(master = self.control_frame, text = "Send", command = self.send_email)
        
        self.widgets = [self.title, self.to_entry, self.subject_entry, self.body,
        self.control_frame, self.delete_bttn, self.send_bttn]
        
    def build(self):
        self.title.grid(row = 0,column = 0)
        self.to_entry.grid(row = 1, column=0, sticky='WE')
        self.subject_entry.grid(row= 2, column = 0, sticky ='WE')
        self.body.grid(row = 3, column=0)
        self.control_frame.grid(row= 4, column = 0, sticky ='WE')
        self.send_bttn.grid(row= 0, column = 0, sticky ='WE')
        self.delete_bttn.grid(row = 0, column = 1, sticky ='WE')
        self.reset_txt()
        
    def send_email(self):
        message = {
            'to': self.to_entry.get(),
            'subject': self.subject_entry.get(),
            'body': self.body.get(1.0, tk.END)
            }
        self.delete_txt()
        self.gmail.send_message(message)
        
    def delete_txt(self):
        self.to_entry.delete(0, tk.END )
        self.subject_entry.delete(0, tk.END)
        self.body.delete(1.0, tk.END)
        self.reset_txt()
        
    def reset_txt(self):
        self.to_entry.insert(index = 0, string = "Email To Send To")
        self.subject_entry.insert(index = 0, string = "Email Subject")
    
    def hide_widgets(self):
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