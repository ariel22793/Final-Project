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

class Sleep():
    def __init__(self, time):
        self.time = time

    def getDict(self):
        return {'time':str(self.time)}

    @classmethod
    def getExtra(cls, extra):
        return Sleep(extra['time'])


class Repeat():
    def __init__(self,time, functions):
        self.time = time
        self.functions = functions

    def getDict(self):
        block = []
        if(len(self.functions) >0):
            for x in self.functions:
                if (x.img != ''):
                    imgdict = x.img.getDict()
                else:
                    imgdict = ''
                if(x.extra != ''):
                    block.append({'name':x.name, 'img':imgdict, 'id':str(x.id),'frame':'','father':str(x.father), 'extra':x.extra.getDict()})
                else:
                    block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '', 'father': str(x.father),
                                  'extra':''})
        return {'time':str(self.time),'functions':block}

    @classmethod
    def getExtra(cls, extra):
        functions = []
        if(len(extra['functions'])>0):
            for x in extra['functions']:
                functions.append(Function.getFunction(x))
        if(extra['time'] == '?'):
            return Repeat(extra['time'],functions)
        else:
            return Repeat(int(extra['time']),functions)


class Photo():
    def __init__(self,x0,y0,x1,y1,imgPath):
        self.x0Cord = x0
        self.x1Cord = x1
        self.y0Cord = y0
        self.y1Cord = y1
        self.img = imgPath
    def getDict(self):
         return({'x0Cord':str(self.x0Cord), 'x1Cord':str(self.x1Cord), 'y0Cord':str(self.y0Cord), 'y1Cord':str(self.y1Cord), 'img':self.img})

    @classmethod
    def getImg(cls, img):
        return Photo(int(img['x0Cord']),int(img['y0Cord']),int(img['x1Cord']),int(img['y1Cord']),img['img'])


class Function():
    def __init__(self, name, img, id, frame, father,extra):
        self.name = name
        self.img = img
        self.id = id
        self.frame = frame
        self.father = father
        self.extra = extra

    @classmethod
    def getFunction(cls, func):
        extra = ''
        img = ''
        frame = ''

        if(func['img'] != ''):
            img = Photo.getImg(func['img'])
        if (func['extra'] != ''):
            if(func['name'] == 'Repeat'):
                extra = Repeat.getExtra(func['extra'])
            if (func['name'] == 'Sleep'):
                extra = Sleep.getExtra(func['extra'])
        if (func['name'] != '{' and func['name'] != '}'):
            frame = getFrame(func['name'])
            if (func['name'] == 'Repeat'):
                getInputBox(extra, frame.children.get('label'), frame.children.get('input'),
                            changeRepeatTime)
            elif(func['name'] == 'Sleep'):
                getInputBox(extra, frame.children.get('label'), frame.children.get('input'),
                            changeSleepTime)
        return Function(func['name'],img,int(func['id']),frame,func['father'],extra)

    def printFunction(self):
        temp = 'name:' + str(self.name) + ', id:' + str(self.id) + ', img:' + str(self.img) + ', father:' + str(self.father)
        return(temp)

    def hasFather(self):           ## check if the function has father
        if self.father != (self.id, self.name):
            return True
        else:
            return False
