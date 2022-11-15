import tkinter as tk
from tkinter import *

window = tk.Tk()
window.geometry("700x500")
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=10)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=20)

frame_top = tk.Frame(window, borderwidth=2, relief="solid")
frame_middle = tk.Frame(window)
frame_left = tk.Frame(window, borderwidth=2, relief="solid")

class inbox_Gui(tk.Frame):
    def __init__(self, master):


frame_top.grid(row=0, column=1, sticky='WENS')
frame_middle.grid(row=1, column=1, sticky='WENS')
frame_left.grid(row=0, column=0, rowspan=3, sticky='WENS')

search_entry = tk.Entry(master=frame_top)
search_entry.insert(index=0, string="Search Email")
search_entry.pack(fill=BOTH, expand=True)

inbox_butt = tk.Button(master=frame_left, text="Inbox", activebackground='red', width=5)
inbox_butt.grid(row=0, column=0, pady=50)

sent_butt = tk.Button(master=frame_left, text="Sent", activebackground='red', width=5)
sent_butt.grid(row=1, column=0)

for x in range(25):
    inbox_mail = tk.Entry(master=frame_middle, width=108, font='Arial 10')
    inbox_mail.insert(index=0, string="From     Subject     Message     Time")
    inbox_mail.grid(row=x, column=0)

window.mainloop()
