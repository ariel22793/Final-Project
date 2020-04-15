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
import numpy as np

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

functionList = ['Right-Click','Left-Click','Repeat','If-Exist','If-Not-Exist','Else', 'Double-Click','Insert-Input', 'Sleep']
currentScript = None
firstTime = True
process = []

# def updateCurrentScript(index,delta):
#     fromIndex = 0
#     toIndex = 0
#
#     for i in range(len(currentScript.functions)): #run on all the functions
#         if(i>toIndex):
#             if(currentScript.functions[i].father[0] > index):
#                 fromIndex = currentScript.linesFather[currentScript.functions[i].father[0] + delta].fromIndex
#                 toIndex = currentScript.linesFather[currentScript.functions[i].father[0] + delta].toIndex
#             else:
#                 fromIndex = currentScript.linesFather[currentScript.functions[i].father[0]].fromIndex
#                 toIndex = currentScript.linesFather[currentScript.functions[i].father[0]].toIndex
#
#         # change fromIndex and toIndex for complex function
#         if (currentScript.functions[i].name == 'Repeat' or currentScript.functions[i].name == 'If-Exist' or currentScript.functions[i].name == 'If-Not-Exist' or currentScript.functions[i].name == 'Else' ):
#             fromIndex = i
#             toIndex = i + len(currentScript.functions[i].extra.functions) + 2
#
#         #if the function have father
#         if currentScript.functions[i].father != '' and (currentScript.functions[i].father[1] == 'Repeat' or currentScript.functions[i].father[1] == 'If-Exist' or currentScript.functions[i].father[1] == 'If-Not-Exist' or currentScript.functions[i].father[1] == 'Else'):
#             if(i != fromIndex and currentScript.functions[i].name != '{' and currentScript.functions[i].name != '}'): #if is not the head function
#                 try:
#                     if (currentScript.functions[i].father[0] > index ):
#                         currentScript.functions[currentScript.functions[i].father[0] + delta].extra.functions[i - fromIndex - 2].id = i
#                     else:
#                         currentScript.functions[currentScript.functions[i].father[0]].extra.functions[i - fromIndex - 2].id = i
#                 except:
#                     print('index:{} , extra:{} , extra index:{}'.format(currentScript.functions[i].father[0],currentScript.functions[currentScript.functions[i].father[0]].extra,i - fromIndex - 2))
#
#             currentScript.functions[i].id = i
#             currentScript.linesFather[i].fromIndex = fromIndex
#             currentScript.linesFather[i].toIndex = toIndex
#             if (currentScript.functions[i].father[0] > index): # if the father of the function is after the insert function the so the father increase in delta times
#                 currentScript.functions[i].father = (currentScript.functions[i].father[0] + delta, currentScript.functions[i].father[1])
#             else:
#                 currentScript.functions[i].father = (
#                     currentScript.functions[i].father[0], currentScript.functions[i].father[1])
#
#         else: #if the function dont have father
#             currentScript.functions[i].id = i
#             currentScript.functions[i].father= (i,currentScript.functions[i].father[1])
#             currentScript.linesFather[i].fromIndex = i
#             currentScript.linesFather[i].toIndex = i

def updateCurrentScript(index,delta):
    fromIndex = 0
    toIndex = 0
    currentIndex = -1
    for i in range(len(currentScript.functions)):#run on all the functions

        if(i > currentIndex and currentScript.functions[i].indention == 0 and currentScript.functions[i].name != '{' and currentScript.functions[i].name != '}'):
            currentScript.functions[i].id = i
            currentScript.functions[i].father = (i,currentScript.functions[i].father[1])

            if (currentScript.functions[i].name == 'Repeat' or currentScript.functions[i].name == 'If-Exist' or
                    currentScript.functions[i].name == 'If-Not-Exist' or currentScript.functions[i].name == 'Else'):
                currentScript.linesFather[i].fromIndex = i
                currentScript.linesFather[i].toIndex = i + len(currentScript.functions[i].extra.functions) + 2
                currentIndex = currentScript.functions[i].extra.updateFunction(index, delta, currentScript, i)
            else:
                currentScript.linesFather[i].fromIndex = i
                currentScript.linesFather[i].toIndex = i





