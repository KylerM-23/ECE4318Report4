import tkinter as tk

def send():
    to_data = to_entry.get()
    subject_data = subject_entry.get()
    body_data = body.get(1.0, tk.END)

    print(to_data)
    print(subject_data)
    print(body_data)

    delete()
    
def delete():

    to_entry.delete(0, tk.END )
    subject_entry.delete(0, tk.END)
    body.delete(1.0, tk.END)
    reset()
    
def reset():
    to_entry.insert(index = 0, string = "Email To Send To")
    subject_entry.insert(index = 0, string = "Email Subject")

window = tk.Tk()

title = tk.Label(master = window, text="Email Send")
title.grid(row = 0,column = 0)

to_entry = tk.Entry(master = window)
to_entry.grid(row = 1, column=0, sticky='WE')

subject_entry = tk.Entry(master = window)
subject_entry.grid(row= 2, column = 0, sticky ='WE')

body = tk.Text(master = window)
body.grid(row = 3, column=0)

reset()

control_frame = tk.Frame(master = window)
control_frame.grid(row= 4, column = 0, sticky ='WE')

#tk.Button(text = "", command = funcName)
send_bttn = tk.Button(master = control_frame, text = "Send", command = send)
send_bttn.grid(row= 0, column = 0, sticky ='WE')

delete_bttn = tk.Button(master = control_frame, text = "Delete", command = delete)
delete_bttn.grid(row = 0, column = 1, sticky ='WE')
window.mainloop()