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
import copy
import time
import ScreenShotWindow
from ScreenShotWindow import ScreenShotWindow
import Sleep
from Sleep import Sleep
import Repeat
from Repeat import Repeat
import Photo
import LineFather
from LineFather import LineFather
import Function
from Function import Function
from win32api import GetSystemMetrics

functionList = ['Right-Click','Left-Click','Repeat','If','Else','Try','Except', 'Double-Click','Insert Input','Key-Press', 'Exist', 'NotExist', 'Sleep']
currentScript = script.Script("Folder1",[],0)
firstTime = True

def updateCurrentScript(index,delta):
    fromIndex = 0
    toIndex = 0
    for i in range(len(currentScript.functions)):
        if(i>toIndex):
            if(currentScript.functions[i].father[0] > index):
                fromIndex = currentScript.linesFather[currentScript.functions[i].father[0] + delta].fromIndex
                toIndex = currentScript.linesFather[currentScript.functions[i].father[0] + delta].toIndex
            else:
                fromIndex = currentScript.linesFather[currentScript.functions[i].father[0]].fromIndex
                toIndex = currentScript.linesFather[currentScript.functions[i].father[0]].toIndex

        if (currentScript.functions[i].name == 'Repeat'):
            fromIndex = i
            toIndex = i + len(currentScript.functions[i].extra.functions) + 2

        if currentScript.functions[i].father != '' and currentScript.functions[i].father[1] == 'Repeat':
            if(i != fromIndex and currentScript.functions[i].name != '{' and currentScript.functions[i].name != '}'):
                try:
                    if (currentScript.functions[i].father[0] > index ):
                        currentScript.functions[currentScript.functions[i].father[0] + delta].extra.functions[i - fromIndex - 2].id = i
                    else:
                        currentScript.functions[currentScript.functions[i].father[0]].extra.functions[i - fromIndex - 2].id = i
                except:
                    print('index:{} , extra:{} , extra index:{}'.format(currentScript.functions[i].father[0],currentScript.functions[currentScript.functions[i].father[0]].extra,i - fromIndex - 2))

            currentScript.functions[i].id = i
            currentScript.linesFather[i].fromIndex = fromIndex
            currentScript.linesFather[i].toIndex = toIndex
            if (currentScript.functions[i].father[0] > index):
                currentScript.functions[i].father = (
                currentScript.functions[i].father[0] + delta, currentScript.functions[i].father[1])
            else:
                currentScript.functions[i].father = (
                    currentScript.functions[i].father[0], currentScript.functions[i].father[1])

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
    delta = 0

    if functionName == 'Sleep':
        sleep = Sleep('?')

        if currentLineFather.fatherName == 'Repeat':
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), sleep)
            currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                           currentLineFather.fatherName)
            repeatFatherFunction = currentScript.functions[currentLineFather.fromIndex]
            if repeatFatherFunction.extra.functions[0].name == '':
                currentScript.functions[currentLineFather.fromIndex].extra.functions[0] = currentFunction
            else:
                currentScript.functions[currentLineFather.fromIndex].extra.functions.insert(currentLineFather.fromIndex + place - 2, currentFunction)

        else:
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, functionName), sleep)
            currentLineFather = LineFather(place, place, functionName)
        Function.getInputBox(currentFunction.extra, currentFunction.frame.children.get('label'), currentFunction.frame.children.get('input'), Sleep.changeSleepTime,Lb2,currentScript)
    elif functionName == 'Repeat':
        delta = 3
        repeat = Repeat('?', [Function('', '', place +2 , '',(place, functionName), '')])
        tempFunction = ['{', '', '}']

        if currentLineFather.fatherName == 'Repeat' and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, '',(currentLineFather.fromIndex, currentLineFather.fatherName), repeat)
            repeatFatherFunction = currentScript.functions[currentLineFather.fromIndex]
            if repeatFatherFunction.extra.functions[place-currentLineFather.fromIndex - 2].name == '':
                repeatFatherFunction.extra.functions[0] = currentFunction
            else:
                repeatFatherFunction.extra.functions.insert(currentLineFather.fromIndex + place - 2,currentFunction)
            for i in range(place+1,place+4):
                tempFunc = Function(tempFunction[i-(place+1)], '', place + 1, '', (place, functionName), '')
                currentScript.functions.insert(i, tempFunc)
                repeatFatherFunction.extra.functions.insert(currentLineFather.fromIndex + i - 2,tempFunc)

        else:
            for i in range(place, place + 4, 1):
                if (i == place):
                    currentScript.linesFather[i] = LineFather(place, place + 3, functionName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, functionName), repeat)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', place + 1, '',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)
        currentFunction.getInputBox(currentFunction.extra, currentFunction.frame.children.get('label'), currentFunction.frame.children.get('input'), Repeat.changeRepeatTime,Lb2,currentScript)
    else:
        if currentLineFather.fatherName == 'Repeat':
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), '')
            currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                           currentLineFather.fatherName)
            repeatFatherFunction = currentScript.functions[currentLineFather.fromIndex]
            if repeatFatherFunction.extra.functions[place - currentLineFather.fromIndex - 2].name == '':
                repeatFatherFunction.extra.functions[place - currentLineFather.fromIndex - 2] = currentFunction
            else:
                repeatFatherFunction.extra.functions.insert(
                    place - currentLineFather.fromIndex - 2, currentFunction)

        else:
            currentFunction = Function(functionName, '', place, '', (currentLineFather.fromIndex, functionName), '')
            currentLineFather = LineFather(place, place, functionName)

    currentScript.functions[place] = currentFunction
    currentScript.linesFather[place] = currentLineFather
    updateCurrentScript(place,delta)
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
        listOfIndexToPop.append(function.id)
    return listOfIndexToPop


