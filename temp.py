
from tkinter import *
import pyautogui
from PIL import Image
import tkinter.ttk as ttk
import os
import random
import uuid
functionList = ['Click', 'Exist', 'NotExist']
selectedFunc = []



class Photo():
    def __init__(self,x0,y0,x1,y1,imgPath):
        self.x0Cord = x0
        self.x1Cord = x1
        self.y0Cord = y0
        self.y1Cord = y1
        self.img = imgPath


class ScreenShotWindow():
    def __init__(self):
        mainScreen.iconify()
        window2 = Tk()
        window2.title("window2")
        window2.attributes('-fullscreen', True)
        window2.attributes('-alpha', 0.3)

        self.width = window2.winfo_screenwidth()
        self.heigth = window2.winfo_screenheight()

        self.x0, self.y0, self.x1, self.y1 =-1,-1,-1,-1
        self.canvas = Canvas(window2,width = window2.winfo_screenwidth(), height = window2.winfo_screenheight(), highlightthickness=0)
        self.canvas.pack()
        self.click=0
        self.window = window2
        window2.bind('<Button-1>', self.getMaousePosition)
        window2.bind('<Motion>', self.paint)
        window2.bind('<ButtonRelease-1>', self.getMaousePosition)
        window2.bind('<Key>', self.keyPress)

    def keyPress(self, event):
        if(str(event.keysym) =='Return'):
            if(self.x0!=self.x1 and self.y0!=self.y1):
                print("taking screenshot")
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save('Screen.png')
                img = Image.open("Screen.png")
                img = img.crop((self.x0, self.y0, self.x1, self.y1))
                ran = random.randrange(1000)
                img = img.save("Screen"+str(ran)+".png")

                img = Photo(self.x0,self.y0,self.x1,self.y1,"Screen"+str(ran)+".png")

                for x in selectedFunc:
                    if(x.get('name')==Lb2.get(Lb2.curselection())):
                        x['img'] = img

                print(selectedFunc)
                mainScreen.state('zoomed')
                self.window.destroy()
        if (str(event.keysym) == 'Escape'):
            print("Quit window")
            mainScreen.state('zoomed')
            self.window.destroy()

        else:
            pass

    def paint(self,event):
        if(self.click==1):
            self.x1, self.y1 = event.x, event.y
            print('{}, {}'.format(self.x1, self.y1))
            self.canvas.delete('all')
            self.canvas.create_rectangle(self.x0,self.y0, self.x1,self.y1,outline='black') #inner

            self.canvas.create_rectangle(0,0, self.x0,self.heigth, fill='red' ,outline='red') #outter
            self.canvas.create_rectangle(self.x0, 0, self.x1, self.y0, fill='red' ,outline='red' ) #outter
            self.canvas.create_rectangle(self.x0, self.y1, self.width, self.heigth, fill='red' ,outline='red') #outter
            self.canvas.create_rectangle(self.x1, 0, self.width,self.heigth, fill='red' ,outline='red') #outter




    def getMaousePosition(self, event):
        print(event.type)
        if (str(event.type) == 'ButtonPress'):
            self.click=1
            self.x0, self.y0 = event.x, event.y

        else:

            self.click=2
            self.x1, self.y1 = event.x, event.y

def addFunction():
    selectedFunc.append({'name':functionList[Lb1.curselection()[0]], 'img':'', 'id':uuid.uuid1()})
    Lb2.delete(0, 'end')

    for x in range(0, len(selectedFunc)):
        Lb2.insert(x, selectedFunc[x].get('name'))
    Lb2.place(x=0, y=0)

def removeFunctions():
    print(Lb2.curselection()[0])
    value = Lb2.curselection()[0]
    selectedFunc.pop(value)

    Lb2.delete(0, 'end')

    for x in range(0, len(selectedFunc)):
        Lb2.insert(x, selectedFunc[x].get('name'))
    Lb2.place(x=0, y=0)

    print(Lb2)
    print(selectedFunc)
def window2():
    window2 = ScreenShotWindow()


def SUBS(path, parent, tree, fileImg):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        tree.image = fileImg

        tree.image = fileImg

        if os.path.isdir(abspath):
            parent_element = tree.insert(parent, 'end', text=p, open=False, tag="T")
            SUBS(abspath, parent_element, tree, fileImg)
        else:
            parent_element = tree.insert(parent, 'end', text=p, open=False, image=fileImg, tag="T")




