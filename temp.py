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
import IfExist
from IfExist import IfExist
import IfNotExist
from IfNotExist import IfNotExist
import Else
from Else import Else
import Photo
import LineFather
from LineFather import LineFather
import Function
from Function import Function
from win32api import GetSystemMetrics
import threading
from datetime import datetime

functionList = ['Right-Click','Left-Click','Repeat','If-Exist','If-Not-Exist','Else', 'Double-Click','Insert-Input', 'Sleep']
# currentScript = script.Script('Folder1',[],0)
currentScript = None
firstTime = True
process = []

def updateCurrentScript(index,delta):
    fromIndex = 0
    toIndex = 0
    for i in range(len(currentScript.functions)): #run on all the functions
        if(i>toIndex):
            if(currentScript.functions[i].father[0] > index):
                fromIndex = currentScript.linesFather[currentScript.functions[i].father[0] + delta].fromIndex
                toIndex = currentScript.linesFather[currentScript.functions[i].father[0] + delta].toIndex
            else:
                fromIndex = currentScript.linesFather[currentScript.functions[i].father[0]].fromIndex
                toIndex = currentScript.linesFather[currentScript.functions[i].father[0]].toIndex

        if (currentScript.functions[i].name == 'Repeat' or currentScript.functions[i].name == 'If-Exist' or currentScript.functions[i].name == 'If-Not-Exist' or currentScript.functions[i].name == 'Else' ):
            fromIndex = i
            toIndex = i + len(currentScript.functions[i].extra.functions) + 2

        if currentScript.functions[i].father != '' and (currentScript.functions[i].father[1] == 'Repeat' or currentScript.functions[i].father[1] == 'If-Exist' or currentScript.functions[i].father[1] == 'If-Not-Exist' or currentScript.functions[i].father[1] == 'Else'):
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



def updateLb2():
    Lb2.delete(0, 'end')
    for x in range(0, len(currentScript.functions)):
        name = currentScript.functions[x].name
        shift = ' ' * currentScript.functions[x].indention * 5
        if name == 'Sleep' or name == 'Repeat':
            Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.time))
            Lb2.pack(side="left", fill="y")
            # Lb2.place(x=0, y=40)
        elif name == 'If-Exist' or name == 'If-Not-Exist':
            Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.image))
            Lb2.pack(side="left", fill="y")
            # Lb2.place(x=0, y=40)
        else:
            Lb2.insert(x, shift + name)
            Lb2.pack(side="left", fill="y")
            # Lb2.place(x=0, y=40)