def removeFunctions():
    delta = 0
    index = Lb2.curselection()[0]
    if(currentScript.functions[index].name =='{' or currentScript.functions[index].name =='}' ):
        msgbox = tkinter.messagebox.showerror('Notic!', 'You cant remove this, this is not a function.')

    popedFunc = currentScript.functions[index]
    popedFuncName =popedFunc.name
    if(popedFuncName == 'Repeat'):
        delta = (len(currentScript.functions[index].extra.functions) + 3) * -1
        Repeat.removeRepeat(index,currentScript)
    else:
        delta = -1
        currentScript.functions.pop(index)
        currentScript.linesFather.pop(index)
    updateCurrentScript(index,delta)
    updateLb2()


def window2():
    window2 = ScreenShotWindow(mainScreen,Lb2,currentScript,explorerFrame)


def SUBS(path, parent, tree):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        # tree.image = fileImg

        if os.path.isdir(abspath):
            parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")
            SUBS(abspath, parent_element, tree)
        else:
            parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")


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
    reportFrame()
def disableTakeScreenShot(event):
    takeScreenShot.config(state=DISABLED)


def createTree(frame):
    tree = ttk.Treeview(frame)
    s = ttk.Style()
    s.configure('Treeview', rowheight=40)
    path = os.path.dirname(os.path.abspath(__file__))
    root = tree.insert('', 'end', text=path + '\Scripts', open=True, tag='T')
    # fileImg = PhotoImage(file='').subsample(3, 3)
    # tree.image = fileImg
    SUBS(path + '\\Scripts', root, tree)
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
            block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '', 'fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                          'extra': x.extra.getDict()})
        else:
            block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '', 'fatherIndex': str(x.father[0]),'fatherName':x.father[1],
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
    tempFunction =[0] * len(data)
    for x in data:
        func = Function('','','','','','')
        inputFunctions.append(func.getFunction(x,Lb2,currentScript,tempFunction))
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
    if place > 0 and place <= len(currentScript.functions)-1:
        previousFunction = currentScript.functions[place - 1]
    else:
        previousFunction = ''
    if place >= 0 and place < len(currentScript.functions)-1:
        nextFunction = currentScript.functions[place + 1]
    else:
        nextFunction = ''
    if (previousFunction != '' and nextFunction !='' ):
        if(previousFunction.father == nextFunction.father):
            currentScript.linesFather.insert(place, LineFather(currentScript.linesFather[previousFunction.father[0]].fromIndex,
                                                               currentScript.linesFather[previousFunction.father[0]].toIndex, currentScript.linesFather[previousFunction.father[0]].fatherName))
            fromIndex = currentScript.linesFather[place].fromIndex
            currentScript.functions[place].father = (fromIndex, nextFunction.father[1])
            currentScript.functions[fromIndex].extra.functions.insert(place - fromIndex - 2, Function('', '', place, '', (
            fromIndex, nextFunction.father[1]), ''))
        else:
            if(nextFunction.name !='Repeat'):
                currentScript.linesFather.insert(place, LineFather(
                    currentScript.linesFather[nextFunction.father[0]].fromIndex,
                    currentScript.linesFather[nextFunction.father[0]].toIndex,
                    currentScript.linesFather[nextFunction.father[0]].fatherName))
                fromIndex = currentScript.linesFather[place].fromIndex
                currentScript.functions[place].father = (fromIndex, nextFunction.father[1])
                currentScript.functions[fromIndex].extra.functions.insert(place - fromIndex - 2,
                                                                          Function('', '', place, '', (
                                                                              fromIndex, nextFunction.father[1]), ''))
            else:
                currentScript.linesFather.insert(place, LineFather(place, place, ''))
                currentScript.functions[place].father = (place, currentScript.functions[place].name)
    else:
        currentScript.linesFather.insert(place, LineFather(place, place, ''))
        currentScript.functions[place].father = (place, currentScript.functions[place].name)

    if len(currentScript.functions) > 0:
        updateCurrentScript(place-1,1)
    updateLb2()
    Lb2.select_set(place)