class LineFather():
    def __init__(self, fromIndex, toIndex, fatherName):
        self.fromIndex = fromIndex
        self.toIndex = toIndex
        self.fatherName = fatherName


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

        self.x0, self.y0, self.x1, self.y1 = -1, -1, -1, -1
        self.canvas = Canvas(window2, width=window2.winfo_screenwidth(), height=window2.winfo_screenheight(),
                             highlightthickness=0)
        self.canvas.pack()
        self.click = 0
        self.window = window2
        window2.bind('<Button-1>', self.getMaousePosition)
        window2.bind('<Motion>', self.paint)
        window2.bind('<ButtonRelease-1>', self.getMaousePosition)
        window2.bind('<Key>', self.keyPress)

    def keyPress(self, event):
        if str(event.keysym) == 'Return':
            if self.x0 != self.x1 and self.y0 != self.y1:
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save('Screen.png')
                img = Image.open("Screen.png")
                img = img.crop((self.x0, self.y0, self.x1, self.y1))

                id = ''
                for x in currentScript.functions:
                    if x.id == Lb2.curselection()[0]:
                        id = x.id
                imgName = "Screen" + str(id) + ".png"
                if not os.path.exists(currentScript.path + 'ScreenShots\\'):
                    os.mkdir(currentScript.path + 'ScreenShots\\')

                img = img.save(currentScript.path + 'ScreenShots\\' + imgName)

                img = Photo(self.x0, self.y0, self.x1, self.y1, imgName)

                mainScreen.state('zoomed')
                self.window.destroy()

                for func in range(len(currentScript.functions)):
                    if currentScript.functions[func].id == Lb2.curselection()[0]:
                        currentScript.functions[func].img = img
                        if currentScript.functions[func].father[1] == 'Repeat':
                            currentScript.functions[currentScript.functions[func].father[0]].extra.functions[
                                func - currentScript.functions[func].father[0] - 2].img = img
                Lb2.select_clear(0, END)
                createTree(explorerFrame)

        if str(event.keysym) == 'Escape':
            print("Quit window")
            mainScreen.state('zoomed')
            self.window.destroy()

        else:
            pass

    def paint(self, event):
        if self.click == 1:
            self.x1, self.y1 = event.x, event.y
            self.canvas.delete('all')
            self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline='black')  # inner

            self.canvas.create_rectangle(0, 0, self.x0, self.heigth, fill='red', outline='red')  # outter
            self.canvas.create_rectangle(self.x0, 0, self.x1, self.y0, fill='red', outline='red')  # outter
            self.canvas.create_rectangle(self.x0, self.y1, self.width, self.heigth, fill='red', outline='red')  # outter
            self.canvas.create_rectangle(self.x1, 0, self.width, self.heigth, fill='red', outline='red')  # outter

    def getMaousePosition(self, event):
        if (str(event.type) == 'ButtonPress'):
            self.click = 1
            self.x0, self.y0 = event.x, event.y
        else:
            self.click = 2
            self.x1, self.y1 = event.x, event.y


def changeSleepTime(sv):
    index = Lb2.curselection()[0]
    currentScript.functions[index].extra.time = int(sv.get())
    currentScript.functions[index].name = "Sleep"
    Lb2.delete(index)
    Lb2.insert(index, currentScript.functions[index].name + '({})'.format(currentScript.functions[index].extra.time))
    Lb2.selection_set(index)
    return True


def changeRepeatTime(sv):
    index = Lb2.curselection()[0]
    currentScript.functions[index].extra.time = int(sv.get())
    currentScript.functions[index].name = "Repeat"
    Lb2.delete(index)
    Lb2.insert(index, currentScript.functions[index].name + '({})'.format(currentScript.functions[index].extra.time))
    Lb2.selection_set(index)
    return True


def updateCurrentScript():
    fromIndex = 0
    toIndex = 0
    for i in range(len(currentScript.functions)):
        if(currentScript.functions[i].name == '}'):
            fromIndex = currentScript.linesFather[i].fromIndex
            toIndex = i
        elif (currentScript.functions[i].name == 'Repeat'):
            fromIndex = i
            toIndex = i + len(currentScript.functions[i].extra.functions) + 2
        if currentScript.functions[i].father != '' and currentScript.functions[i].father[1] == 'Repeat':
            currentScript.functions[i].id = i
            currentScript.linesFather[i].fromIndex = fromIndex
            currentScript.linesFather[i].toIndex = toIndex
        else:
            currentScript.functions[i].id = i
            currentScript.linesFather[i].fromIndex = i
            currentScript.linesFather[i].toIndex = i

    for i in currentScript.functions:
        if i.name != '':
            if i.id == 0:
                # print('####################')
            # print('{}:{}'.format(i.id, i.name))
                pass
            if i.id == len(currentScript.functions) - 1:
                pass
                # print('####################')


def getInputBox(function, frameLabel, frameInput, eventFunction):
    count = 0
    for attr in dir(function):
        if not callable(getattr(function, attr)) and not attr.startswith("__") and attr != 'functions':
            count += 1

            y = 50 + count * 50
            frameLabel.place(x=50, y=y)
            label = Label(frameLabel, text=attr)
            label.place(x=0, y=0)

            frameInput.place(x=150, y=y)

            sv = StringVar(value=function.time)
            entry = Entry(frameInput, textvariable=sv)
            entry.bind('<Return>', (lambda _: eventFunction(entry)))
            entry.pack()
            entry.place(x=0, y=0)


