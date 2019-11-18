import tkinter as tk
import easygui


def click(event):
    easygui.msgbox("You clicked on "+event.widget.cget("text"), title="")


root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

b1 = tk.Button(root, text="Add Function")
b1.place(x=10, y=5)
b1.bind("<Button-1>", click)

b2 = tk.Button(root, text="Start")
b2.bind("<Button-1>", click)
b2.place(x=600, y=5)

b3 = tk.Button(root, text="Stop")
b3.bind("<Button-1>", click)
b3.place(x=640, y=5)

root.mainloop()