def insertB():
    try:
        place = Lb2.curselection()[0] + 1
    except:
        place = 0
    currentScript.functions.insert(place, Function('', '', place, '', '', ''))
    if place > 0 and place <= len(currentScript.functions) - 1:
        previousFunction = currentScript.functions[place - 1]
    else:
        previousFunction = ''
    if place >= 0 and place < len(currentScript.functions) - 1:
        nextFunction = currentScript.functions[place + 1]
    else:
        nextFunction = ''
    if (nextFunction != ''):
        currentScript.linesFather.insert(place,
                                         LineFather(currentScript.linesFather[nextFunction.father[0]].fromIndex,
                                                    currentScript.linesFather[nextFunction.father[0]].toIndex,
                                                    currentScript.linesFather[nextFunction.father[0]].fatherName))
        fromIndex = currentScript.linesFather[place].fromIndex
        currentScript.functions[place].father = (fromIndex, nextFunction.father[1])
        currentScript.functions[fromIndex].extra.functions.insert(place - fromIndex - 2, Function('', '', place, '', (
            fromIndex, nextFunction.father[1]), ''))

    else:
        currentScript.linesFather.insert(place, LineFather(place, place, ''))
        currentScript.functions[place].father = (place,currentScript.functions[place].name)
    if len(currentScript.functions) > 1:
        updateCurrentScript(place,1)
    updateLb2()
    Lb2.select_set(place)

def closeStartWindow(event, startWin):
    startWin.destroy()
    mainScreen.deiconify()
    mainScreen.state("zoomed")


def getCenterOfScreen(screen):
    h = screen.winfo_height()
    w = screen.winfo_width()
    wScreen = GetSystemMetrics(0)
    hScreen = GetSystemMetrics(1)
    xPoint = (wScreen/2) - (w/2)
    yPoint = hScreen/2 - h/2
    return(int(xPoint), int(yPoint))

def Minimize_and_Open(event, screenToMini):
    screenToMini.iconify()
    try:
        filePath = tkinter.filedialog.askopenfilename(initialdir=".", title="Select file",
                                                  filetypes=(("json files", "*.json"), ("all files", "*.*")))
        print(filePath)
        currentScript.functions.clear()
        with open(filePath) as json_file:
            data = json_file.read()
            functionsData = json.loads(data[:data.index('\n')])
            linesFatherData = json.loads(data[data.index('\n') + 1:])

        openFunctions(functionsData)
        openLinesFather(linesFatherData)
        updateLb2()

        closeStartWindow(None,screenToMini)

    except:
        screenToMini.deiconify()






def startScreen():
    firstTime = False
    startS = Tk()
    startS.title("Automation Tool Program")
    startS.geometry('1100x500')
    startS.update_idletasks()
    mainScreen.withdraw()
    x,y = getCenterOfScreen(startS)
    startS.geometry("1100x500+" + str(x)+'+'+str(y))
    startS.update_idletasks()



    title = Label(startS, text = 'Automation Testing Tool', font=("Helvetica", 30))
    title.place(x=200,y=10)
    subtitle = Label(startS, text='Welcome! please select you pice of shit!', font=("Helvetica", 12))
    subtitle.place(x=250, y=100)

    newProject = Button(startS, text='New Project', width=20)
    newProject.bind('<Button-1>', lambda event: closeStartWindow(event, startS))
    newProject.place(x=400, y=200)

    load = Button(startS, text='load', width =20)
    load.bind('<Button-1>', lambda event: Minimize_and_Open(event, startS))
    load.place(x=400, y=250)

    close = Button(startS, text='Close', width=20)
    close.bind('<Button-1>', func=quit)
    close.place(x=400, y=300)
    startS.attributes('-topmost', True)