def getFrame(functionName):
    frame1 = Frame(bd=3, relief=SUNKEN, width=450, height=350, bg='white')
    functionNameLabel = Label(frame1, text='Function Name : {}'.format(functionName))
    if functionName == 'Sleep' or functionName == 'Repeat':
        functionNameLabel.place(x=50, y=50)
        Frame(frame1, width=200, height=30, bg='white', name='label')
        Frame(frame1, width=200, height=30, bg='white', name='input')
    else:
        fileNameLabel = Label(frame1, text='File Name : ',name = 'fileName')
        functionNameLabel.place(x=50, y=200)
        fileNameLabel.place(x=50, y=250)
        littlePhoto = Frame(frame1, bd=2, relief=SUNKEN, width=437, height=150, bg='white', name='canvasFrame')
        littlePhoto.place(x=0, y=0)
    return frame1


def updateLb2():
    Lb2.delete(0, 'end')
    for x in range(0, len(currentScript.functions)):
        name = currentScript.functions[x].name
        if name == 'Sleep' or name == 'Repeat':
            Lb2.insert(x, name + '({})'.format(currentScript.functions[x].extra.time))
            Lb2.place(x=0, y=40)
        else:
            Lb2.insert(x, name)
            Lb2.place(x=0, y=40)


def addFunction():
    place = Lb2.curselection()[0]
    functionName = functionList[Lb1.curselection()[0]]
    currentFunction = currentScript.functions[place]
    currentLineFather = currentScript.linesFather[place]

    if functionName == 'Sleep':
        count = 0
        sleep = Sleep('?')
        frame1 = getFrame(functionName)

        if currentLineFather.fatherName == 'Repeat':
            currentFunction = Function(functionName, '', place, frame1,
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), sleep)
            currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                           currentLineFather.fatherName)
            repeatFatherFunction = currentScript.functions[currentLineFather.fromIndex]
            if repeatFatherFunction.extra.functions[0].name == '':
                currentScript.functions[currentLineFather.fromIndex].extra.functions[0] = Function(functionName, '',
                                                                                                   place, frame1, (
                                                                                                       currentLineFather.fromIndex,
                                                                                                       currentLineFather.fatherName),
                                                                                                   sleep)
            else:
                currentScript.functions[currentLineFather.fromIndex].extra.functions.insert(
                    currentLineFather.fromIndex + place - 2, Function(functionName, '', place, frame1, (
                        currentLineFather.fromIndex, currentLineFather.fatherName), sleep))

        else:
            currentFunction = Function(functionName, '', place, frame1,
                                       (currentLineFather.fromIndex, functionName), sleep)
            currentLineFather = LineFather(place, place, functionName)
        getInputBox(currentFunction.extra, frame1.children.get('label'), frame1.children.get('input'), changeSleepTime)
        currentFunction.frame = frame1
    elif functionName == 'Repeat':
        count = 0
        repeat = Repeat('?', [Function('', '', place +2 , '', '', '')])
        frame1 = getFrame(functionName)
        tempFunction = ['{', '', '}']

        if currentLineFather.fatherName == 'Repeat' and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, frame1,
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), repeat)

            for i in range(place+1,place+4):
                currentScript.functions.insert(i, Function(tempFunction[i-(place+1)], '', place + 1, '', (place, functionName), ''))

            repeatFatherFunction = currentScript.functions[currentLineFather.fromIndex]
            if repeatFatherFunction.extra.functions[0].name == '':
                currentScript.functions[currentLineFather.fromIndex].extra.functions[0] = Function(
                    functionName, '', place, frame1,
                    (currentLineFather.fromIndex, currentLineFather.fatherName), repeat)
            else:
                currentScript.functions[currentLineFather.fromIndex].extra.functions.insert(
                    currentLineFather.fromIndex + place - 2,
                    Function(functionName, '', place, frame1,
                             (currentLineFather.fromIndex, currentLineFather.fatherName), repeat))
            for i in range(currentLineFather.fromIndex + place - 1,currentLineFather.fromIndex + place + 2):
                currentScript.functions[currentLineFather.fromIndex].extra.functions.insert(i, Function(tempFunction[i-(currentLineFather.fromIndex + place - 1)], '', place + 1, '', (place, functionName), ''))

        else:
            for i in range(place, place + 4, 1):
                if (i == place):
                    currentScript.linesFather[i] = LineFather(place, place + 3, functionName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, frame1,
                                       (currentLineFather.fromIndex, functionName), repeat)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', place + 1, '',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)
        getInputBox(currentFunction.extra, frame1.children.get('label'), frame1.children.get('input'), changeRepeatTime)
    else:
        frame1 = getFrame(functionName)
        if currentLineFather.fatherName == 'Repeat':
            currentFunction = Function(functionName, '', place, frame1,
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), '')
            currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                           currentLineFather.fatherName)
            repeatFatherFunction = currentScript.functions[currentLineFather.fromIndex]
            if repeatFatherFunction.extra.functions[place - currentLineFather.fromIndex - 2].name == '':
                currentScript.functions[currentLineFather.fromIndex].extra.functions[place - currentLineFather.fromIndex - 2] = Function(functionName, '',
                                                                                                   place, frame1, (
                                                                                                       currentScript.linesFather[
                                                                                                           place].fromIndex,
                                                                                                       currentScript.linesFather[
                                                                                                           place].fatherName),
                                                                                                   '')
            else:
                currentScript.functions[currentLineFather.fromIndex].extra.functions.insert(
                    place - currentLineFather.fromIndex - 2, Function(functionName, '', place, frame1, (
                        currentLineFather.fromIndex, currentLineFather.fatherName), ''))

        else:
            currentFunction = Function(functionName, '', place, frame1, (currentLineFather.fromIndex, functionName), '')
            currentLineFather = LineFather(place, place, functionName)

    currentScript.functions[place] = currentFunction
    currentScript.linesFather[place] = currentLineFather
    updateCurrentScript()
    updateLb2()
    Lb2.selection_clear(0, END)
    Lb1.selection_clear(0, END)

