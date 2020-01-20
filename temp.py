from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import pyautogui
from PIL import Image
import tkinter.ttk as ttk
import os
import json
import functions_handler
import script
import ast
import copy

functionList = ['Right-Click','Left-Click','Repeat','If','Else','Try','Except', 'Double-Click','Insert Input','Key-Press', 'Exist', 'NotExist', 'Sleep']
currentScript = script.Script("Folder1",[],0)



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
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save('Screen.png')
                img = Image.open("Screen.png")
                img = img.crop((self.x0, self.y0, self.x1, self.y1))

                id=''
                for x in currentScript.functions:
                    if (x.get('id') == Lb2.curselection()[0]):
                        id = (x.get('id'))
                imgName = "Screen"+str(id)+".png"
                if not os.path.exists(currentScript.path+'ScreenShots\\'):
                    os.mkdir(currentScript.path+'ScreenShots\\')

                img = img.save(currentScript.path+'ScreenShots\\'+imgName)

                img = Photo(self.x0,self.y0,self.x1,self.y1,imgName)

                for x in currentScript.functions:
                    if(x.get('id')==Lb2.curselection()[0]):
                        x['img'] = img

                mainScreen.state('zoomed')
                self.window.destroy()
                Lb2.select_clear(0,END)
                createTree(explorerFrame)

        if (str(event.keysym) == 'Escape'):
            print("Quit window")
            mainScreen.state('zoomed')
            self.window.destroy()

        else:
            pass

    def paint(self,event):
        if(self.click==1):
            self.x1, self.y1 = event.x, event.y
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
    tmp = functionList[Lb1.curselection()[0]]
    if  (tmp =='Repeat'or tmp == 'If' or tmp =='Else' or tmp =='Try' or tmp =='Except'):
        currentScript.functions.append({'name': functionList[Lb1.curselection()[0]], 'img': '', 'id': Lb2.size()})
        currentScript.functions.append({'name':'{', 'img': '', 'id': Lb2.size()})
        currentScript.functions.append({'name':'}', 'img':'', 'id':Lb2.size()})
    else:
        currentScript.functions.append({'name':functionList[Lb1.curselection()[0]], 'img':'', 'id':Lb2.size()})
    Lb2.delete(0, 'end')
    for x in range(0, len(currentScript.functions)):
        name = currentScript.functions[x].get('name')
        Lb2.insert(x, name)
        Lb2.place(x=0, y=40)


def removeFunctions():
    index = Lb2.curselection()[0]
    currentScript.functions.pop(index)
    for i in range(index, len(currentScript.functions)):         ## changing the id to be as the index
        currentScript.functions[i]['id']=i


    Lb2.delete(0,'end')
    for x in range(0, len(currentScript.functions)):
        Lb2.insert(x, currentScript.functions[x].get('name'))
    Lb2.place(x=0, y=40)



def window2():
    window2 = ScreenShotWindow()


def SUBS(path, parent, tree, fileImg):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        tree.image = fileImg

        tree.image = fileImg

        if os.path.isdir(abspath):
            parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")
            SUBS(abspath, parent_element, tree, fileImg)
        else:
            parent_element = tree.insert(parent, 'end', text=p, open=True, image=fileImg, tag="T")


def FocusOnSelectedFunc(event):
    takeScreenShot.config(state='normal')
    try:
        index = Lb2.curselection()[0]
    except:
        return

    id = index
    photoName = ''
    functionName = ''
    for x in currentScript.functions:
        if (x.get('id') == id):
            try:
                photoName = x.get('img').img
                functionName = x.get('name')
            except:
                pass

    littlePhoto = Frame(photoViewFrame, bd=2, relief=SUNKEN, width=437, height=150, bg='white')
    littlePhoto.place(x=0,y=0)
    canvas = Canvas(littlePhoto, width=437, height=150)
    canvas.pack()
    if(photoName != ''):
        one = PhotoImage(file=currentScript.path + "ScreenShots\\" + photoName)
        photoViewFrame.one = one  # to prevent the image garbage collected.
        canvas.create_image((0, 0), image=one, anchor="nw")

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
        reTake.place(x=150, y = 295)

def disableTakeScreenShot(event):
    takeScreenShot.config(state=DISABLED)