def addFunction():
    place = Lb2.curselection()[0]
    functionName = functionList[Lb1.curselection()[0]]
    delta = 0

    try:
        currentFunction = currentScript.functions[place]
        currentLineFather = currentScript.linesFather[place]
    except:
        if(currentScript.functions==[] and place ==0):      ## case that this is the first time we add a function
            print('first time!')

    if functionName == 'Sleep':
        sleep = Sleep('?')

        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), sleep,currentScript.functions[currentLineFather.fromIndex].indention +1)

            currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                           currentLineFather.fatherName)

            tempLineFather = currentLineFather
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

            while True:
                if tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2].name == '':
                    tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2] = currentFunction
                else:
                    tempFatherFunction.extra.functions.insert(
                        place - tempLineFather.fromIndex - 2, currentFunction)
                if tempFatherFunction.father[0] == tempFatherFunction.id:
                    break
                tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

        else:
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, functionName), sleep)
            currentLineFather = LineFather(place, place, functionName)
        currentFunction.getInputBox(currentFunction.extra, currentFunction.frame.children.get('label'), currentFunction.frame.children.get('input'), Sleep.changeSleepTime,Lb2,currentScript)
    elif functionName == 'Repeat':
        delta = 3
        repeat = Repeat('?', [Function('', '', place +2 , '',(place, functionName), '')])
        tempFunction = ['{', '', '}']

        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))

            currentFunction = Function(functionName, '', place, '',(currentLineFather.fromIndex, currentLineFather.fatherName), repeat,currentScript.functions[currentLineFather.fromIndex].indention +1)

            tempLineFather = currentLineFather
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
            tempIndention = currentScript.functions[tempLineFather.fromIndex].indention + 1

            while True:
                if tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2].name == '':
                    tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2] = currentFunction
                else:
                    tempFatherFunction.extra.functions.insert(
                        place - tempLineFather.fromIndex - 2, currentFunction)
                for i in range(place + 1, place + 4):
                    tempFunc = Function(tempFunction[i - (place + 1)], '', i, '', (place, functionName), '',tempIndention)
                    if tempFatherFunction.father[0] == tempFatherFunction.id:
                        currentScript.functions.insert(i, tempFunc)
                    tempFatherFunction.extra.functions.insert(i - tempLineFather.fromIndex - 2, tempFunc)
                if tempFatherFunction.father[0] == tempFatherFunction.id:
                    break
                tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

        else:
            for i in range(place, place + 4, 1):
                if (i == place):
                    currentScript.linesFather[i] = LineFather(place, place + 3, functionName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, functionName), repeat)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, '',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)
        currentFunction.getInputBox(currentFunction.extra, currentFunction.frame.children.get('label'), currentFunction.frame.children.get('input'), Repeat.changeRepeatTime,Lb2,currentScript)
    elif functionName == 'If-Exist':
        delta = 3
        ifExist = IfExist('?', [Function('', '', place +2 , '',(place, functionName), '')])
        tempFunction = ['{', '', '}']

        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, '',(currentLineFather.fromIndex, currentLineFather.fatherName), ifExist,currentScript.functions[currentLineFather.fromIndex].indention +1)

            tempLineFather = currentLineFather
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
            tempIndention = currentScript.functions[tempLineFather.fromIndex].indention + 1

            while True:
                if tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2].name == '':
                    tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2] = currentFunction
                else:
                    tempFatherFunction.extra.functions.insert(
                        place - tempLineFather.fromIndex - 2, currentFunction)
                for i in range(place + 1, place + 4):
                    tempFunc = Function(tempFunction[i - (place + 1)], '', i, '', (place, functionName), '',
                                        tempIndention)
                    if tempFatherFunction.father[0] == tempFatherFunction.id:
                        currentScript.functions.insert(i, tempFunc)
                    tempFatherFunction.extra.functions.insert(i - tempLineFather.fromIndex - 2, tempFunc)
                if tempFatherFunction.father[0] == tempFatherFunction.id:
                    break
                tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

        else:
            for i in range(place, place + 4, 1):
                if (i == place):
                    currentScript.linesFather[i] = LineFather(place, place + 3, functionName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, functionName), ifExist)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, '',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)

    elif functionName == 'If-Not-Exist':
        delta = 3
        ifNotExist = IfNotExist('?', [Function('', '', place + 2, '', (place, functionName), '')])
        tempFunction = ['{', '', '}']

        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), ifNotExist,
                                       currentScript.functions[currentLineFather.fromIndex].indention + 1)

            tempLineFather = currentLineFather
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
            tempIndention = currentScript.functions[tempLineFather.fromIndex].indention + 1


            while True:
                if tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2].name == '':
                    tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2] = currentFunction
                else:
                    tempFatherFunction.extra.functions.insert(
                        place - tempLineFather.fromIndex - 2, currentFunction)
                for i in range(place + 1, place + 4):
                    tempFunc = Function(tempFunction[i - (place + 1)], '', i, '', (place, functionName), '',
                                        tempIndention)
                    if tempFatherFunction.father[0] == tempFatherFunction.id:
                        currentScript.functions.insert(i, tempFunc)
                    tempFatherFunction.extra.functions.insert(i - tempLineFather.fromIndex - 2, tempFunc)
                if tempFatherFunction.father[0] == tempFatherFunction.id:
                    break
                tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

        else:
            for i in range(place, place + 4, 1):
                if (i == place):
                    currentScript.linesFather[i] = LineFather(place, place + 3, functionName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, functionName), ifNotExist)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, '',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)
    elif functionName == 'Else':
        if place == 0 or (currentScript.functions[place-1].father[1] != 'If-Exist' and currentScript.functions[place-1].father[1] != 'If-Not-Exist'):
            popupmsg('cannot use Else function without ifExist or ifNotExist')
        else:
            delta = 3
            elseObj = Else([Function('', '', place +2 , '',(place, functionName), '')])
            tempFunction = ['{', '', '}']

            if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

                for i in range(place, place + 4, 1):
                    if i == place:
                        currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                                  currentScript.linesFather[i].toIndex,
                                                                  currentScript.linesFather[i].fatherName)
                    else:
                        currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
                currentFunction = Function(functionName, '', place, '',(currentLineFather.fromIndex, currentLineFather.fatherName), elseObj,currentScript.functions[currentLineFather.fromIndex].indention +1)

                tempLineFather = currentLineFather
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
                tempIndention = currentScript.functions[tempLineFather.fromIndex].indention + 1

                while True:
                    if tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2].name == '':
                        tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2] = currentFunction
                    else:
                        tempFatherFunction.extra.functions.insert(
                            place - tempLineFather.fromIndex - 2, currentFunction)
                    for i in range(place + 1, place + 4):
                        tempFunc = Function(tempFunction[i - (place + 1)], '', i, '', (place, functionName), '',
                                            tempIndention)
                        if tempFatherFunction.father[0] == tempFatherFunction.id:
                            currentScript.functions.insert(i, tempFunc)
                        tempFatherFunction.extra.functions.insert(i - tempLineFather.fromIndex - 2, tempFunc)
                    if tempFatherFunction.father[0] == tempFatherFunction.id:
                        break
                    tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                    tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

            else:
                for i in range(place, place + 4, 1):
                    if (i == place):
                        currentScript.linesFather[i] = LineFather(place, place + 3, functionName)
                    else:
                        currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
                currentFunction = Function(functionName, '', place, '',
                                           (currentLineFather.fromIndex, functionName), elseObj)
                for i in range(place + 1, place + 4):
                    currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, '',
                                                               (place, functionName), ''))
                currentLineFather = LineFather(place, place + 3, functionName)
    else:
        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:
            currentFunction = Function(functionName, '', place, '',
                                       (currentLineFather.fromIndex, currentLineFather.fatherName), '',currentScript.functions[currentLineFather.fromIndex].indention +1)
            currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                           currentLineFather.fatherName)

            tempLineFather = currentLineFather
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

            while True:
                if tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2].name == '':
                    tempFatherFunction.extra.functions[place - tempLineFather.fromIndex - 2] = currentFunction
                else:
                    tempFatherFunction.extra.functions.insert(
                        place - tempLineFather.fromIndex - 2, currentFunction)
                if tempFatherFunction.father[0] == tempFatherFunction.id:
                    break
                tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
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
    for x in Lb2.curselection():
        if len(Lb2.curselection())>1:
            if(x!=0):
                x-=1
        index = x
        removeFuncFatherIndex = index
        haveFather = False

        if currentScript.functions[index].father != (index,currentScript.functions[index].name):
            haveFather = True
            removeFuncFatherIndex = currentScript.linesFather[currentScript.functions[index].father[0]].fromIndex

        if(currentScript.functions[index].name =='{' or currentScript.functions[index].name =='}' ):
            msgbox = tkinter.messagebox.showerror('Notic!', 'You cant remove this, this is not a function.')

        popedFunc = currentScript.functions[index]
        popedFuncName =popedFunc.name
        if(popedFuncName == 'Repeat'):
            delta = (len(currentScript.functions[index].extra.functions) + 3) * -1
            Repeat.removeRepeat(removeFuncFatherIndex,index,currentScript,haveFather)
        elif (popedFuncName == 'If-Exist'):
            delta = (len(currentScript.functions[index].extra.functions) + 3) * -1
            IfExist.removeIfExist(removeFuncFatherIndex,index, currentScript,haveFather)
        elif (popedFuncName == 'If-Not-Exist'):
            delta = (len(currentScript.functions[index].extra.functions) + 3) * -1
            IfNotExist.removeIfNotExist(removeFuncFatherIndex,index, currentScript,haveFather)
        elif (popedFuncName == 'Else'):
            delta = (len(currentScript.functions[index].extra.functions) + 3) * -1
            Else.removeElse(removeFuncFatherIndex,index, currentScript,haveFather)
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

    mainScreen.update_idletasks()
    # mainScreen.update()

    try:
        index = Lb2.curselection()[0]
    except:
        return

    frame = ''
    id = index
    photoName = ''
    functionName = ''    # repoFrame_and_Button[0].destroy()

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
    s.configure('Treeview', rowheight=30)
    path = os.path.dirname(os.path.abspath(__file__))
    # root = tree.insert('', 'end', text=path + '\Scripts', open=True, tag='T')
    # fileImg = PhotoImage(file='').subsample(3, 3)
    # tree.image = fileImg
    # SUBS(path + '\\Scripts', root, tree)

    tree.pack(side='left')

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')

    tree.configure(yscrollcommand=vsb.set)
    tree.column("#0", width=frame.winfo_reqwidth(), stretch=False, anchor='c')
    tree.heading("#0", text="Project Files View")
    return tree