def removeFunction(function,functionIndex):
    listOfIndexToPop = []
    if function.name == 'Repeat':
        for func in function.extra.functions:
            if(func.name == 'Repeat'):
                listOfIndexToPop.append(removeFunction(func,func.id + functionIndex))
            else:
                listOfIndexToPop.append(func.id)
        listOfIndexToPop.append(function.id)
        listOfIndexToPop.append(function.id + 1)
        listOfIndexToPop.append(currentScript.linesFather[function.id].toIndex)
    else:
        print('kaka')
    return listOfIndexToPop


def removeFunctions():
    index = Lb2.curselection()[0]
    if(currentScript.functions[index].name =='{' or currentScript.functions[index].name =='}' ):
        msgbox = tkinter.messagebox.showerror('Notic!', 'You cant remove this, this is not a function.')

    popedFunc = currentScript.functions[index]
    popedFuncName =popedFunc.name

    kaka = removeFunction(popedFunc,index)
    print (kaka)

    #
    # listOfIndexToPop = []
    # for x in range(len(currentScript.functions)):
    #
    #     if currentScript.functions[x].father == (index, popedFuncName):
    #         listOfIndexToPop.append(x)
    #     if currentScript.functions[x].name == 'Repeat':
    #         index = x
    #         popedFuncName = 'Repeat'
    #
    # for x in listOfIndexToPop[::-1]:      # this will reverse the list of index to pop to avoid  IndexError exeption.
    #     try:
    #         img = currentScript.functions[x].img.img
    #         if(img!=''):
    #             path = currentScript.path+'ScreenShots\\'+img
    #             os.remove(path)
    #     except:
    #         pass
    #     currentScript.functions.pop(x)


    # for x in currentScript.functions:
    #     print(x.printFunction())
    updateCurrentScript()
    updateLb2()


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
    Lb1.config(state='normal')
    addFunc.config(state='normal')
    try:
        index = Lb2.curselection()[0]
    except:
        return
    frame = ''
    id = index
    photoName = ''
    functionName = ''
    for x in currentScript.functions:
        if x.id == id:
            try:
                if(x.img != ''):
                    photoName = x.img.img
                functionName = x.name
            except:
                pass
            frame = currentScript.functions[index].frame
            break
    if frame != '':
        frame.place(x=1455, y=600)
        if photoName != '':
            for childName, childValue in frame.children.items():
                if childName == 'fileName':
                    childValue.config(text='File Name: {}'.format(photoName))
                if childName == 'canvasFrame':
                    canvas = Canvas(childValue, width=437, height=150, name='canvas')
                    one = PhotoImage(file=currentScript.path + "ScreenShots\\" + photoName)
                    photoViewFrame.one = one  # to prevent the image garbage collected.
                    canvas.create_image((0, 0), image=one, anchor="nw")
                    canvas.pack()

        frame.tkraise()