def createTree(frame):
    tree = ttk.Treeview(frame)
    s = ttk.Style()
    s.configure('Treeview', rowheight=40)

    path = os.path.dirname(os.path.abspath(__file__))

    root = tree.insert('', 'end', text=path+'\Scripts', open=True, tag='T')
    fileImg = PhotoImage(file='').subsample(3, 3)
    tree.image = fileImg
    SUBS(path+'\\Scripts', root, tree, fileImg)
    tree.column("#0", width=frame.winfo_reqwidth(), stretch=False)

    tree.place(x=0,y=0)
    return tree

def moveUp():
    index = Lb2.curselection()[0]
    currentScript.functions[index]['id']=index-1
    currentScript.functions[index-1]['id'] = index
    a, b = index, index-1
    currentScript.functions[b], currentScript.functions[a] = currentScript.functions[a], currentScript.functions[b]
    listReload(Lb2)
    Lb2.selection_set(index-1)


def moveDown():
    index = Lb2.curselection()[0]
    currentScript.functions[index]['id']=index+1
    currentScript.functions[index+1]['id'] = index
    a, b = index+1, index
    currentScript.functions[b], currentScript.functions[a] = currentScript.functions[a], currentScript.functions[b]
    listReload(Lb2)
    Lb2.selection_set(index+1)





def listReload(list):
    list.delete(0, 'end')
    for x in range(0, len(currentScript.functions)):
        Lb2.insert(x, currentScript.functions[x].get('name'))
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
    for func in currentScript.functions:
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
        for func in currentScript.functions:
            if(func['name'] == 'Left-Click'):
                functions_handler.left_click_handle(func['img'],currentScript.path)
            elif(func['name'] == 'Exist'):
                functions_handler.exist_handle(func['img'])
            elif (func['name'] == 'NotExist'):
                functions_handler.not_exist_handle(func['img'])


def savehundle():
    functionPath = currentScript.path + "functions.json"
    if(os.path.isfile(functionPath)):
        print ("kaka")
    # file = open(functionPath,"w+")
    functionFile = ""
    for func in currentScript.functions:
        functionFile += '{'
        for i in func:
            if(i=='id'): #last atribute of func
                functionFile += '"'+i + '" : ' + '"'+str(func[i]) + '"},'
            elif(i == 'img'):
                if(func[i] != ''):
                    functionFile += '"'+i + '" : ' + json.dumps(func[i].__dict__) + ', '
                else:
                    functionFile += '"'+i + '" : "", '


            else:
                functionFile += '"'+i + '" : "' + func[i] + '", '

    temp = ast.literal_eval(functionFile)
    with open(functionPath, 'w') as outfile:
        json.dump(temp, outfile)



def saveAsHundle():
    filePath = tkinter.filedialog.asksaveasfilename(initialdir=".", title="Select file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    functionPath = filePath + ".txt"
    if (os.path.isfile(functionPath)):
        print("kaka")
    file = open(functionPath, "w+")
    functionFile = ""
    for func in currentScript.functions:
        functionFile += '{'
        for i in func:
            if (i == 'id'):  # last atribute of func
                functionFile += i + " : " + str(func[i]) + "}\n"
            elif (i == 'img'):
                if (func[i] != ''):
                    functionFile += i + " : " + json.dumps(func[i].__dict__) + ", "
                else:
                    functionFile += i + " : {}, "
            else:
                functionFile += i + " : " + func[i] + ", "
    file.write(functionFile)
    file.close()


def openButton():
    filePath = tkinter.filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("json files", "*.json"), ("all files", "*.*")))
    currentScript.functions.clear()

    with open(filePath) as json_file:
            data = json.load(json_file)


    for x in data:
        for key,value in x.items():
            if(key=='id'):
                x['id'] =int(value)
            if(key=='img' and value !=''):
                img = Photo(value.get('x0Cord'),value.get('y0Cord'), value.get('x1Cord'), value.get('y1Cord'), value.get('img'))
                x['img'] = img


    currentScript.functions =copy.deepcopy(data)

    listReload(Lb2)