def updateLb2():
    index = Lb2.curselection()

    Lb2.delete(0, 'end')
    for x in range(0, len(currentScript.functions)):
        name = currentScript.functions[x].name
        shift = ' ' * currentScript.functions[x].indention * 5
        if name == 'Sleep' or name == 'Repeat':
            Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.time))
        elif name == 'If-Exist' or name == 'If-Not-Exist':
            Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.image))
        else:
            Lb2.insert(x, shift + name)
    try:
        Lb2.get(index)
    except:
        pass


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

            currentFunction = Function(functionName, '', place, rightSectionFrame, '',
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
            currentFunction = Function(functionName, '', place, rightSectionFrame,'',
                                       (currentLineFather.fromIndex, functionName), sleep)
            currentLineFather = LineFather(place, place, functionName)
        currentFunction.getInputBox(currentFunction.extra, currentFunction.frame.children.get('label'), currentFunction.frame.children.get('input'), Sleep.changeSleepTime,Lb2,currentScript)
    elif functionName == 'Repeat':
        delta = 3
        repeat = Repeat('?', [Function('', '', place +2 , rightSectionFrame,'',(place, functionName), '')])
        tempFunction = ['{', '', '}']

        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))

            currentFunction = Function(functionName, '', place, rightSectionFrame,'',(currentLineFather.fromIndex, currentLineFather.fatherName), repeat,currentScript.functions[currentLineFather.fromIndex].indention +1)

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
                    if(tempFunction[i - (place + 1)] == ''):
                        tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame,'', (place, functionName), '',tempIndention+1)
                    else:
                        tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                            (place, functionName), '', tempIndention)
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
            currentFunction = Function(functionName, '', place, rightSectionFrame,'',
                                       (currentLineFather.fromIndex, functionName), repeat)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame,'',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)
        currentFunction.getInputBox(currentFunction.extra, currentFunction.frame.children.get('label'), currentFunction.frame.children.get('input'), Repeat.changeRepeatTime,Lb2,currentScript)
    elif functionName == 'If-Exist':
        delta = 3
        ifExist = IfExist('?', [Function('', '', place +2 , rightSectionFrame,'',(place, functionName), '')])
        tempFunction = ['{', '', '}']

        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, rightSectionFrame,'',(currentLineFather.fromIndex, currentLineFather.fatherName), ifExist,currentScript.functions[currentLineFather.fromIndex].indention +1)

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
                    if (tempFunction[i - (place + 1)] == ''):
                        tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                            (place, functionName), '', tempIndention + 1)
                    else:
                        tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                            (place, functionName), '', tempIndention)
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
            currentFunction = Function(functionName, '', place, rightSectionFrame,'',
                                       (currentLineFather.fromIndex, functionName), ifExist)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame,'',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)

    elif functionName == 'If-Not-Exist':
        delta = 3
        ifNotExist = IfNotExist('?', [Function('', '', place + 2, rightSectionFrame,'', (place, functionName), '')])
        tempFunction = ['{', '', '}']

        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

            for i in range(place, place + 4, 1):
                if i == place:
                    currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                              currentScript.linesFather[i].toIndex,
                                                              currentScript.linesFather[i].fatherName)
                else:
                    currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
            currentFunction = Function(functionName, '', place, rightSectionFrame,'',
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
                    if (tempFunction[i - (place + 1)] == ''):
                        tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                            (place, functionName), '', tempIndention + 1)
                    else:
                        tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                            (place, functionName), '', tempIndention)
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
            currentFunction = Function(functionName, '', place, rightSectionFrame,'',
                                       (currentLineFather.fromIndex, functionName), ifNotExist)
            for i in range(place + 1, place + 4):
                currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame,'',
                                                           (place, functionName), ''))
            currentLineFather = LineFather(place, place + 3, functionName)
    elif functionName == 'Else':
        if place == 0 or (currentScript.functions[place-1].father[1] != 'If-Exist' and currentScript.functions[place-1].father[1] != 'If-Not-Exist'):
            popupmsg('cannot use Else function without ifExist or ifNotExist')
        else:
            delta = 3
            elseObj = Else([Function('', '', place +2 , rightSectionFrame,'',(place, functionName), '')])
            tempFunction = ['{', '', '}']

            if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:

                for i in range(place, place + 4, 1):
                    if i == place:
                        currentScript.linesFather[i] = LineFather(currentScript.linesFather[i].fromIndex,
                                                                  currentScript.linesFather[i].toIndex,
                                                                  currentScript.linesFather[i].fatherName)
                    else:
                        currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))
                currentFunction = Function(functionName, '', place, rightSectionFrame,'',(currentLineFather.fromIndex, currentLineFather.fatherName), elseObj,currentScript.functions[currentLineFather.fromIndex].indention +1)

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
                        if (tempFunction[i - (place + 1)] == ''):
                            tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                                (place, functionName), '', tempIndention + 1)
                        else:
                            tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                                (place, functionName), '', tempIndention)
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
                currentFunction = Function(functionName, '', place, rightSectionFrame,'',
                                           (currentLineFather.fromIndex, functionName), elseObj)
                for i in range(place + 1, place + 4):
                    currentScript.functions.insert(i, Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame,'',
                                                               (place, functionName), ''))
                currentLineFather = LineFather(place, place + 3, functionName)
    else:
        if (currentLineFather.fatherName == 'Repeat' or currentLineFather.fatherName == 'If-Exist' or currentLineFather.fatherName == 'If-Not-Exist' or currentLineFather.fatherName == 'Else') and currentLineFather.fromIndex != place:
            currentFunction = Function(functionName, '', place, rightSectionFrame,'',
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
            currentFunction = Function(functionName, '', place, rightSectionFrame,'', (currentLineFather.fromIndex, functionName), '')
            currentLineFather = LineFather(place, place, functionName)

    currentScript.functions[place] = currentFunction
    currentScript.linesFather[place] = currentLineFather
    updateCurrentScript(place,delta)
    updateLb2()
    Lb2.select_set(place)
    FocusOnSelectedFunc(None)
    # Lb2.selection_clear(0, END)
    # Lb1.selection_clear(0, END)


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


def checkMarkArea(indexes):
    firstIndex = indexes[0]
    lastIndex = indexes[len(indexes)-1]
    markFlag = True
    message = ''

    if(currentScript.functions[firstIndex].name == '{' or currentScript.functions[firstIndex].name == '}'):
        message += "cannot start the mark from { or }"
        markFlag = False
    if(currentScript.functions[firstIndex].indention != currentScript.functions[lastIndex].indention):
        message += "functions are not complete"
        markFlag = False
    if (currentScript.functions[lastIndex].name == 'Repeat' or currentScript.functions[lastIndex].name == 'If-Exist' or
                        currentScript.functions[lastIndex].name == 'If-Not-Exist' or currentScript.functions[lastIndex].name == 'Else'):
        message += "cannot End the mark with complex function"
        markFlag = False
    if(markFlag == False):
        popupmsg(message)
    return markFlag


def removeFunctions():
    delta = 0
    indexes = []
    currentIndex = -1
    for x in Lb2.curselection():
        indexes.append(x)
    flag = checkMarkArea(indexes)
    if(flag == True):
        for index in indexes[::-1]:
            if(currentScript.functions[index].indention == currentScript.functions[0].indention and currentScript.functions[index].name != '}' and currentScript.functions[index].name != '{'):
                removeFuncFatherIndex = index
                haveFather = False

                if currentScript.functions[index].father != (index,currentScript.functions[index].name):
                    haveFather = True
                    removeFuncFatherIndex = currentScript.linesFather[currentScript.functions[index].father[0]].fromIndex

                # if(currentScript.functions[index].name =='{' or currentScript.functions[index].name =='}' ):
                #     msgbox = tkinter.messagebox.showerror('Notic!', 'You cant remove this, this is not a function.')


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
    window2 = ScreenShotWindow(mainScreen,Lb2,currentScript,tree,photoViewFrame)


def SUBS(path, parent, tree):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        # tree.image = fileImg

        if os.path.isdir(abspath):
            parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")
            SUBS(abspath, parent_element, tree)
        else:
            parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")


def disableMoveDown(index,functionsLen,functionName):
    if (currentScript.functions[index].indention > 0):  # if the function is a child

        fatherLinesFather = currentScript.linesFather[currentScript.functions[index].father[0]]
        fatherFuncLen = len(currentScript.functions[currentScript.functions[index].father[0]].extra.functions)

        if (functionName == 'Repeat' or functionName == 'If-Exist' or functionName == 'If-Not-Exist' or functionName == 'Else'):
            if (currentScript.linesFather[index].toIndex + 1 == currentScript.linesFather[currentScript.functions[index].father[0]].toIndex):
                moveDownButton.config(state=DISABLED)
            else:
                moveDownButton.config(state=NORMAL)
        else:
            if (fatherFuncLen == index - fatherLinesFather.fromIndex-1):
                moveDownButton.config(state=DISABLED)
            else:
                moveDownButton.config(state=NORMAL)
    else:
        if (currentScript.linesFather[index].toIndex == functionsLen - 1):
            moveDownButton.config(state=DISABLED)
        else:
            moveDownButton.config(state=NORMAL)





def disableMoveUp(index,functionsLen,functionName):
    if (currentScript.functions[index].indention > 0):  # if the function is a child

        fatherLinesFather = currentScript.linesFather[currentScript.functions[index].father[0]]
        fatherFuncLen = len(currentScript.functions[currentScript.functions[index].father[0]].extra.functions)

        if (index - fatherLinesFather.fromIndex - 2 == 0):
            moveUpButton.config(state=DISABLED)
        else:
            moveUpButton.config(state=NORMAL)
    else:
        if (index == 0):
            moveUpButton.config(state=DISABLED)
        else:
            moveUpButton.config(state=NORMAL)



def disableMoveUpAndDown(index):
    functionsLen = len(currentScript.functions)
    functionName = currentScript.functions[index].name

    if(functionsLen <= 1 or functionName == '{' or functionName == '}' or functionName == ''): #if the number of functions is less then 2
        moveDownButton.config(state=DISABLED)
        moveUpButton.config(state=DISABLED)
    else:
        disableMoveDown(index,functionsLen,functionName)
        disableMoveUp(index,functionsLen,functionName)


def disableRemoveFunction(index):
    functionName = currentScript.functions[index].name
    if(functionName == '{' or functionName == '}' or functionName == '' ):
        removeFunc.config(state=DISABLED)
    else:
        removeFunc.config(state=NORMAL)


def disableInsertAboveAndBelow(index):
    functionName = currentScript.functions[index].name
    if(functionName == '{'):
        insertA.config(state=DISABLED)
    else:
        insertA.config(state=NORMAL)
    if(functionName == 'Repeat' or functionName == 'If-Exist' or functionName == 'If-Not-Exist' or functionName == 'Else'):
        insertB.config(state=DISABLED)
    else:
        insertB.config(state=NORMAL)


def disableScreeShot(index):
    functionName = currentScript.functions[index].name
    if (functionName == '{' or functionName == '}' or functionName == '' or functionName == 'Repeat' or functionName == 'Sleep' or functionName == 'Else'):
        # takeScreenShot.config(state=DISABLED)
        takeS_flag[0]='takeSDis'
        change_on_hover('event', takeS_flag[0], canvasTakeS, takeS)
    else:
        # takeScreenShot.config(state=NORMAL)
        takeS_flag[0]='takeS'
        change_on_hover('event', takeS_flag[0], canvasTakeS, takeS)



def disableAddFunction(index):
    functionName = currentScript.functions[index].name

    if(functionName == ''):
        # addFunc.config(state=NORMAL)
        add_func_flag[0]='AddFunc'
        change_on_hover('event',add_func_flag[0],canvasAddFun,addFunc)
    else:
        # addFunc.config(state=DISABLED)
        add_func_flag[0] = 'AddFuncDis'
        change_on_hover('event', add_func_flag[0], canvasAddFun, addFunc)

def disableButtons(index):
    disableMoveUpAndDown(index)
    disableRemoveFunction(index)
    disableInsertAboveAndBelow(index)
    disableScreeShot(index)
    disableAddFunction(index)


def FocusOnSelectedFunc(event):

    # takeScreenShot.config(state='normal')
    takeS_flag[0] = 'takeS'
    change_on_hover('event', takeS_flag[0], canvasTakeS, takeS)
    Lb1.config(state='normal')
    # addFunc.config(state='normal')
    add_func_flag[0] = 'AddFunc'
    change_on_hover('event', add_func_flag[0], canvasAddFun, addFunc)
    mainScreen.update_idletasks()
    # mainScreen.update()

    try:
        index = Lb2.curselection()[0]
    except:
        return

    disableButtons(index)

    frame = ''
    id = index
    photoName = ''
    functionName = ''    # repoFrame_and_Button[0].destroy()

    x = currentScript.functions[index]
    try:
        if(x.img != ''):
            photoName = x.img.img
        functionName = x.name
    except:
        pass
    frame = x.frame
    if frame != '':
        frame.grid(row=1, column=0, sticky='NEWS')
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
        try:
            frame.refresh()
        except:
            pass
    reportFrame()

def disableTakeScreenShot(event):
    # takeScreenShot.config(state=DISABLED)
    takeS_flag[0] = 'takeSDis'
    change_on_hover('event', takeS_flag[0], canvasTakeS, takeS)

def createTree(frame):
    tree = ttk.Treeview(frame)
    s = ttk.Style()
    s.theme_use("alt")
    s.configure('Treeview', rowheight=30, font=(None, 8), background = "#2b2b2b", fieldbackground="#2b2b2b", foreground="white")

    tree.grid(row = 0,column = 0,sticky = 'WE')

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    vsb.grid(row=0,column=1,sticky = 'NS')
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    hsb.grid(row=1, column=0, sticky='EW')
    tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)

    frame.update_idletasks()
    tree.column("#0", width=frame.winfo_reqwidth(), stretch=True, anchor='c')
    tree.heading("#0", text="Project Files View")

    return tree


