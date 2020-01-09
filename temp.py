from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import pyautogui
from PIL import Image
import tkinter.ttk as ttk
import os
import json
import random
import uuid
import functions_handler


functionList = ['Right-Click','Left-Click', 'Insert Input','Key-Press', 'Exist', 'NotExist', 'Sleep']
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

        tkinter.messagebox.showinfo("Notic!", "Press ENTER To Take ScreenShot\nPress ESC To Quit")
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
                Lb2.select_clear(0,END)


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
        if (str(event.type) == 'ButtonPress'):
            self.click=1
            self.x0, self.y0 = event.x, event.y

        else:

            self.click=2
            self.x1, self.y1 = event.x, event.y

def addFunction():
    selectedFunc.append({'name':functionList[Lb1.curselection()[0]], 'img':'', 'id':Lb2.size()})
    Lb2.delete(0, 'end')

    for x in range(0, len(selectedFunc)):
        Lb2.insert(x, selectedFunc[x].get('name'))
        Lb2.place(x=0, y=40)


def removeFunctions():
    index = Lb2.curselection()[0]
    selectedFunc.pop(index)
    for i in range(index, len(selectedFunc)):         ## changing the id to be as the index
        selectedFunc[i]['id']=i


    Lb2.delete(0,'end')
    for x in range(0, len(selectedFunc)):
        Lb2.insert(x, selectedFunc[x].get('name'))
    Lb2.place(x=0, y=40)



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

    littlePhoto = Frame(photoViewFrame, bd=2, relief=SUNKEN, width=437, height=150, bg='white')
    littlePhoto.place(x=0,y=0)
    canvas = Canvas(littlePhoto, width=437, height=150)
    canvas.pack()
    print(photoName)
    one = PhotoImage(file=photoName)


    photoViewFrame.one = one  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=one, anchor = "nw" )



    functionNameLabel =  Label(photoViewFrame, text='Function Name : ')
    fileNameLabel = Label(photoViewFrame, text='File Name : ')
    functionNameLabel.place(x=50, y=200)
    fileNameLabel.place(x=50, y=250)


    functionNameFrame = Frame(photoViewFrame, width=200, height=30, bg='white')
    functionNameFrame.place(x=200, y=200)
    labelInfunctionNameFrame = Label(functionNameFrame, text=functionName)
    labelInfunctionNameFrame.place(x=0,y=0)

    fileNameFrame = Frame(photoViewFrame, width=200, height=30, bg='white')
    fileNameFrame.place(x=200, y=250)
    labelInfunctionNameFrame = Label(fileNameFrame, text=photoName)
    labelInfunctionNameFrame.place(x=0, y=0)

    if(photoName!=''):
        reTake = Button(photoViewFrame, text='Take New ScreenShot' , command=window2)
        reTake.place(x=150, y = 330)






def disableTakeScreenShot(event):
    takeScreenShot.config(state=DISABLED)

def createTree(frame):
    tree = ttk.Treeview(frame)

    s = ttk.Style()
    s.configure('Treeview', rowheight=40)

    # tree.heading("#0", text="Explorer")
    root = tree.insert('', 'end', text=os.path.dirname(os.path.abspath(__file__)), open=True, tag='T')
    fileImg = PhotoImage(file='').subsample(3, 3)
    tree.image = fileImg
    SUBS(os.path.dirname(os.path.abspath(__file__)), root, tree, fileImg)
    tree.column("#0", width=frame.winfo_reqwidth(), stretch=False)

    tree.pack(fill=X)


def runHendle(event):
    print('run pressed')


def moveUp():
    index = Lb2.curselection()[0]
    selectedFunc[index]['id']=index-1
    selectedFunc[index-1]['id'] = index
    a, b = index, index-1
    selectedFunc[b], selectedFunc[a] = selectedFunc[a], selectedFunc[b]
    listReload(Lb2)
    Lb2.selection_set(index-1)


def moveDown():
    index = Lb2.curselection()[0]
    selectedFunc[index]['id']=index+1
    selectedFunc[index+1]['id'] = index
    a, b = index+1, index
    selectedFunc[b], selectedFunc[a] = selectedFunc[a], selectedFunc[b]
    listReload(Lb2)
    print(selectedFunc)
    Lb2.selection_set(index+1)





def listReload(list):
    list.delete(0, 'end')
    for x in range(0, len(selectedFunc)):
        Lb2.insert(x, selectedFunc[x].get('name'))
        Lb2.place(x=0, y=40)

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def checkImageInFunc():
    funcWithoutImage = ""
    index = 1
    for func in selectedFunc:
        if(func['img'] == ''):
            funcWithoutImage += ("The {} in line {} doesn't have screenshot\n".format(func['name'],index))
        index += 1
    return funcWithoutImage

def runHendle():
    funcWithoutImage = checkImageInFunc()
    if(funcWithoutImage != ''):
        popupmsg(funcWithoutImage)
    else:
        mainScreen.iconify()
        for func in selectedFunc:
            if(func['name'] == 'Click'):
                functions_handler.click_handle(func['img'])
            elif(func['name'] == 'Exist'):
                functions_handler.exist_handle(func['img'])
            elif (func['name'] == 'NotExist'):
                functions_handler.not_exist_handle(func['img'])



if __name__ =='__main__':

    mainScreen = Tk()
    mainScreen.attributes('-fullscreen', True)
    mainScreen.title("MyApp")


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



    explorerFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=500, height=900, bg='white')
    explorerFrame.place(x=10, y=150)


    mainFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=900, height=900, bg='white')
    mainFrame.place(x=535, y=150)



    moveDownButton  = Button(mainFrame, text="Move down", command=moveDown)
    moveDownButton.place(x=170,y=0)

    moveUpButton = Button(mainFrame, text="Move up", command=moveUp)
    moveUpButton.place(x=300, y=0)

    removeFunc = Button(mainFrame, text="Remove Function", command=removeFunctions)
    removeFunc.place(x=420, y=0)

    takeScreenShot = Button(mainFrame, text="Take Screen Shot", command=window2, state=DISABLED)
    takeScreenShot.place(x=600, y=0)


    funFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=450, height=400, bg='white')
    funFrame.place(x=1455, y=150)

    photoViewFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=450, height=400, bg='white')
    photoViewFrame.place(x=1455, y=600)

    Lb1 = Listbox(funFrame, width=450, height=2400 )
    for x in range(0, len(functionList)):
        Lb1.insert(x, functionList[x])


    Lb1.place(x=0,y=0)


    Lb2 = Listbox(mainFrame, width=99, height=300)
    for x in range(0, len(selectedFunc)):
        Lb2.insert(x, selectedFunc[x])

        Lb2.place(x=0, y=40)

    Lb2.bind("<FocusIn>", func=FocusOnSelectedFunc)
    Lb2.bind("<<ListboxSelect>>", func=FocusOnSelectedFunc)
    Lb2.bind("<FocusOut>", func=disableTakeScreenShot)

    createTree(explorerFrame)



mainScreen.mainloop()