def moveUp():
    index = Lb2.curselection()[0]    # tree.place(x=0, y=0)

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
        Lb2.pack(side="left", fill="y")
        # Lb2.place(x=0, y=40)


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
        elif func.name == 'If-Exist':
            if func.extra.image == '?':
                funcWithoutImage += ("The {} in line {} doesn't have image\n".format(func.name, index))
        elif func.name == 'If-Not-Exist':
            if func.extra.image == '?':
                funcWithoutImage += ("The {} in line {} doesn't have image\n".format(func.name, index))
        elif func.img == '' and func.name != '' and func.name != '{' and func.name != '}' and func.name != 'Else':
            funcWithoutImage += ("The {} in line {} doesn't have screenshot\n".format(func.name, index))
        index += 1
    return funcWithoutImage


def runHendle():
    functionNum = 0
    ifExistFlag = True
    funcWithoutImage = checkImageInFunc()
    if funcWithoutImage != '':
        popupmsg(funcWithoutImage)
    else:
        mainScreen.iconify()
        for func in range(len(currentScript.functions)):
            if currentScript.functions[func].father[0] == currentScript.functions[func].id:
                if func >= functionNum:
                    if currentScript.functions[func].name == 'Repeat':
                        functionNum += functions_handler.repeat_handle(currentScript.functions[func],
                                                                       currentScript.path) + 3
                    elif currentScript.functions[func].name == 'Left-Click':
                        functions_handler.left_click_handle(currentScript.functions[func].img, currentScript.path)
                        functionNum += 1
                    elif currentScript.functions[func].name == 'If-Exist':
                        exist,tempFunctionNum = functions_handler.exist_handle(currentScript.functions[func],currentScript.path)
                        functionNum += tempFunctionNum
                        ifExistFlag = exist
                    elif currentScript.functions[func].name == 'If-Not-Exist':
                        exist,tempFunctionNum = functions_handler.not_exist_handle(currentScript.functions[func],
                                                                       currentScript.path)
                        functionNum += tempFunctionNum
                        ifExistFlag = exist
                    elif currentScript.functions[func].name == 'Else' and not ifExistFlag:
                        functions_handler.else_handle(currentScript.functions[func],
                                                                       currentScript.path)
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
                          'extra': x.extra.getDict(),'indention':x.indention})
        else:
            block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '', 'fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                          'extra': '','indention':x.indention})
    return block