def disableTakeScreenShot(event):
    takeScreenShot.config(state=DISABLED)


def createTree(frame):
    tree = ttk.Treeview(frame)
    s = ttk.Style()
    s.configure('Treeview', rowheight=40)

    path = os.path.dirname(os.path.abspath(__file__))

    root = tree.insert('', 'end', text=path + '\Scripts', open=True, tag='T')
    fileImg = PhotoImage(file='').subsample(3, 3)
    tree.image = fileImg
    SUBS(path + '\\Scripts', root, tree, fileImg)
    tree.column("#0", width=frame.winfo_reqwidth(), stretch=False)

    tree.place(x=0, y=0)
    return tree


def moveUp():
    index = Lb2.curselection()[0]
    currentScript.functions[index].id = index - 1
    currentScript.functions[index - 1].id = index
    a, b = index, index - 1
    currentScript.functions[b], currentScript.functions[a] = currentScript.functions[a], currentScript.functions[b]
    listReload(Lb2)
    Lb2.selection_set(index - 1)


def moveDown():
    index = Lb2.curselection()[0]
    currentScript.functions[index].id = index + 1
    currentScript.functions[index + 1].id = index
    a, b = index + 1, index
    currentScript.functions[b], currentScript.functions[a] = currentScript.functions[a], currentScript.functions[b]
    listReload(Lb2)
    Lb2.selection_set(index + 1)


def listReload(list):
    list.delete(0, 'end')
    for x in range(0, len(currentScript.functions)):
        Lb2.insert(x, currentScript.functions[x].name)
        Lb2.place(x=0, y=40)


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def checkImageInFunc():
    funcWithoutImage = ""
    index = 1
    for func in currentScript.functions:
        if func.name == 'Repeat':
            if func.extra.time == '?':
                funcWithoutImage += ("The {} in line {} doesn't have repeat time\n".format(func.name, index))
        elif func.name == 'Sleep':
            if func.extra.time == '?':
                funcWithoutImage += ("The {} in line {} doesn't have sleep time\n".format(func.name, index))
        elif func.img == '' and func.name != '' and func.name != '{' and func.name != '}':
            funcWithoutImage += ("The {} in line {} doesn't have screenshot\n".format(func.name, index))
        index += 1
    return funcWithoutImage


def runHendle():
    functionNum = 0
    funcWithoutImage = checkImageInFunc()
    if funcWithoutImage != '':
        popupmsg(funcWithoutImage)
    else:
        mainScreen.iconify()
        for func in range(len(currentScript.functions)):
            if func >= functionNum:
                if currentScript.functions[func].name == 'Repeat':
                    functionNum += functions_handler.repeat_handle(currentScript.functions[func].extra.time,
                                                                   currentScript.functions[func].extra.functions,
                                                                   currentScript.path) + 3
                elif currentScript.functions[func].name == 'Left-Click':
                    functions_handler.left_click_handle(currentScript.functions[func].img, currentScript.path)
                    functionNum += 1
                elif currentScript.functions[func].name == 'Exist':
                    functions_handler.exist_handle(currentScript.functions[func].img)
                    functionNum += 1
                elif currentScript.functions[func].name == 'NotExist':
                    functions_handler.not_exist_handle(currentScript.functions[func].img)
                    functionNum += 1
                elif currentScript.functions[func].name == 'Double-Click':
                    functions_handler.double_click_handle(currentScript.functions[func].img, currentScript.path)
                    functionNum += 1
                elif currentScript.functions[func].name == 'Right-Click':
                    functions_handler.right_click_handle(currentScript.functions[func].img, currentScript.path)
                    functionNum += 1
                elif currentScript.functions[func].name == 'Sleep':
                    functions_handler.sleep_handle(currentScript.functions[func].extra.time)
                    functionNum += 1
    mainScreen.deiconify()


