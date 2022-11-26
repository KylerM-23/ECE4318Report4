import tkinter as tk
from email_class import email_handler
from gui_components import *
from send_gui import *
from inbox_gui import inboxGUI

class emailGUI(tk.Frame):
    gmail = email_handler() #create the email service
    widgets = []
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.inbox_GUI_Frame = inboxGUI(self, self.gmail)   #create inbox GUI
        self.inbox_GUI_Frame.grid(row = 1, column=0, sticky='N', padx=(10, 10))
    
        self.send_GUI_Frame = send_GUI(self, self.gmail)    #create send GUI
        
        #Controls for the GUI
        self.ctrl_frame = tk.Frame(self)     #Container
        self.refresh_inbox_bttn = tk.Button(master = self.ctrl_frame, text = "Refresh Emails", \
            command = self.inbox_GUI_Frame.refresh_email)
        self.hide_msg_bttn = tk.Button(master = self.ctrl_frame, text = "Close Message", \
            command = self.inbox_GUI_Frame.closeMessageView)
        self.make_send_bttn = tk.Button(master = self.ctrl_frame, text = "Send", command = self.createSend)
        self.del_send_bttn = tk.Button(master = self.ctrl_frame, text = "Hide Send", command = self.hideSend)
        
        #Place controls on the screen
        self.ctrl_frame.grid(row= 0, column = 0, sticky ='WE')
        self.refresh_inbox_bttn.grid(row= 0, column = 0, sticky ='WE')
        self.hide_msg_bttn.grid(row= 0, column = 1, sticky ='WE')
        self.make_send_bttn.grid(row= 0, column = 2, sticky ='WE')
        self.del_send_bttn.grid(row= 0, column = 3, sticky ='WE')

    def createSend(self):                   #display send GUI
        self.inbox_GUI_Frame.closeMessageView()
        self.send_GUI_Frame.grid(row = 1,column = 2, sticky = 'NWE', padx=(10, 10))
        self.send_GUI_Frame.build()         #build widgets in it
        
    def hideSend(self):                     #hide the send GUI
        self.send_GUI_Frame.grid_remove() 
        self.send_GUI_Frame.hide_widgets()  #hide the widgets

    def destroy(self):
        for w in self.widgets:              #destroy all widgets
            w.destroy()
        tk.Frame.destroy(self)              #destroy the window
    
if __name__ == '__main__':
    window = tk.Tk()                        #create root window
    window.title('Email')
    window.geometry(window_geometry)
    window.state('zoomed')
    GUI = emailGUI(master = window)         #create emailGUI
    GUI.grid(row = 0,column = 0)            #place on the screen
    window.mainloop()                       #run the main loop