def saveLinesFather():
    block = []
    for x in currentScript.linesFather:
        block.append({'fatherName':x.fatherName,'fromIndex':x.fromIndex,'toIndex':x.toIndex})
    return block


def saveHundle():
    functionPath = currentScript.path + "/functions.json"
    print(functionPath)
    try:
        os.remove(functionPath)
    except:
        pass
    functionsblock = saveFunctions()
    linesFatherblock = saveLinesFather()
    with open(functionPath, 'w+') as outfile:
        outfile.write(json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))

def make_new_project(label):
    functionPath = tkinter.filedialog.askdirectory()
    label.configure(text = functionPath)

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
    currentScript.path = functionPath

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
    projectNamePath = os.path.split(os.path.split(filePath)[0])
    label = projectNamePath[0]
    global currentScript
    currentScript = script.Script(projectNamePath[1], [], datetime.now(), path=label + '/')
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
            saveHundle()
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


def insert_A():
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


def insert_B():
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
    try:
        startWin.destroy()
    except:
        pass
    firstTime = False
    startS = Toplevel()
    startS.resizable(False, False)
    startS.overrideredirect(True)
    startS.geometry('1100x500')

    startS.update_idletasks()
    mainScreen.withdraw()
    x, y = getCenterOfScreen(startS)
    startS.geometry("1100x500+" + str(x) + '+' + str(y))
    startS.update_idletasks()

    frame = Frame(startS, width=110, height=500)
    frame.pack(fill=BOTH)

    canvas = Canvas(frame, width=110, height=500)
    canvas.pack(fill=BOTH)

    background = PhotoImage(file=r"img\StartUpScreen2.png")
    canvas.bg = background
    canvas.create_image(0, 0, anchor=NW, image=background)

    e1 = Entry(frame)
    e1.pack()
    e1.delete(0, END)
    e1.insert(0, "My_New_Project")

    label = ttk.Label(frame, text="Please select path of new project", background="white")
    label.place(height=40, width=600, x=365, y=310)

    newPButton = PhotoImage(file=r"img\buttonStart.png")
    canvas.Button1 = newPButton
    np = canvas.create_image(150, 400, anchor=NW, image=newPButton, tags="Start")
    canvas.tag_bind('Start', '<Button-1>', lambda event: save_new_project_and_run_app(label.cget("text"),e1.get(), startS))
    canvas.tag_bind('Start', '<Enter>', lambda event: hoverOn(event, canvas, np, 1))
    canvas.tag_bind('Start', '<Leave>', lambda event: hoverOff(event, canvas, np, 1))

    e1.place( height=40, width=600 ,x=365,y=215)
    Selec_F_Button = PhotoImage(file=r"img\buttonPaN.png")
    canvas.Button2 = Selec_F_Button
    Selec_F = canvas.create_image(135, 285, anchor=NW, image=Selec_F_Button, tags="PaN")
    canvas.tag_bind('PaN', '<Button-1>', lambda event: make_new_project(label))
    canvas.tag_bind('PaN', '<Enter>', lambda event: hoverOn(event, canvas, Selec_F, 5))
    canvas.tag_bind('PaN', '<Leave>', lambda event: hoverOff(event, canvas, Selec_F, 5))

    returnButton = PhotoImage(file=r"img\buttonReturn.png")
    canvas.Button3 = returnButton
    returnB = canvas.create_image(750, 400, anchor=NW, image=returnButton, tags="return")
    canvas.tag_bind('return', '<Button-1>', lambda event: startScreen())
    canvas.tag_bind('return', '<Enter>', lambda event: hoverOn(event, canvas, returnB, 6))
    canvas.tag_bind('return', '<Leave>', lambda event: hoverOff(event, canvas, returnB, 6))

    mainScreen.wait_window(startS)