def reportFrame():
    data = {}

    reportFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=GetSystemMetrics(0), height=400)
    reportFrame.place(x=0, y=mainScreen.winfo_height() - 50)

    buttonUp = Button(reportFrame, text='⬆')
    buttonUp.place(x=mainScreen.winfo_width() - 40)
    buttonUp.bind('<Button-1>', lambda event: exposeReport(event, reportFrame, buttonUp))


    reportContex = Frame(reportFrame, bd=3, relief=SUNKEN, width=GetSystemMetrics(0) - 300, bg='white', height=400)
    reportContex.place(x=100, y=50)
    size = GetSystemMetrics(0) - 300
    getRepo = Button(reportFrame, text='Get Repo')
    getRepo.place(x=mainScreen.winfo_width() - 150, y=100)
    getRepo.bind('<Button-1>', lambda event: getReport(event, reportContex, data, size))

    clearReport = Button(reportFrame, text='Clear All')
    clearReport.place(x=mainScreen.winfo_width() - 150)
    clearReport.bind('<Button-1>', lambda event: clearRe(event, data, reportContex ))


def clearRe(event, data, frame):
    data.clear()
    for i in frame.winfo_children():
        try:
            i.destroy()
        except:
            pass


def getReport(event, frameToWrite, data, size):
    data.update({"set_info":{}})
    counter=1
    for x in currentScript.functions:
        if x.name!='{' and x.name !='}':
            if(x.extra!=''):
                extra = x.extra.getDict()
            else:
                extra="no other parameters"

            data['set_info'].update({
                x.name:{
                    'id_number': str(x.id),
                    'more_vars': extra
                }



            })
            counter+=1


    scrollbar = Scrollbar(frameToWrite)
    scrollbar.pack(side=RIGHT, fill=Y,expand=False)

    tree = ttk.Treeview(frameToWrite, yscrollcommand=scrollbar.set)
    root = tree.insert('', 'end', text='', open=True, tag='T')
    s = ttk.Style()

    tree.pack(side = LEFT, fill = BOTH)
    scrollbar.config(command=tree.yview)
    jsonTree(frameToWrite, data, tree, root)
    tree.column("#0", width=size, stretch=False)

def jsonTree(frame, data, tree, parent):

    for key, value in data.items():
        if isinstance(value,list):
            value = value[0]

        if isinstance(value,dict):
            parent_element = tree.insert(parent, 'end', text=key, open=True, tag="T")
            jsonTree(frame, value , tree, parent_element)
            # print('insert ' + str(key) + ' his uid is: ' + str(parent_element) + ' his parent uid is: ' + str(parent) )

        else:
            parent_element = tree.insert(parent, 'end', text=(key + ':' + value), open=True, tag="T")
            pass


def exposeReport(event, frame, button):
    counter = 0

    if(button.cget('text')=='⬆'):

        while(counter!=10):
                y = frame.winfo_y() - 30
                frame.place(y=y)
                frame.update()
                time.sleep(0.02)
                counter+=1
        button['text'] = '⬇'

    else:
        while (counter != 10):
            y = frame.winfo_y() + 30
            frame.place(y=y)
            frame.update()
            counter += 1
        button['text'] = '⬆'




if __name__ == '__main__':
    functionFather = []

    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("MyApp")
    if firstTime :
        startScreen()
    toolbarFrame = Frame(mainScreen, bd=3, width=mainScreen.winfo_screenwidth(), height=50)
    toolbarFrame.place(x=0, y=50)

    openButton = Button(toolbarFrame, text="Open", command=openButton)
    openButton.place(x=0, y=0)

    saveButton = Button(toolbarFrame, text="Save", command=savehundle)
    saveButton.place(x=70, y=0)

    saveAsButton = Button(toolbarFrame, text="Save As", command=saveAsHundle)
    saveAsButton.place(x=140, y=0)

    photo = PhotoImage(file=r"img\start2.png")
    photoimage = photo.subsample(3, 3)
    runButton = Button(toolbarFrame, text="Run", command=runHendle, image = photoimage,)
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

    reportFrame()


mainScreen.mainloop()