def moveUp():
    index = Lb2.curselection()[0]
    tempFunctions = []
    tempLineFather = []

#################### get move function range################################
    if (currentScript.functions[index].name == 'Repeat' or currentScript.functions[index].name == 'If-Exist' or
            currentScript.functions[index].name == 'If-Not-Exist' or currentScript.functions[
                index].name == 'Else'):
        fromIndexToMove = index
        toIndexToMove = index + len(currentScript.functions[index].extra.functions) + 2
    else:
        fromIndexToMove = index
        toIndexToMove = index
#############################################################################

#################### get Upper function top function#########################
    if (currentScript.functions[index-1].name == '}'):
        fromIndexUpperFunc = currentScript.functions[index-1].father[0]
    else:
        fromIndexUpperFunc = index-1
#############################################################################

    numberOfFunctionToMove = toIndexToMove - fromIndexToMove +1

    for funcIndex in range(toIndexToMove,fromIndexToMove-1,-1): # save and remove the function that we want to move in tempFunction
        tempFunctions.insert(0,currentScript.functions[funcIndex])
        tempLineFather.insert(0,currentScript.linesFather[funcIndex])
        currentScript.functions.pop(funcIndex)
        currentScript.linesFather.pop(funcIndex)

    tempFuncIndex = 0
    for funcIndex in range(fromIndexUpperFunc,fromIndexUpperFunc + numberOfFunctionToMove):
        currentScript.functions.insert(funcIndex,tempFunctions[tempFuncIndex])
        currentScript.linesFather.insert(funcIndex,tempLineFather[tempFuncIndex])
        tempFuncIndex += 1

    updateCurrentScript(index,0)
    updateLb2()
    Lb2.select_set(fromIndexUpperFunc)