def save_new_project_and_run_app(label,fileName, window):
    if label!='Please select path of new project':
        functionPath =  label+'/'+fileName + "/functions.json"
        global currentScript
        currentScript = script.Script(fileName,[],datetime.now(),path=label + '/')
        try:
            os.mkdir(label+'/'+fileName + '/ScreenShots')
        except:
            print('folder alreay exist!')

        #**************************** Just for testing **********************************
        try:
            os.mkdir(label+'/'+fileName + '/Test Image')
        except:
            print('folder alreay exist!')

        #********************************************************************************


        functionsblock = saveFunctions()
        linesFatherblock = saveLinesFather()

        root = tree.insert('', 'end', text=label+'/'+fileName, open=True, tag='T')
        SUBS(label+'/'+fileName, root, tree)

        insert_A()
        Lb2.select_set(0)
        Lb2.focus_force()
        FocusOnSelectedFunc(None)

        updateLb2()
        with open(functionPath, 'w+') as outfile:
            outfile.write(json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))


    window.destroy()
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
    screenToMini.destroy()

    try:
        filePath = tkinter.filedialog.askopenfilename(initialdir=".", title="Select file",
                                                  filetypes=(("json files", "*.json"), ("all files", "*.*")))
        projectNamePath = os.path.split(os.path.split(filePath)[0])
        label = projectNamePath[0]
        global currentScript
        currentScript = script.Script(projectNamePath[1], [], datetime.now(), path=label + '/')

        with open(filePath) as json_file:
            data = json_file.read()
            functionsData = json.loads(data[:data.index('\n')])
            linesFatherData = json.loads(data[data.index('\n') + 1:])


        openFunctions(functionsData)
        openLinesFather(linesFatherData)
        updateLb2()
        # closeStartWindow(None,screenToMini)
        folder_path = filePath[0:filePath.rfind('/')]
        root = tree.insert('', 'end', text=folder_path, open=True, tag='T')
        SUBS(folder_path, root, tree)

        mainScreen.deiconify()
        mainScreen.state("zoomed")
    except Exception as e:
        print(e)
        startScreen()