def saveFunctions():
    block = []
    for x in currentScript.functions:
        if (x.img != ''):
            imgdict = x.img.getDict()
        else:
            imgdict = ''
        if (x.extra != ''):
            block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '', 'father': str(x.father),
                          'extra': x.extra.getDict()})
        else:
            block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '', 'father': str(x.father),
                          'extra': ''})
    return block


def saveLinesFather():
    block = []
    for x in currentScript.linesFather:
        block.append({'fatherName':x.fatherName,'fromIndex':x.fromIndex,'toIndex':x.toIndex})
    return block


def savehundle():
    functionPath = currentScript.path + "functions.json"
    try:
        os.remove(functionPath)
    except:
        pass
    functionsblock = saveFunctions()
    linesFatherblock = saveLinesFather()
    with open(functionPath, 'w+') as outfile:
        outfile.write(json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))



def saveAsHundle():
    # filePath = tkinter.filedialog.asksaveasfilename(initialdir=".", title="Select file",
    #                                                 filetypes=(("txt files", "*.json"), ("all files", "*.*")))

    functionPath = tkinter.filedialog.asksaveasfilename(initialdir=".", title="Select file",
                                                    filetypes=(("Json file", "*.json"), ("all files", "*.*")))
    functionPath+= '.json'
    try:
        os.remove(functionPath)
    except:
        pass
    functionsblock = saveFunctions()
    linesFatherblock = saveLinesFather()
    with open(functionPath, 'w+') as outfile:
        outfile.write(json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))


def openFunctions(data):
    inputFunctions = []
    for x in data:
        inputFunctions.append(Function.getFunction(x))
    currentScript.functions = copy.copy(inputFunctions)


def openLinesFather(data):
    inputFunctions = []
    for x in data:
        inputFunctions.append(LineFather(x['fromIndex'],x['toIndex'],x['fatherName']))
    currentScript.linesFather = copy.copy(inputFunctions)


def openButton():
    filePath = tkinter.filedialog.askopenfilename(initialdir=".", title="Select file",
                                                  filetypes=(("json files", "*.json"), ("all files", "*.*")))
    currentScript.functions.clear()
    with open(filePath) as json_file:
        data = json_file.read()
        functionsData = json.loads(data[:data.index('\n')])
        linesFatherData = json.loads(data[data.index('\n')+1:])

    openFunctions(functionsData)
    openLinesFather(linesFatherData)
    updateLb2()


def TreeviewD_Click(event):
    item_id = tree.selection()[0]
    parent_id = tree.parent(item_id)
    fullPath = ''
    while item_id != '':
        temp = tree.item(item_id)['text']
        if fullPath == '':
            fullPath = temp
        else:
            fullPath = temp + '\\' + fullPath
        item_id = parent_id
        parent_id = tree.parent(item_id)

    if currentScript.functions != []:
        msgbox = tkinter.messagebox.askyesnocancel('Notic!', 'Do you want to save changes you made?')
        if (msgbox == True):
            savehundle()
        elif (msgbox == None):
            return
    currentScript.functions.clear()

    with open(fullPath) as json_file:
        data = json_file.read()
        functionsData = json.loads(data[:data.index('\n')])
        linesFatherData = json.loads(data[data.index('\n')+1:])

    openFunctions(functionsData)
    openLinesFather(linesFatherData)
    updateLb2()


def insertA():
    try:
        place = Lb2.curselection()[0]
    except:
        place = 0
    currentScript.functions.insert(place, Function('', '', place, '', '', ''))
    if len(currentScript.functions) > 1:
        nextFunction = currentScript.functions[place + 1]
    if (len(currentScript.functions) > 1 and nextFunction.father[1] == 'Repeat' and not (
            nextFunction.name == 'Repeat')):
        currentScript.linesFather.insert(place, currentScript.linesFather[place + 1])
        currentScript.linesFather[currentScript.linesFather[place + 1].fromIndex].toIndex += 1
    else:
        currentScript.linesFather.insert(place, LineFather(place, place, ''))
    for x in range(len(currentScript.functions)):
        if x > place:
            newId = currentScript.functions[x].id

    if len(currentScript.functions) > 0:
        updateCurrentScript()
    updateLb2()
    Lb2.select_set(place)