def moveDown():
    index = Lb2.curselection()[0]
    tempFunctions = []
    tempLineFather = []

    #################### get move function range################################
    if (currentScript.functions[index].name == 'Repeat' or currentScript.functions[index].name == 'If-Exist' or
            currentScript.functions[index].name == 'If-Not-Exist' or currentScript.functions[
                index].name == 'Else'):
        fromIndexToMove = index
        toIndexToMove = index + len(currentScript.functions[index].extra.functions) + 2
    else:
        fromIndexToMove = index
        toIndexToMove = index
    #############################################################################

    #################### get bottom function top function#########################
    if (currentScript.functions[toIndexToMove+1].name == 'Repeat' or currentScript.functions[toIndexToMove+1].name == 'If-Exist' or
                        currentScript.functions[toIndexToMove+1].name == 'If-Not-Exist' or currentScript.functions[toIndexToMove+1].name == 'Else'):
        toIndexBottomFunc = currentScript.linesFather[toIndexToMove +1].toIndex
    else:
        toIndexBottomFunc = toIndexToMove + 1
    #############################################################################

    numberOfFunctionToMove = toIndexToMove - fromIndexToMove + 1

    for funcIndex in range(toIndexToMove, fromIndexToMove - 1,-1):  # save and remove the function that we want to move in tempFunction
        tempFunctions.insert(0, currentScript.functions[funcIndex])
        tempLineFather.insert(0, currentScript.linesFather[funcIndex])
        currentScript.functions.pop(funcIndex)
        currentScript.linesFather.pop(funcIndex)

    tempFuncIndex = 0
    for funcIndex in range(toIndexBottomFunc, toIndexBottomFunc + numberOfFunctionToMove):
        currentScript.functions.insert(funcIndex, tempFunctions[tempFuncIndex])
        currentScript.linesFather.insert(funcIndex, tempLineFather[tempFuncIndex])
        tempFuncIndex += 1

    updateCurrentScript(index, 0)
    updateLb2()
    Lb2.select_set(toIndexBottomFunc)