def FocusOnSelectedFunc(event):


    takeScreenShot.config(state='normal')
    photoViewLabel = Label(mainScreen, text='Shot View')
    photoViewLabel.place(x=1620, y=560)
    widget = event.widget
    selection = widget.curselection()
    nameOfFun = Lb2.get(selection)

    photoName = ''
    functionName = ''
    for x in selectedFunc:
        if (x.get('name') == nameOfFun):
            try:
                photoName = x.get('img').img
                functionName = x.get('name')
            except:
                pass

    littlePhoto = Frame(photoViewFrame, bd=2, relief=SUNKEN, width=150, height=150, bg='white')
    littlePhoto.place(x=150,y=0)
    canvas = Canvas(littlePhoto, width=150, height=150)
    canvas.pack()
    print(photoName)
    one = PhotoImage(file=photoName)
    photoViewFrame.one = one  # to prevent the image garbage collected.
    canvas.create_image((200, 0), image=one )

    functionNameLabel =  Label(photoViewFrame, text='Function Name : ' +functionName )
    fileNameLabel = Label(photoViewFrame, text='File Name : ' + photoName)

    functionNameLabel.place(x=50,y=200)
    fileNameLabel.place(x=50,y=230)

def disableTakeScreenShot(event):
    takeScreenShot.config(state=DISABLED)

def createTree(frame):
    tree = ttk.Treeview(frame)

    s = ttk.Style()
    s.configure('Treeview', rowheight=40)

    # tree.heading("#0", text="Explorer")
    root = tree.insert('', 'end', text=os.path.dirname(os.path.abspath(__file__)), open=True, tag='T')
    fileImg = PhotoImage(file='img\\file.png').subsample(3, 3)
    tree.image = fileImg
    SUBS(os.path.dirname(os.path.abspath(__file__)), root, tree, fileImg)
    tree.column("#0", width=frame.winfo_reqwidth(), stretch=False)

    tree.pack(fill=X)


def runHendle(event):
    print('run pressed')



if __name__ =='__main__':

    mainScreen = Tk()
    mainScreen.attributes('-fullscreen', True)
    mainScreen.title("MyApp")
    takeScreenShot = Button(mainScreen, text="Take Screen Shot", command=window2, state=DISABLED)
    takeScreenShot.place(x=1000,y=100)

    toolbarFrame = Frame(mainScreen, bd=3, width=mainScreen.winfo_screenwidth(), height=50)
    toolbarFrame.place(x=0, y=50)

    openButton = Button(toolbarFrame, text="Open")
    openButton.place(x=0,y=0)

    openButton = Button(toolbarFrame, text="Save")
    openButton.place(x=80, y=0)

    runButton = Button(toolbarFrame, text="Run", command=runHendle)
    runButton.place(x=160, y=0)

    stopButton = Button(toolbarFrame, text="Stop")
    stopButton.place(x=230, y=0)

    close = Button(mainScreen, text="Close", command=mainScreen.destroy)
    close.place(x=0,y=0)

    minimize = Button(mainScreen, text="Minimize", command=mainScreen.iconify)
    minimize.place(x=60, y=0)

    addFunc = Button(mainScreen, text="Add Functions", command=addFunction)
    addFunc.place(x=1600, y=100)
    removeFunc = Button(mainScreen, text="Remove Function", command=removeFunctions)
    removeFunc.place(x=800,y=100)

    explorerFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=500, height=900, bg='white')
    explorerFrame.place(x=10, y=150)

    mainFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=900, height=900, bg='white')
    mainFrame.place(x=535, y=150)

    funFrame = Frame(mainScreen, bd=2, relief=SUNKEN, width=450, height=400, bg='white')
    funFrame.place(x=1455, y=150)

    photoViewFrame = Frame(mainScreen, bd=2, relief=SUNKEN, width=450, height=400, bg='white')
    photoViewFrame.place(x=1455, y=600)

    Lb1 = Listbox(funFrame, width=450, height=400 )
    for x in range(0, len(functionList)):
        Lb1.insert(x, functionList[x])


    Lb1.place(x=0,y=0)

    Lb2 = Listbox(mainFrame, width=450, height=400)
    for x in range(0, len(selectedFunc)):
        Lb2.insert(x, selectedFunc[x])

    Lb2.place(x=0, y=0)
    Lb2.bind("<FocusIn>", func=FocusOnSelectedFunc)
    Lb2.bind("<<ListboxSelect>>", func=FocusOnSelectedFunc)
    Lb2.bind("<FocusOut>", func=disableTakeScreenShot)

    createTree(explorerFrame)



mainScreen.mainloop()