def insertB():
    try:
        place = Lb2.curselection()[0] + 1
    except:
        place = 0
    currentScript.functions.insert(place, Function('', '', place, '', '', ''))
    if len(currentScript.functions) > 1:
        previousFunction = currentScript.functions[place - 1]
    if len(currentScript.functions) > 1 and previousFunction.father[1] == 'Repeat' and previousFunction.name != '}':
        currentScript.linesFather.insert(place, LineFather(currentScript.linesFather[place].fromIndex,
                                                           currentScript.linesFather[place].toIndex, currentScript.linesFather[place].fatherName))

        fromIndex = currentScript.linesFather[place].fromIndex
        toIndex = currentScript.linesFather[place].toIndex+2
        for i in range(fromIndex,toIndex):
            currentScript.linesFather[i].toIndex += 1
        currentScript.functions[place].father = (fromIndex, previousFunction.father[1])
        currentScript.functions[fromIndex].extra.functions.insert(place-fromIndex-2,Function('', '', place, '', (fromIndex,previousFunction.father[1]),''))
    else:
        currentScript.linesFather.insert(place, LineFather(place, place, ''))
    for x in range(len(currentScript.functions)):
        if x > place:
            newId = currentScript.functions[x].id + 1
            currentScript.functions[x].id = newId

    if len(currentScript.functions) > 1:
        updateCurrentScript()
    updateLb2()
    Lb2.select_set(place)


if __name__ == '__main__':
    functionFather = []
    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("MyApp")

    toolbarFrame = Frame(mainScreen, bd=3, width=mainScreen.winfo_screenwidth(), height=50)
    toolbarFrame.place(x=0, y=50)

    openButton = Button(toolbarFrame, text="Open", command=openButton)
    openButton.place(x=0, y=0)

    saveButton = Button(toolbarFrame, text="Save", command=savehundle)
    saveButton.place(x=70, y=0)

    saveAsButton = Button(toolbarFrame, text="Save As", command=saveAsHundle)
    saveAsButton.place(x=140, y=0)

    runButton = Button(toolbarFrame, text="Run", command=runHendle)
    runButton.place(x=230, y=0)

    stopButton = Button(toolbarFrame, text="Stop")
    stopButton.place(x=290, y=0)

    close = Button(mainScreen, text="Close", command=mainScreen.destroy)
    close.place(x=0, y=0)

    minimize = Button(mainScreen, text="Minimize", command=mainScreen.iconify)
    minimize.place(x=60, y=0)

    addFunc = Button(mainScreen, text="Add Functions", command=addFunction, state=DISABLED)
    addFunc.place(x=1600, y=100)

    explorerFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=500, height=430, bg='white')
    explorerFrame.place(x=10, y=150)

    mainFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=900, height=800, bg='white')
    mainFrame.place(x=535, y=150)

    moveDownButton = Button(mainFrame, text="Move down", command=moveDown)
    moveDownButton.place(x=20, y=0)

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

    photoViewFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=450, height=350, bg='white', name='photoViewFrame')
    photoViewFrame.place(x=1455, y=600)

    Lb1 = Listbox(funFrame, width=450, height=2400, exportselection=0)
    for x in range(0, len(functionList)):
        Lb1.insert(x, functionList[x])

    Lb1.place(x=0, y=0)
    Lb1.config(state=DISABLED)

    Lb2 = Listbox(mainFrame, width=99, height=300, exportselection=0)
    for x in range(0, len(currentScript.functions)):
        Lb2.insert(x, currentScript.functions[x])

    Lb2.place(x=0, y=40)

    Lb2.bind("<<ListboxSelect>>", func=FocusOnSelectedFunc)
    Lb2.bind("<FocusOut>", func=disableTakeScreenShot)

    tree = createTree(explorerFrame)
    tree.bind("<Double-1>", TreeviewD_Click)

mainScreen.mainloop()