def TreeviewD_Click(event):

    item_id = tree.selection()[0]
    parent_id = tree.parent(item_id)
    fullPath = ''
    while( item_id!= ''):
        temp = tree.item(item_id)['text']
        if ( fullPath==''):
            fullPath = temp
        else:
            fullPath = temp + '\\' + fullPath
        item_id = parent_id
        parent_id = tree.parent(item_id)

    if (currentScript.functions != []):
        msgbox = tkinter.messagebox.askyesnocancel('Notic!', 'Do you want to save changes you made?')
        if(msgbox==True):
            savehundle()
        elif(msgbox==None):
            return
    currentScript.functions.clear()

    with open(fullPath) as json_file:
        data = json.load(json_file)

    for x in data:
        for key, value in x.items():
            if (key == 'id'):
                x['id'] = int(value)
            if (key == 'img' and value != ''):
                img = Photo(value.get('x0Cord'), value.get('y0Cord'), value.get('x1Cord'), value.get('y1Cord'),
                            value.get('img'))
                x['img'] = img

    currentScript.functions = copy.deepcopy(data)
    listReload(Lb2)



def insertA():
  print('insert A')



def insertB():
  print('insert B')

if __name__ =='__main__':

    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("MyApp")
    # kaka = script.Script.getFunctions(currentScript.path)

    toolbarFrame = Frame(mainScreen, bd=3, width=mainScreen.winfo_screenwidth(), height=50)
    toolbarFrame.place(x=0, y=50)

    openButton = Button(toolbarFrame, text="Open" , command = openButton)
    openButton.place(x=0,y=0)

    saveButton = Button(toolbarFrame, text="Save",command = savehundle)
    saveButton.place(x=70, y=0)

    saveAsButton = Button(toolbarFrame, text="Save As", command=saveAsHundle)
    saveAsButton.place(x=140, y=0)

    runButton = Button(toolbarFrame, text="Run", command=runHendle)
    runButton.place(x=230, y=0)

    stopButton = Button(toolbarFrame, text="Stop")
    stopButton.place(x=290, y=0)

    close = Button(mainScreen, text="Close", command=mainScreen.destroy)
    close.place(x=0,y=0)

    minimize = Button(mainScreen, text="Minimize", command=mainScreen.iconify)
    minimize.place(x=60, y=0)

    addFunc = Button(mainScreen, text="Add Functions", command=addFunction)
    addFunc.place(x=1600, y=100)



    explorerFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=500, height=430, bg='white')
    explorerFrame.place(x=10, y=150)


    mainFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=900, height=800, bg='white')
    mainFrame.place(x=535, y=150)



    moveDownButton  = Button(mainFrame, text="Move down", command=moveDown)
    moveDownButton.place(x=20,y=0)

    moveUpButton = Button(mainFrame, text="Move up", command=moveUp)
    moveUpButton.place(x=140, y=0)

    removeFunc = Button(mainFrame, text="Remove Function", command=removeFunctions)
    removeFunc.place(x=240, y=0)

    insertB = Button(mainFrame, text="Insert Below", command=insertB)
    insertB.place(x=410, y=0)

    insertA = Button(mainFrame, text="Insert Above", command=insertA)
    insertA.place(x=550, y=0)

    takeScreenShot = Button(mainFrame, text="Take Screen Shot", command=window2, state=DISABLED)
    takeScreenShot.place(x=690, y=0)


    funFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=450, height=400, bg='white')
    funFrame.place(x=1455, y=150)

    photoViewFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=450, height=350, bg='white')
    photoViewFrame.place(x=1455, y=600)

    Lb1 = Listbox(funFrame, width=450, height=2400 )
    for x in range(0, len(functionList)):
        Lb1.insert(x, functionList[x])


    Lb1.place(x=0,y=0)


    Lb2 = Listbox(mainFrame, width=99, height=300)
    for x in range(0, len(currentScript.functions)):
        Lb2.insert(x, currentScript.functions[x])

    Lb2.place(x=0, y=40)

    Lb2.bind("<<ListboxSelect>>", func=FocusOnSelectedFunc)
    Lb2.bind("<FocusOut>", func=disableTakeScreenShot)


    tree = createTree(explorerFrame)
    tree.bind("<Double-1>", TreeviewD_Click)


mainScreen.mainloop()