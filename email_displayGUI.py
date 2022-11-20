import tkinter as tk
from tkinter import *

class inboxEmail(tk.Frame):
    def __init__(self, master, message):
        super().__init__(master)
        self.master = master
        self.fromLabel = tk.Label(text = message['from name'])
        self.subjectLabel = tk.Label(text = message['subject'])
        self.snippetLabel = tk.Label(text = message['snippet'])
        self.dateLabel = tk.Label(text = message['date'])

        self.fromLabel.grid(0, 0)
        self.subjectLabel.grid(0,1)
        self.snippetLabel.grid(0,2)
        self.dateLabel.grid(0,3)

class emailGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.frame_top = tk.Frame(self, borderwidth=2, relief="solid")
        self.frame_middle = tk.Frame(self, borderwidth=2, relief="solid")
        self.frame_left = tk.Frame(self, borderwidth=2, relief="solid")
        self.search_entry = tk.Entry(master=self.frame_top)
        self.inbox_butt = tk.Button(master=self.frame_left, text="Inbox", activebackground='red', width=5)
        self.send_butt = tk.Button(master=self.frame_left, text="Sent", activebackground='red', width=5)
        self.frame_top.grid(row=0, column=1, sticky='WENS')
        self.frame_middle.grid(row=1, column=1, sticky='WENS')
        self.frame_left.grid(row=0, column=0, rowspan=3, sticky='WENS')
        self.search_entry.insert(index=0, string="Search Email")
        self.search_entry.pack(fill=BOTH, expand=True)
        self.inbox_butt.grid(row=0, column=0, pady=50)
        self.send_butt.grid(row=1, column=0)
        self.inbox_mail()

    def inbox_mail(self):
        for x in range(25):
            mail = tk.Entry(master=self.frame_middle, width=108, font='Arial 10')
            mail.insert(index=0, string="From     Subject     Message     Time")
            mail.grid(row=x, column=0)


window = tk.Tk()
GUI = emailGUI(master=window)
GUI.grid()
window.mainloop()