# def listReload(list):
#     list.delete(0, 'end')
#     for x in range(0, len(currentScript.functions)):
#         Lb2.insert(x, currentScript.functions[x].name)
#         Lb2.pack(side="left", fill="y")
#         # Lb2.place(x=0, y=40)


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
            block.append({'name': x.name, 'img': imgdict, 'id': str(x.id),'frameFather':'', 'frame': '', 'fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                          'extra': x.extra.getDict(),'indention':x.indention})
        else:
            block.append({'name': x.name, 'img': imgdict, 'id': str(x.id),'frameFather':'', 'frame': '', 'fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                          'extra': '','indention':x.indention})
    return block


def saveLinesFather():
    block = []
    for x in currentScript.linesFather:
        block.append({'fatherName':x.fatherName,'fromIndex':x.fromIndex,'toIndex':x.toIndex})
    return block


def saveHundle():
    functionPath = currentScript.path + "/functions.json"
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
        func = Function('','','', rightSectionFrame,'','','')
        inputFunctions.append(func.getFunction(x,Lb2,currentScript,tempFunction,rightSectionFrame))
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
    scriptPath = os.path.split(os.path.split(currentScript.path)[0])[0]
    fullPath =''
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
    path = scriptPath + '\\' + fullPath
    if(os.path.isdir(path)):
        path += '\\'
    with open(path) as json_file:
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
    currentScript.functions.insert(place, Function('', '', place, rightSectionFrame,'', '', '',currentScript.functions[place+1].indention))
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
            currentScript.functions[fromIndex].extra.functions.insert(place - fromIndex - 2, Function('', '', place, rightSectionFrame,'', (
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
                                                                          Function('', '', place, rightSectionFrame,'', (
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
    currentScript.functions.insert(place, Function('', '', place, rightSectionFrame,'', '', '',currentScript.functions[place-1].indention))
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
        currentScript.functions[fromIndex].extra.functions.insert(place - fromIndex - 2, Function('', '', place, rightSectionFrame,'', (
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


        # functionsblock = saveFunctions()
        # linesFatherblock = saveLinesFather()

        root = tree.insert('', 'end', text=fileName, open=True, tag='T')
        SUBS(label+'/'+fileName, root, tree)


        FocusOnSelectedFunc(None)

        updateLb2()


    insert_A()
    functionsblock = saveFunctions()
    linesFatherblock = saveLinesFather()
    with open(functionPath, 'w+') as outfile:
        outfile.write(json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))
    Lb2.select_set(0)
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
        folder_path = os.path.split(filePath)[0]
        file_name = os.path.split(folder_path)[1]
        root = tree.insert('', 'end', text=file_name, open=True, tag='T')
        SUBS(folder_path, root, tree)

        mainScreen.deiconify()
        mainScreen.state("zoomed")

        if(len(currentScript.functions)<=1):
            Lb2.select_set(0)
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
        canvas.a = Button1
        canvas.itemconfig(item, image=Button1)

    if(number==2):
        Button1 = PhotoImage(file=r"img\buttonNPHover.png")
        canvas.b = Button1
        canvas.itemconfig(item, image = Button1)
    if(number==3):
        Button1 = PhotoImage(file=r"img\buttonLoadHover.png")
        canvas.c = Button1
        canvas.itemconfig(item, image = Button1)

    if(number==4):
        Button1 = PhotoImage(file=r"img\buttonCloseHover.png")
        canvas.d = Button1
        canvas.itemconfig(item, image = Button1)

    if (number == 5):

        Button1 = PhotoImage(file=r"img\buttonPaNHover.png")
        canvas.e = Button1
        canvas.itemconfig(item, image=Button1)

    if (number == 6):
        Button1 = PhotoImage(file=r"img\buttonReturnHover.png")
        canvas.f = Button1
        canvas.itemconfig(item, image=Button1)

def hoverOff(event,canvas, item, number):
    if (number == 1):
        Button1 = PhotoImage(file=r"img\buttonStart.png")
        canvas.a = Button1
        canvas.itemconfig(item, image=Button1)

    if (number == 2):
        Button1 = PhotoImage(file=r"img\buttonNP.png")
        canvas.b = Button1
        canvas.itemconfig(item, image=Button1)

    if (number == 3):
        Button1 = PhotoImage(file=r"img\buttonLoad.png")
        canvas.c = Button1
        canvas.itemconfig(item, image=Button1)

    if(number==4):
        closeButton1 = PhotoImage(file=r"img\buttonClose.png")
        canvas.d = closeButton1
        canvas.itemconfig(item, image=closeButton1)
    if (number == 5):
        Button1 = PhotoImage(file=r"img\buttonPaN.png")
        canvas.e = Button1
        canvas.itemconfig(item, image=Button1)
    if (number == 6):
        Button1 = PhotoImage(file=r"img\buttonReturn.png")
        canvas.f = Button1
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



def autosave(arg):

        countThread = process[0]

        flag =0
        if('No' in arg):
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

def comboBoxSelect(arg):
    try:
        for x in process:
           x._is_stopped = True
           time.sleep(1)

           x._is_stopped = False

    except:
        print('in exept')

    process.clear()
    saver = threading.Thread(target=autosave, args=(arg,))
    process.append(saver)

    saver.start()



def on_closing():
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            for x in process:
                x._is_stopped = True
            mainScreen.destroy()



def Treeview_right_click(event):
    tree.selection_set(tree.identify_row(event.y))
    item = tree.identify("item", event.x, event.y)

    item_iid = tree.selection()[0]
    parent_iid = tree.parent(item_iid)
    node = tree.item(parent_iid)['text']
    path = currentScript.path[0:-1] +'/' + node +'/' + tree.item(item)["text"]

    if '.png' in tree.item(item)["text"]:
        menu = Menu(explorerFrame, tearoff=0, bg='#3c3f41', fg='white')
        menu.add_command(label="Change Name", command = lambda: changeName(item_iid,tree.item(item)["text"], path))
        menu.add_command(label="Preview", command = lambda: image_preview(path))
        menu.add_command(label="Delete Photo", command = lambda: deletePhoto(path, item_iid))
        menu.post(event.x_root, event.y_root)
def deletePhoto(path,iid):
    if tkinter.messagebox.askokcancel("Delete", "Are you sure you want to delete this file?\nThis will keep the function if exist but without the image"):
        os.remove(path)
        tree.delete(iid)
def changeName(iid, fileName, path):
    bbox = tree.bbox(iid)
    x = bbox[0]
    y = bbox[1]

    entry = Entry(explorerFrame, borderwidth=2, relief="groove")
    entry.insert(END, fileName)
    entry.place(x=x+30,y=y)
    entry.focus()
    entry.bind('<FocusOut>', lambda event: out(entry,fileName, iid, path))
    entry.bind('<Return>', lambda event: out(entry,fileName, iid, path))
    entry.bind('<Escape>', lambda event: out(entry,fileName, iid, path))

def out(entry,fileName, iid, path):
    new_name = entry.get()
    entry.destroy()
    tree.item(iid, text=new_name)
    new_path = path[0:path.rfind('/')]+'/' + new_name
    os.rename(path, new_path)
    for x in currentScript.functions:
        if x.img.img == fileName:
            x.img.img = new_name



def image_preview(filePath):
    r = Toplevel()
    my_image = PhotoImage(file=filePath, master=mainScreen)
    canvas_image = my_image.zoom(2, 2)

    canvas = Canvas(r, height=my_image.width()+100, width=my_image.height()+100)
    canvas.pack()

    canvas.create_image(0, 0, anchor=NW, image=canvas_image)

    r.mainloop()



def drag_and_drop(event,pointers,selection_index, canvasGoust, flag):
    selection = Lb1.get(selection_index)
    for child in canvasGoust.winfo_children():
        child.destroy()

    if flag[0]=='empty':
        flag[0] = selection
        flag[1] = selection_index
        name_of_fun = Label(canvasGoust, text=selection, fg='white', bg='black')
        print(selection_index)
        Lb1.select_set(selection_index)
    else:
        name_of_fun = Label(canvasGoust, text=flag[0], fg='white', bg='black' )
        Lb1.select_set(flag[1])

    name_of_fun.pack()

    canvasGoust.place(x=pointers[0]-30, y=pointers[1]-50)


def drop(event, canvasGoust, flag ):

    for child in canvasGoust.winfo_children():
        child.destroy()
    background = PhotoImage(file=r"img\transparent.png")
    canvasGoust.bg = background
    canvasGoust.create_image(0, 0, image=background)
    # canvasGoust.pack()
    canvasGoust.place(x=10000000, y=1000000000)
    flag[0]='empty'

    pointerX, pointerY = event.x_root,event.y_root
    if(pointerX>= Lb2.winfo_rootx() and pointerX<= Lb2.winfo_rootx()+ Lb2.winfo_width() and pointerY>=Lb2.winfo_rooty() and pointerY<= Lb2.winfo_rooty()+ Lb2.winfo_height()) :
        addFunction()

def change_on_hover(event, name, canvas, item):
    try:
        if 'Dis' in name:
            filename = "img\\" + name + ".png"
            Button1 = PhotoImage(file=filename)
            canvas.a = Button1
            canvas.itemconfig(item, image=Button1)
            return
    except:
        pass
    if 'Hover' in name:
        filename = "img\\" +  name[0:name.rfind('Hover')] + ".png"
    else:
        filename = "img\\" + name + "Hover.png"
    Button1 = PhotoImage(file=filename)
    canvas.a = Button1
    canvas.itemconfig(item, image=Button1)

def combobox_save(comboFlag,x,y):
    if comboFlag[0] =='0':
        menu = Menu(explorerFrame, tearoff=0, bg='#3c3f41', fg='white')
        menu.add_command(label="No Auto Save", command = lambda: comboBoxSelect('No_Auto'))
        menu.add_command(label="Auto Save", command = lambda: comboBoxSelect('Auto'))
        menu.post(x+20, y+35)
        comboFlag[0]='1'
    else:
        comboFlag[0]='0'
        pass




if __name__ == '__main__':
    functionFather = []

    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.configure(background='#3c3f41')

    # mainScreen.title("MyApp")
    # mainScreen.overrideredirect(True)
    mainScreen.columnconfigure(0,weight = 1)
    mainScreen.columnconfigure(1,weight = 2)
    mainScreen.columnconfigure(2,weight = 1)
    mainScreen.rowconfigure(0,weight = 1)
    mainScreen.rowconfigure(1,weight = 1)
    mainScreen.rowconfigure(2,weight = 30)

    if firstTime :
        startScreen()

    toolbarFrame = Frame(mainScreen, bd=3, bg='#3c3f41')
    toolbarFrame.grid(sticky = 'WEN')

    openToolButton = PhotoImage(file=r"img\OpenTool.png")
    canvasOpen = Canvas(toolbarFrame,height = openToolButton.height(),width = openToolButton.width(),  bg='#3c3f41', bd=-2)
    canvasOpen.grid(row=0,column=0, sticky="N", pady=2)

    canvasOpen.open = openToolButton
    openTool = canvasOpen.create_image(-1, -1, anchor=NW, image=openToolButton, tags="openTool")

    canvasOpen.tag_bind('openTool', '<Button-1>', lambda event:openButton())
    canvasOpen.tag_bind('openTool', '<Enter>', lambda event: change_on_hover(event,"openTool",canvasOpen,openTool))
    canvasOpen.tag_bind('openTool', '<Leave>', lambda event: change_on_hover(event,"openToolHover",canvasOpen,openTool))

    # openButton = Button(toolbarFrame, text="Open", command=openButton)
    # openButton.grid(row=0,column=0,padx = 7, pady = 7)


    saveToolButton = PhotoImage(file=r"img\SaveTool.png")
    canvasSave = Canvas(toolbarFrame, height=saveToolButton.height(), width=saveToolButton.width(), bg='#3c3f41', bd=-2)
    canvasSave.grid(row=0, column=1, sticky="N", pady=2)

    canvasSave.save = saveToolButton
    saveTool = canvasSave.create_image(-1, -1, anchor=NW, image=saveToolButton, tags="SaveTool")

    canvasSave.tag_bind('SaveTool', '<Button-1>', lambda event: saveHundle())
    canvasSave.tag_bind('SaveTool', '<Enter>', lambda event: change_on_hover(event, "SaveTool", canvasSave, saveTool))
    canvasSave.tag_bind('SaveTool', '<Leave>',lambda event: change_on_hover(event, "SaveToolHover", canvasSave, saveTool))

    # saveButton = Button(toolbarFrame, text="Save", command=saveHundle,)
    # saveButton.grid(row=0, column=1,padx = 7, pady = 7)

    saveAsToolButton = PhotoImage(file=r"img\SaveAsTool.png")
    canvasSaveAs = Canvas(toolbarFrame, height=saveAsToolButton.height(), width=saveAsToolButton.width(), bg='#3c3f41', bd=-2)
    canvasSaveAs.grid(row=0, column=2, sticky="N", pady=2)

    canvasSaveAs.save = saveToolButton
    saveAsTool = canvasSaveAs.create_image(-1, -1, anchor=NW, image=saveAsToolButton, tags="SaveAsTool")

    canvasSaveAs.tag_bind('SaveAsTool', '<Button-1>', lambda event: saveAsHundle())
    canvasSaveAs.tag_bind('SaveAsTool', '<Enter>', lambda event: change_on_hover(event, "SaveAsTool", canvasSaveAs, saveAsTool))
    canvasSaveAs.tag_bind('SaveAsTool', '<Leave>', lambda event: change_on_hover(event, "SaveAsToolHover", canvasSaveAs, saveAsTool))

    # saveAsButton = Button(toolbarFrame, text="Save As", command=saveAsHundle)
    # saveAsButton.grid(row=0, column=2,padx = 7, pady = 7)

    playToolButton = PhotoImage(file=r"img\PlayTool.png")
    canvasPlay = Canvas(mainScreen, height=playToolButton.height(), width=playToolButton.width(), bg='#3c3f41',bd=-2)
    canvasPlay.grid(row=0, column=1, sticky="N", pady=4)

    canvasPlay.play = playToolButton
    playTool = canvasPlay.create_image(0, 0, anchor=NW, image=playToolButton, tags="PlayTool")

    canvasPlay.tag_bind('PlayTool', '<Button-1>', lambda event: runHendle())
    canvasPlay.tag_bind('PlayTool', '<Enter>', lambda event: change_on_hover(event, "PlayTool", canvasPlay, playTool))
    canvasPlay.tag_bind('PlayTool', '<Leave>', lambda event: change_on_hover(event, "PlayToolHover", canvasPlay, playTool))

    # photo = PhotoImage(file=r"img\start2.png")
    # photoimage = photo.subsample(3, 3)
    # runButton = Button(mainScreen, text="Run", command=runHendle, image = photoimage)
    # runButton.grid(row=0, column=1,padx = 7, pady = 7,sticky='N')

    comboToolButton = PhotoImage(file=r"img\Combo.png")
    canvasCombo = Canvas(mainScreen, height=comboToolButton.height(), width=comboToolButton.width(), bg='#3c3f41', bd=-2)
    canvasCombo.grid(row=0, column=2, sticky="N", pady=4)

    canvasCombo.combo = comboToolButton
    combo = canvasCombo.create_image(0, 0, anchor=NW, image=comboToolButton, tags="Combo")
    comboFlag=['0']
    canvasCombo.tag_bind('Combo', '<Button-1>', lambda event: combobox_save(comboFlag,canvasCombo.winfo_rootx(),canvasCombo.winfo_rooty()))
    canvasCombo.tag_bind('Combo', '<Enter>', lambda event: change_on_hover(event, "Combo",canvasCombo , combo))
    canvasCombo.tag_bind('Combo', '<Leave>', lambda event: change_on_hover(event, "ComboHover", canvasCombo, combo))

    # AutoSave = ttk.Combobox(mainScreen, values=[
    #     "No AutoSave",
    #     "Every 10 Min",
    # ],
    #                         state="readonly" )
    # AutoSave.bind('<<ComboboxSelected>>', lambda event: comboBoxSelect(event))
    # AutoSave.grid(row=0, column=2, sticky='N', padx=7, pady=7)
    # AutoSave.current(0)

    line_style = ttk.Style()
    line_style.configure("Line.TSeparator", background="black")
    separator = ttk.Separator(mainScreen, orient='horizontal', style="Line.TSeparator")
    separator.grid(column=0, row=0, sticky="WE", pady=35)

    separator2 = ttk.Separator(mainScreen, orient='horizontal', style="Line.TSeparator")
    separator2.grid(column=1, row=0, sticky="WE", pady=35)

    separator3 = ttk.Separator(mainScreen, orient='horizontal', style="Line.TSeparator")
    separator3.grid(column=2, row=0, sticky="WE", pady=35)

    addFunclButton = PhotoImage(file=r"img\AddFuncDis.png")
    canvasAddFun = Canvas(mainScreen, height=addFunclButton.height(), width=addFunclButton.width(), bg='#3c3f41', bd=-2)
    canvasAddFun.grid(row=1, column=2, sticky="N", pady=4)

    canvasAddFun.addFun = addFunclButton
    addFunc = canvasAddFun.create_image(0, 0, anchor=NW, image=addFunclButton, tags="AddFunc")
    add_func_flag=['AddFuncDis']
    # canvasAddFun.tag_bind('AddFunc', '<Button-1>',lambda event: addFunction())
    canvasAddFun.tag_bind('AddFunc', '<Enter>', lambda event: change_on_hover(event, add_func_flag[0], canvasAddFun, addFunc))
    canvasAddFun.tag_bind('AddFunc', '<Leave>', lambda event: change_on_hover(event, add_func_flag[0]+'Hover', canvasAddFun, addFunc))
    # addFunc = Button(mainScreen, text="Add Functions", command=addFunction, state=DISABLED)
    # addFunc.grid(row=1,column = 2,sticky='N')

    # mainSectionFrame = Frame(mainScreen)
    # mainSectionFrame.columnconfigure(0, weight = 2)
    # mainSectionFrame.columnconfigure(1, weight = 1)
    # mainSectionFrame.columnconfigure(2, weight = 2)
    # mainSectionFrame.rowconfigure(0, weight = 1)
    # mainSectionFrame.grid(row = 2, column=0,sticky = 'WESN')

    leftSectionFrame = Frame(mainScreen)
    leftSectionFrame.columnconfigure(0, weight=1)
    leftSectionFrame.rowconfigure(0, weight=1)
    leftSectionFrame.grid(row=2, column=0,sticky='NWE',padx = 10,pady=(0,55))

    explorerFrame = Frame(leftSectionFrame, bd=3, relief=SUNKEN)
    explorerFrame.columnconfigure(0,weight=1)
    explorerFrame.rowconfigure(0,weight=1)
    explorerFrame.grid(row=0,column=0,sticky='NWE')

    centerSectionFrame = Frame(mainScreen)
    centerSectionFrame.columnconfigure(0, weight=1)
    centerSectionFrame.rowconfigure(0, weight=1)
    centerSectionFrame.rowconfigure(1, weight=30)
    centerSectionFrame.grid(row=2,column=1,sticky='NWES',padx = 50)

    mainFrame1 = Frame(centerSectionFrame,bd = 3, relief=SUNKEN, bg='#3c3f41')
    mainFrame1.grid(row=0, column=0,sticky='N')

    Lb2Fframe = Frame(centerSectionFrame, relief=SUNKEN)
    Lb2Fframe.columnconfigure(0,weight=1)
    Lb2Fframe.rowconfigure(0,weight=1)
    Lb2Fframe.grid(row=1, column=0, sticky='NSWE',pady=(0,55))

    yScroll = Scrollbar(Lb2Fframe, orient=VERTICAL)
    yScroll.grid(row=0, column=1, sticky='NS')

    xScroll = Scrollbar(Lb2Fframe, orient=HORIZONTAL)
    xScroll.grid(row=1, column=0, sticky='EW')

    Lb2 = Listbox(Lb2Fframe,xscrollcommand=xScroll.set,yscrollcommand=yScroll.set,selectmode=EXTENDED)
    Lb2.grid(row=0, column=0, sticky='NSWE')
    xScroll['command'] = Lb2.xview
    yScroll['command'] = Lb2.yview

    rightSectionFrame = Frame(mainScreen, relief=SUNKEN, background="#3c3f41")
    rightSectionFrame.columnconfigure(0,weight=1)
    rightSectionFrame.rowconfigure(0,weight=1)
    rightSectionFrame.rowconfigure(1,weight=4)
    rightSectionFrame.grid(row=2,column=2,sticky='NWES',padx =(0,10),pady=(0,55))
    # s = ttk.Style()
    # s.theme_use("alt")
    # s.configure('Treeview', rowheight=30, font=(None, 8), background="#2b2b2b", fieldbackground="#2b2b2b",
    #             foreground="white")
    Lb1 = Listbox(rightSectionFrame, exportselection=0, selectmode = SINGLE, bd=3,  background="#2b2b2b", fg='white')
    Lb1.grid(row=0, column=0, sticky='NEW')
    for x in range(0, len(functionList)):
        Lb1.insert(x, functionList[x])
    Lb1.config(state=DISABLED)
    flag_for_drag_and_drop = ["empty", 0]

    canvasGoust = Canvas(mainScreen)
    Lb1.bind('<B1-Motion>', lambda event: drag_and_drop(event,mainScreen.winfo_pointerxy(), Lb1.curselection()[0], canvasGoust, flag_for_drag_and_drop))
    Lb1.bind('<ButtonRelease-1>', lambda event:drop(event, canvasGoust, flag_for_drag_and_drop))

    photoViewFrame = Frame(rightSectionFrame, bd=3, relief=SUNKEN, bg='white', name='photoViewFrame')
    photoViewFrame.grid(row=1, column=0,sticky='NEWS')

    moveDownButton = PhotoImage(file=r"img\moveDown.png")
    canvasmoveDown = Canvas(mainFrame1, height=moveDownButton.height(), width=moveDownButton.width(), bg='#3c3f41', bd=-2)
    canvasmoveDown.grid(row=0, column=0, sticky="N", pady=4)

    canvasmoveDown.moveDown = moveDownButton
    moveDown = canvasmoveDown.create_image(0, 0, anchor=NW, image=moveDownButton, tags="moveDown")

    canvasmoveDown.tag_bind('moveDown', '<Button-1>', lambda event: moveDown())
    canvasmoveDown.tag_bind('moveDown', '<Enter>', lambda event: change_on_hover(event, "moveDown", canvasmoveDown, moveDown))
    canvasmoveDown.tag_bind('moveDown', '<Leave>', lambda event: change_on_hover(event, "moveDownHover", canvasmoveDown, moveDown))
    #
    # moveDownButton = Button(mainFrame1, text="Move down", command=moveDown)
    # moveDownButton.grid(row=0, column=0, padx=10)

    moveUpButton = PhotoImage(file=r"img\moveUp.png")
    canvasmoveUp = Canvas(mainFrame1, height=moveUpButton.height(), width=moveUpButton.width(), bg='#3c3f41', bd=-2)
    canvasmoveUp.grid(row=0, column=1, sticky="N", pady=4)

    canvasmoveUp.moveUp = moveUpButton
    moveUp = canvasmoveUp.create_image(0, 0, anchor=NW, image=moveUpButton, tags="moveUp")

    canvasmoveUp.tag_bind('moveUp', '<Button-1>',lambda event: moveUp())
    canvasmoveUp.tag_bind('moveUp', '<Enter>', lambda event: change_on_hover(event, "moveUp", canvasmoveUp, moveUp))
    canvasmoveUp.tag_bind('moveUp', '<Leave>', lambda event: change_on_hover(event, "moveUpHover", canvasmoveUp, moveUp))

    # moveUpButton = Button(mainFrame1, text="Move up", command=moveUp)
    # moveUpButton.grid(row=0, column=1, padx=10)

    removeButton = PhotoImage(file=r"img\remove.png")
    canvasRemove = Canvas(mainFrame1, height=removeButton.height(), width=removeButton.width(), bg='#3c3f41', bd=-2)
    canvasRemove.grid(row=0, column=2, sticky="N", pady=4)

    canvasRemove.remove = removeButton
    remove_b = canvasRemove.create_image(0, 0, anchor=NW, image=removeButton, tags="remove")

    canvasRemove.tag_bind('remove', '<Button-1>', lambda event: removeFunctions())
    canvasRemove.tag_bind('remove', '<Enter>', lambda event: change_on_hover(event, "remove", canvasRemove, remove_b))
    canvasRemove.tag_bind('remove', '<Leave>', lambda event: change_on_hover(event, "removeHover", canvasRemove, remove_b))

    # removeFunc = Button(mainFrame1, text="Remove Function", command=removeFunctions)
    # removeFunc.grid(row=0, column=2, padx=10)

    insertBButton = PhotoImage(file=r"img\insertB.png")
    canvasinsertB = Canvas(mainFrame1, height=insertBButton.height(), width=insertBButton.width(), bg='#3c3f41', bd=-2)
    canvasinsertB.grid(row=0, column=3, sticky="N", pady=4)

    canvasinsertB.insertb = insertBButton
    insertB= canvasinsertB.create_image(0, 0, anchor=NW, image=insertBButton, tags="insertB")

    canvasinsertB.tag_bind('insertB', '<Button-1>', lambda event: insert_B())
    canvasinsertB.tag_bind('insertB', '<Enter>', lambda event: change_on_hover(event, "insertB", canvasinsertB, insertB))
    canvasinsertB.tag_bind('insertB', '<Leave>',lambda event: change_on_hover(event, "insertBHover", canvasinsertB, insertB))

    # insertB = Button(mainFrame1, text="Insert Below", command=insert_B)
    # insertB.grid(row=0, column=3, padx=10)

    insertAButton = PhotoImage(file=r"img\insertA.png")
    canvasinsertA = Canvas(mainFrame1, height=insertAButton.height(), width=insertAButton.width(), bg='#3c3f41', bd=-2)
    canvasinsertA.grid(row=0, column=4, sticky="N", pady=4)
    canvasinsertA.insertb = insertAButton
    insertA = canvasinsertA.create_image(0, 0, anchor=NW, image=insertAButton, tags="insertA")
    canvasinsertA.tag_bind('insertA', '<Button-1>', lambda event: insert_A())
    canvasinsertA.tag_bind('insertA', '<Enter>', lambda event: change_on_hover(event, "insertA", canvasinsertA, insertA))
    canvasinsertA.tag_bind('insertA', '<Leave>', lambda event: change_on_hover(event, "insertAHover", canvasinsertA, insertA))

    # insertA = Button(mainFrame1, text="Insert Above", command=insert_A)
    # insertA.grid(row=0, column=4, padx=10)

    takeSButton = PhotoImage(file=r"img\TakeSDis.png")
    canvasTakeS = Canvas(mainFrame1, height=takeSButton.height(), width=takeSButton.width(), bg='#3c3f41', bd=-2)
    canvasTakeS.grid(row=0, column=5, sticky="N", pady=4)
    canvasTakeS.takeS = takeSButton
    takeS_flag = ['takeSDis']
    takeS = canvasTakeS.create_image(0, 0, anchor=NW, image=takeSButton, tags="takeS")
    # canvasTakeS.tag_bind('takeS', '<Button-1>', lambda event: window2())
    canvasTakeS.tag_bind('takeS', '<Enter>', lambda event: change_on_hover(event, takeS_flag[0] , canvasTakeS, takeS))
    canvasTakeS.tag_bind('takeS', '<Leave>', lambda event: change_on_hover(event, takeS_flag[0], canvasTakeS, takeS))

    # takeScreenShot = Button(mainFrame1, text="Take Screen Shot", command=window2, state=DISABLED)
    # takeScreenShot.grid(row=0, column=5, padx=10)

    reportFrame()


    Lb2.bind("<<ListboxSelect>>", func=FocusOnSelectedFunc)
    Lb2.bind("<FocusOut>", func=disableTakeScreenShot)

    tree = createTree(explorerFrame)

    # tree.bind("<Double-1>", TreeviewD_Click)
    tree.bind("<Button-3>", Treeview_right_click)

    mainScreen.protocol("WM_DELETE_WINDOW", on_closing)


mainScreen.mainloop()
