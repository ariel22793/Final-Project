import tkinter as tk
import easygui


def click(event):
    easygui.msgbox("You clicked on "+event.widget.cget("text"), title="")

root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

def donothing():
   x = 0

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

b1 = tk.Button(root, text="Add Function")
b1.place(x=10, y=20)
b1.bind("<Button-1>", click)

b2 = tk.Button(root, text="Start")
b2.bind("<Button-1>", click)
b2.place(x=600, y=20)

b3 = tk.Button(root, text="Stop")
b3.bind("<Button-1>", click)
b3.place(x=640, y=20)

root.mainloop()