def startScreen():
    firstTime = False
    startS = Toplevel()
    startS.resizable(False, False)
    startS.overrideredirect(True)
    startS.geometry('1100x500')

    startS.update_idletasks()
    mainScreen.withdraw()
    x,y = getCenterOfScreen(startS)
    startS.geometry("1100x500+" + str(x)+'+'+str(y))
    startS.update_idletasks()

    frame = Frame(startS, width=110, height=500)
    frame.pack(fill=BOTH)

    canvas = Canvas(frame, width=110, height=500)
    canvas.pack(fill=BOTH)

    background = PhotoImage(file=r"img\StartUpScreen.png")
    canvas.bg = background
    canvas.create_image(0,0,anchor=NW, image=background)


    newPButton = PhotoImage(file=r"img\buttonNP.png")
    canvas.Button1 = newPButton
    np = canvas.create_image(150,400, anchor=NW, image=newPButton,  tags="NewProject")
    canvas.tag_bind('NewProject','<Button-1>', lambda event: closeStartWindow(event, startS))
    canvas.tag_bind('NewProject', '<Enter>', lambda event: hoverOn(event, canvas, np,2))
    canvas.tag_bind('NewProject', '<Leave>', lambda event: hoverOff(event, canvas, np,2))


    loadButton = PhotoImage(file=r"img\buttonLoad.png")
    canvas.Button2 = loadButton
    load = canvas.create_image(450, 400, anchor=NW, image=loadButton, tags="Load")
    canvas.tag_bind('Load', '<Button-1>', lambda event: Minimize_and_Open(event, startS))
    canvas.tag_bind('Load', '<Enter>',lambda event: hoverOn(event,canvas, load,3))
    canvas.tag_bind('Load', '<Leave>',lambda event: hoverOff(event, canvas, load,3))

    closeButton = PhotoImage(file=r"img\buttonClose.png")
    canvas.Button3 = closeButton
    close=canvas.create_image(750, 400, anchor=NW, image=closeButton, tags="Close")
    canvas.tag_bind('Close', '<Button-1>', lambda event: terminate(startS))
    canvas.tag_bind('Close', '<Enter>',lambda event: hoverOn(event,canvas, close,4))
    canvas.tag_bind('Close', '<Leave>',lambda event: hoverOff(event, canvas, close,4))



    startS.attributes('-topmost', True)
def terminate(screen):
    for widget in mainScreen.winfo_children():
        if isinstance(widget,Toplevel):
            widget.destroy()
    screen.destroy()
    exit()

def hoverOn(event,canvas, item, number):
    if (number == 1):
        Button1 = PhotoImage(file=r"img\buttonStartHover.png")
        canvas.z = Button1
        canvas.itemconfig(item, image=Button1)

    if(number==2):
        Button1 = PhotoImage(file=r"img\buttonNPHover.png")
        canvas.z = Button1
        canvas.itemconfig(item, image = Button1)
    if(number==3):
        Button1 = PhotoImage(file=r"img\buttonLoadHover.png")
        canvas.y = Button1
        canvas.itemconfig(item, image = Button1)

    if(number==4):
        Button1 = PhotoImage(file=r"img\buttonCloseHover.png")
        canvas.x = Button1
        canvas.itemconfig(item, image = Button1)

    if (number == 5):
        Button1 = PhotoImage(file=r"img\buttonPaNHover.png")
        canvas.y = Button1
        canvas.itemconfig(item, image=Button1)

    if (number == 6):
        Button1 = PhotoImage(file=r"img\buttonReturnHover.png")
        canvas.y = Button1
        canvas.itemconfig(item, image=Button1)

def hoverOff(event,canvas, item, number):
    if (number == 1):
        Button1 = PhotoImage(file=r"img\buttonStart.png")
        canvas.z = Button1
        canvas.itemconfig(item, image=Button1)

    if (number == 2):
        Button1 = PhotoImage(file=r"img\buttonNP.png")
        canvas.z = Button1
        canvas.itemconfig(item, image=Button1)

    if (number == 3):
        Button1 = PhotoImage(file=r"img\buttonLoad.png")
        canvas.y = Button1
        canvas.itemconfig(item, image=Button1)

    if(number==4):
        closeButton1 = PhotoImage(file=r"img\buttonClose.png")
        canvas.x = closeButton1
        canvas.itemconfig(item, image=closeButton1)
    if (number == 5):
        Button1 = PhotoImage(file=r"img\buttonPaN.png")
        canvas.y = Button1
        canvas.itemconfig(item, image=Button1)
    if (number == 6):
        Button1 = PhotoImage(file=r"img\buttonReturn.png")
        canvas.y = Button1
        canvas.itemconfig(item, image=Button1)

def reportFrame():
    data = {}

    reportFrame = Frame(mainScreen, bd=6, relief=SUNKEN, width=GetSystemMetrics(0), height=350, name='reportFrame')
    reportFrame.place(x=0, y=mainScreen.winfo_height() - 50)

    buttonUp = Button(reportFrame, text='⬆', name='arrow')
    buttonUp.place(x=mainScreen.winfo_width() - 40)
    buttonUp.bind('<Button-1>', lambda event: exposeReport(event, reportFrame, buttonUp))

    reportContex = Frame(reportFrame, bd=3, relief=SUNKEN, width=GetSystemMetrics(0) - 300, height=270)
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
    scrollbar.pack(side=RIGHT, fill=Y)
    tree = ttk.Treeview(frameToWrite, yscrollcommand=scrollbar.set, name='repoTree')
    root = tree.insert('', 'end', text='', open=True, tag='T')

    scrollbar.config(command=tree.yview)
    jsonTree(frameToWrite, data, tree, root)
    tree.column("#0", width=size)
    tree.pack(fill=BOTH, expand=True)

    frameToWrite.place(height=270)


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
                time.sleep(0.009)
                counter+=1
        button['text'] = '⬇'

    else:
        while (counter != 10):
            y = frame.winfo_y() + 30
            frame.place(y=y)
            frame.update()
            # time.sleep(0.009)
            counter += 1
        button['text'] = '⬆'



def autosave():

        countThread = process[0]
        print(AutoSave.get())
        flag =0
        if('No' in AutoSave.get()):
            return
        while (True):
            counter = 60*10
            while(counter!=0):
                if (not countThread.is_alive()):
                    flag = 1
                else:
                    flag =0
                print(counter)
                time.sleep(1)
                counter -= 1
                if flag==1:
                    return
            saveHundle()

def comboBoxSelect(event):
    try:
        for x in process:
           x._is_stopped = True
           time.sleep(1)

           x._is_stopped = False

    except:
        print('in exept')

    process.clear()
    saver = threading.Thread(target=autosave)
    process.append(saver)

    saver.start()



def on_closing():
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            for x in process:
                x._is_stopped = True
            mainScreen.destroy()

if __name__ == '__main__':
    functionFather = []

    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("MyApp")

    if firstTime :
        startScreen()
    toolbarFrame = Frame(mainScreen, bd=3, width=mainScreen.winfo_screenwidth(), height=50)
    toolbarFrame.place(x=0, y=0)

    openButton = Button(toolbarFrame, text="Open", command=openButton)
    openButton.place(x=0, y=0)

    saveButton = Button(toolbarFrame, text="Save", command=saveHundle)
    saveButton.place(x=70, y=0)

    saveAsButton = Button(toolbarFrame, text="Save As", command=saveAsHundle)
    saveAsButton.place(x=140, y=0)

    photo = PhotoImage(file=r"img\start2.png")
    photoimage = photo.subsample(3, 3)
    runButton = Button(toolbarFrame, text="Run", command=runHendle, image = photoimage)
    runButton.place(x=230, y=0)


    stopButton = Button(toolbarFrame, text="Stop")
    stopButton.place(x=290, y=0)

    addFunc = Button(mainScreen, text="Add Functions", command=addFunction, state=DISABLED)
    addFunc.place(x=1600, y=100)

    explorerFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=400, height=430, bg='white')
    explorerFrame.place(x=10, y=150)

    mainFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=900, height=700, bg='white')
    mainFrame.place(x=535, y=200)

    mainFrame2 = Frame(mainScreen, bd=3, relief=SUNKEN, width=899, height=50, bg='white')
    mainFrame2.place(x=535, y=150)


    moveDownButton = Button(mainFrame2, text="Move down", command=moveDown)
    moveDownButton.place(x=20, y=0)

    moveUpButton = Button(mainFrame2, text="Move up", command=moveUp)
    moveUpButton.place(x=140, y=0)

    removeFunc = Button(mainFrame2, text="Remove Function", command=removeFunctions)
    removeFunc.place(x=240, y=0)

    insertB = Button(mainFrame2, text="Insert Below", command=insert_B)
    insertB.place(x=410, y=0)

    insertA = Button(mainFrame2, text="Insert Above", command=insert_A)
    insertA.place(x=550, y=0)

    takeScreenShot = Button(mainFrame2, text="Take Screen Shot", command=window2, state=DISABLED)
    takeScreenShot.place(x=690, y=0)

    # funFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=450, height=400, bg='white')
    # funFrame.place(x=1455, y=150)

    photoViewFrame = Frame(mainScreen, bd=3, relief=SUNKEN, width=450, height=350, bg='white', name='photoViewFrame')
    photoViewFrame.place(x=1455, y=600)

    Lb1 = Listbox(mainScreen, width=45, height=11, exportselection=0)
    for x in range(0, len(functionList)):
        Lb1.insert(x, functionList[x])

    Lb1.place(x=1450, y=150)
    Lb1.config(state=DISABLED)




    Lb2 = Listbox(mainFrame, width=78, height=25, font=("Ariel", 10), exportselection=0, selectmode=EXTENDED)
    Lb2.pack(side="left", fill="y" )

    scrollbar = Scrollbar(mainFrame, orient="vertical")
    scrollbar.config(command=Lb2.yview)
    scrollbar.pack(side="right", fill="y")

    Lb2.config(yscrollcommand=scrollbar.set)

    AutoSave = ttk.Combobox(toolbarFrame,values=[
                                                "No AutoSave",
                                                "Every 10 Min",
                                                ],
                                                state="readonly"
                            )
    AutoSave.bind('<<ComboboxSelected>>', lambda event: comboBoxSelect(event))
    AutoSave.place(x=mainScreen.winfo_width()-300,y=0)
    AutoSave.current(0)

    reportFrame()


    Lb2.bind("<<ListboxSelect>>", func=FocusOnSelectedFunc)
    Lb2.bind("<FocusOut>", func=disableTakeScreenShot)

    tree = createTree(explorerFrame)
    tree.bind("<Double-1>", TreeviewD_Click)

    mainScreen.protocol("WM_DELETE_WINDOW", on_closing)


mainScreen.mainloop()
