from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font as tkFont
import pyautogui
import PIL
from PIL import Image
import tkinter.ttk as ttk
import os
import json
import matplotlib.pyplot as plt
from keyboard import on_press
from pynput import keyboard
import pyautogui
import ImgRecog
from time import sleep
from Logger import Logger
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
import InsertInput
from InsertInput import InsertInput
import Scan_Text_Compare
from Scan_Text_Compare import Scan_Text_Compare
import ScanText
import Photo
import LineFather
from LineFather import LineFather
import Function
from Function import Function
from win32api import GetSystemMetrics
import threading
from datetime import datetime
from pynput.keyboard import Key, Listener
import numpy as np
from EmailSender import EmailSender
import traceback

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

functionList = ['Right-Click','Left-Click','Repeat','If-Exist','If-Not-Exist','Else', 'Double-Click','Insert-Input', 'Sleep','Exit','Hover']
currentScript = None
firstTime = True
process = []
copyFunction = []
copyLineFather = []
redoFunctions = []
undoFunctions = []
redoLinesFather = []
undoLinesFather = []
stopScript = False
Lb1Colors = ['#f4b63f','#57ceff' , '#ff5792', '#c2ff57','#ff8657','#579aff','#d557ff','#078f02','#57ff7f','white','white']
flag_of_shift = False
speed=1
logger = None
lastClickOnLb2 = 0
lb2NumberOfRows = 0
waitBeforeImageProcess = 0.4
Emails = None

def updateRedoFunctions(type = 'regular'):
    if(logger != None):
        logger.writeToLog('updateRedoFunctions function')
    try:
        if((type != 'A' and type != 'B') or len(currentScript.functions) == 1):
            numberOfRedo = 20
            functionsblock = saveFunctions()
            linesFatherblock = saveLinesFather()

            if(len(redoFunctions) == numberOfRedo):
                redoFunctions.insert(len(redoFunctions),functionsblock)
                redoFunctions.pop(0)
                redoLinesFather.insert(len(redoLinesFather),linesFatherblock)
                redoLinesFather.pop(0)
            else:
                redoFunctions.append(functionsblock)
                redoLinesFather.append(linesFatherblock)
    except Exception as e:
        exeptionHandler(e)

def updateUndoFunctions(redoIndex):
    if (logger != None):
        logger.writeToLog('updateUndoFunctions function')
    try:
        numberOfUndo = 20
        functionsblock = copy.deepcopy(redoFunctions[redoIndex])
        linesFatherblock = copy.deepcopy(redoLinesFather[redoIndex])

        if(len(undoFunctions) == numberOfUndo):
            undoFunctions.insert(len(undoFunctions),functionsblock)
            undoFunctions.pop(0)
            undoLinesFather.insert(len(undoLinesFather),linesFatherblock)
            undoLinesFather.pop(0)
        else:
            undoFunctions.append(functionsblock)
            undoLinesFather.append(linesFatherblock)
    except Exception as e:
        print(traceback.format_exc())
        exeptionHandler(e)

def updateCurrentScript(type = 'regular'):
    if (logger != None):
        logger.writeToLog('updateCurrentScript function')
    try:
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
                    currentIndex = currentScript.functions[i].extra.updateFunction(currentScript, i)
                else:
                    currentScript.linesFather[i].fromIndex = i
                    currentScript.linesFather[i].toIndex = i
        updateRedoFunctions(type)
    except Exception as e:
        exeptionHandler(e)


def getFunctionColor(funcName):
    try:
        if(funcName == 'Right-Click'):
            return Lb1Colors[0]
        elif(funcName == 'Left-Click'):
            return Lb1Colors[1]
        elif (funcName == 'Repeat'):
            return Lb1Colors[2]
        elif (funcName == 'If-Exist'):
            return Lb1Colors[3]
        elif (funcName == 'If-Not-Exist'):
            return Lb1Colors[4]
        elif (funcName == 'Else'):
            return Lb1Colors[5]
        elif (funcName == 'Double-Click'):
            return Lb1Colors[6]
        elif (funcName == 'Insert-Input'):
            return Lb1Colors[7]
        elif (funcName == 'Sleep'):
            return Lb1Colors[8]
        elif (funcName == 'Exit'):
            return Lb1Colors[9]
        elif (funcName == 'Move-To'):
            return Lb1Colors[10]
        else:
            return 'white'
    except Exception as e:
        exeptionHandler(e)


def updateLb2Indexes(difference,lb2IndexesLength):
    if (logger != None):
        logger.writeToLog('updateLb2Indexes function')
    try:
        lb2Indexes.config(state=NORMAL)
        if(difference<0):
            for i in range(lb2IndexesLength, lb2IndexesLength + difference-1,-1):
                lb2Indexes.delete(i)
        else:
            for i in range(lb2IndexesLength,lb2IndexesLength+difference):
                lb2Indexes.insert(END, str(i+1))
                lb2Indexes.itemconfig(i, foreground='white')
        lb2Indexes.config(state=DISABLED)
    except Exception as e:
        exeptionHandler(e)

def updateLb2(fromIndex,toIndex,operation,options = 'regular',functionsSize = 0,fatherIndex = 0,childrenSize=0):
    if (logger != None):
        logger.writeToLog('updateLb2 function')
    try:
        vw = Lb2.yview()
        if(options == 'deleteBefore'):
            Lb2.delete(0, 'end')
        highestNumDigit = len(str(len(currentScript.functions)))
        lb2IndexesLength = lb2Indexes.size()
        if(len(currentScript.functions) != lb2IndexesLength):
            updateLb2Indexes(len(currentScript.functions) - lb2IndexesLength ,lb2IndexesLength)
        if (operation == 'add' or operation == 'replace' ):
            for x in range(fromIndex, toIndex+1):
                textColor = getFunctionColor(currentScript.functions[x].name)
                currentNumDigit = len(str(x))
                if(operation == 'add'):
                    updateLb2Add(currentNumDigit, fromIndex, highestNumDigit, options, textColor, x)
                elif (operation == 'replace'):
                    updateLb2Replace(currentNumDigit, highestNumDigit, textColor, x)
            Lb2.update()
        elif(operation == 'remove'):
            updateLb2Remove(childrenSize, fatherIndex, fromIndex, functionsSize, toIndex)
            Lb2.update()
        Lb2.yview_moveto(vw[0])
    except Exception as e:
        exeptionHandler(e)


def updateLb2Remove(childrenSize, fatherIndex, fromIndex, functionsSize, toIndex):
    for x in range(toIndex, fromIndex - 1, -1):
        Lb2.delete(x)
    if (childrenSize == (toIndex - fromIndex) + 1):
        shift = ' ' * currentScript.functions[fatherIndex + 2].indention * 5
        Lb2.insert(fatherIndex + 2, shift + '')
        Lb2.itemconfig(fatherIndex + 2, foreground='white')
    elif (functionsSize == (toIndex - fromIndex) + 1):
        shift = ' ' * currentScript.functions[0].indention * 5
        Lb2.insert(0, shift + '')
        Lb2.itemconfig(0, foreground='white')


def updateLb2Replace(currentNumDigit, highestNumDigit, textColor, x):
    name = currentScript.functions[x].name
    shift = ' ' * currentScript.functions[x].indention * 5
    tabFromNumber = ' ' * (5 + (highestNumDigit - currentNumDigit))
    Lb2.delete(x)
    if name == 'Sleep' or name == 'Repeat':
        Lb2.insert(x, shift + name + '({})'.format(
            currentScript.functions[x].extra.time))
        Lb2.itemconfig(x, foreground=textColor)
    elif name == 'If-Exist' or name == 'If-Not-Exist':
        if currentScript.functions[x].extra.compareState == 'text':
            Lb2.insert(x, shift + name + '({},{})'.format(currentScript.functions[x].extra.image,
                                                          currentScript.functions[x].extra.text))
        else:
            Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.image))
        Lb2.itemconfig(x, foreground=textColor)
    elif name == 'Insert-Input' or name == 'Scan Text & Compare':
        Lb2.insert(x, + name + '("{}")'.format(
            currentScript.functions[x].extra.text))
        Lb2.itemconfig(x, foreground=textColor)
    else:
        Lb2.insert(x, shift + name)
        Lb2.itemconfig(x, foreground=textColor)


def updateLb2Add(currentNumDigit, fromIndex, highestNumDigit, options, textColor, x):
    name = currentScript.functions[x].name
    shift = ' ' * currentScript.functions[x].indention * 5
    tabFromNumber = ' ' * (5 + (highestNumDigit - currentNumDigit))
    if (x == fromIndex and options != 'A' and options != 'B'):
        Lb2.delete(x)
    if name == 'Sleep' or name == 'Repeat':
        Lb2.insert(x, shift + name + '({})'.format(
            currentScript.functions[x].extra.time))
        Lb2.itemconfig(x, foreground=textColor)
    elif name == 'If-Exist' or name == 'If-Not-Exist':
        if currentScript.functions[x].extra.compareState == 'text':
            Lb2.insert(x, shift + name + '("{}","{}")'.format(currentScript.functions[x].extra.image,
                                                              currentScript.functions[x].extra.text))
        else:
            Lb2.insert(x, shift + name + '("{}")'.format(currentScript.functions[x].extra.image))
        Lb2.itemconfig(x, foreground=textColor)
    elif name == 'Insert-Input' or name == 'Scan Text & Compare':
        Lb2.insert(x, shift + name + '("{}")'.format(
            currentScript.functions[x].extra.text))
        Lb2.itemconfig(x, foreground=textColor)
    else:
        Lb2.insert(x, shift + name)
        Lb2.itemconfig(x, foreground=textColor)


def addEmptyFunc(lastFuncIndex,firstFuncIndex):
    functions = currentScript.functions
    if lastFuncIndex+1 == len(functions) or (functions[lastFuncIndex].indention > 0
        and len(functions[functions[firstFuncIndex].father[0]].extra.functions) == lastFuncIndex - functions[firstFuncIndex].father[0] -1):
        insert_B(lastFuncIndex+1,False)
        return True
    return False


def getExtraObject(functionName, place, currentLineFather):
    if functionName == 'Repeat':
        return Repeat('?', [
            Function('', '', place + 2, rightSectionFrame, '', (place, functionName), '', currentScript, tree, Lb2,
                     photoViewFrame, currentScript.functions[currentLineFather.fromIndex].indention + 2)])

    elif functionName == 'If-Exist':
        return IfExist('?', 'image', '', [
            Function('', '', place + 2, rightSectionFrame, '', (place, functionName), '', currentScript, tree, Lb2,
                     photoViewFrame, currentScript.functions[currentLineFather.fromIndex].indention + 2)])

    elif functionName == 'If-Not-Exist':
        return IfNotExist('?', 'image', '', [
            Function('', '', place + 2, rightSectionFrame, '', (place, functionName), '', currentScript, tree, Lb2,
                     photoViewFrame, currentScript.functions[currentLineFather.fromIndex].indention + 2)])

    elif functionName == 'Else':
        return Else([Function('', '', place + 2, rightSectionFrame, '', (place, functionName), '', currentScript,
                                 tree, Lb2, photoViewFrame,
                                 currentScript.functions[currentLineFather.fromIndex].indention + 2)])

    elif functionName == 'Insert-Input':
        return InsertInput('')

    elif functionName == 'Sleep':
        return Sleep('?')


def getInputChangeObject(functionName,extra):
    if functionName == 'Repeat':
        return extra
    elif functionName == 'If-Exist':
        return extra
    elif functionName == 'If-Not-Exist':
        return extra
    elif functionName == 'Else':
        return extra
    elif functionName == 'Insert-Input':
        return extra.changeInsertInputText
    elif functionName == 'Sleep':
        return extra.changeSleepTime


def addFunction(place = 0,functionName = 'None',flag = True):
    if (logger != None):
        logger.writeToLog('addFunction function')
    try:
        if 'Dis' in add_func_flag[0]:
            return
        if(flag == True):
            place = Lb2.curselection()[0]
            functionName = functionList[Lb1.curselection()[0]]
            logger.writeToLog('add {} function'.format(functionName))
        fromIndex = place
        toIndex = place

        try:
            currentLineFather = currentScript.linesFather[place]
        except:
            if(currentScript.functions==[] and place ==0):      ## case that this is the first time we add a function
                print('first time!')

        if functionName == 'Insert-Input' or functionName == 'Sleep':
            currentFunction, currentLineFather = createSimpleFuncWithExtra(currentLineFather, functionName, place)
        elif isComplexFuncByName(functionName):
            currentFunction, toIndex = createComplexFunction(currentLineFather, functionName, place,toIndex)
        else:
            currentFunction, currentLineFather = createSimpleFuncWithoutExtra(currentLineFather, functionName, place)

        currentScript.functions[place] = currentFunction
        lastFuncIndex = place
        if isComplexFuncByIndex(place):
            lastFuncIndex = place + 3
        updateCurrentScript()
        addOrNot = addEmptyFunc(lastFuncIndex,place)
        if addOrNot == False:
            pass
        else:
            toIndex+=1
        updateLb2(fromIndex,toIndex,'add')
        selectLb2Index(place)
        FocusOnSelectedFunc(None)
    except Exception as e:
        exeptionHandler(e)


def createSimpleFuncWithoutExtra(currentLineFather, functionName, place):
    if isComplexFuncByName(currentLineFather.fatherName) and currentLineFather.fromIndex != place:
        currentFunction = Function(functionName, '', place, rightSectionFrame, '',
                                   (currentLineFather.fromIndex, currentLineFather.fatherName), '', currentScript, tree,
                                   Lb2, photoViewFrame,
                                   currentScript.functions[currentLineFather.fromIndex].indention + 1)
        currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                       currentLineFather.fatherName)
        UpdateFathers(currentFunction, currentLineFather, place)
    else:
        currentFunction = Function(functionName, '', place, rightSectionFrame, '',
                                   (currentLineFather.fromIndex, functionName), '', currentScript, tree, Lb2,
                                   photoViewFrame)
        currentLineFather = LineFather(place, place, functionName)
    return currentFunction, currentLineFather


def createComplexFunction(currentLineFather, functionName, place, toIndex):
    toIndex = place + 3
    extra = getExtraObject(functionName, place, currentLineFather)
    tempFunction = ['{', '', '}']
    if isComplexFuncByName(currentLineFather.fatherName) and currentLineFather.fromIndex != place:
        updateLineFatherWithFathers(functionName, place)
        currentFunction = Function(functionName, '', place, rightSectionFrame, '',
                                   (currentLineFather.fromIndex, currentLineFather.fatherName), extra, currentScript,
                                   tree, Lb2, photoViewFrame,
                                   currentScript.functions[currentLineFather.fromIndex].indention + 1)
        updateComplexFathers(currentFunction, currentLineFather, functionName, place, tempFunction)
    else:
        updateLineFatherWithoutFathers(functionName, place)
        currentFunction = Function(functionName, '', place, rightSectionFrame, '',
                                   (currentLineFather.fromIndex, functionName), extra, currentScript, tree, Lb2,
                                   photoViewFrame)
        updateComplexFunctionWithoutFahters(functionName, place, tempFunction)
    changeObject = getInputChangeObject(functionName, extra)
    currentFunction.getInputBox(currentFunction.name, currentFunction.extra,
                                currentFunction.frame.children.get('labelAndInput'), changeObject, Lb2, currentScript)
    return currentFunction, toIndex


def createSimpleFuncWithExtra(currentLineFather, functionName, place):
    extra = getExtraObject(functionName, place, currentLineFather)
    if (isComplexFuncByName(currentLineFather.fatherName)) and currentLineFather.fromIndex != place:
        currentFunction = Function(functionName, '', place, rightSectionFrame, '',
                                   (currentLineFather.fromIndex, currentLineFather.fatherName), extra, currentScript,
                                   tree, Lb2, photoViewFrame,
                                   currentScript.functions[currentLineFather.fromIndex].indention + 1)
        currentLineFather = LineFather(currentLineFather.fromIndex, currentLineFather.toIndex,
                                       currentLineFather.fatherName)
        UpdateFathers(currentFunction, currentLineFather, place)
    else:
        currentFunction = Function(functionName, '', place, rightSectionFrame, '',
                                   (currentLineFather.fromIndex, functionName), extra, currentScript, tree, Lb2,
                                   photoViewFrame)
        currentLineFather = LineFather(place, place, functionName)
    changeObject = getInputChangeObject(functionName, extra)
    currentFunction.getInputBox(currentFunction.name, currentFunction.extra,
                                currentFunction.frame.children.get('labelAndInput'), changeObject, Lb2, currentScript)
    return currentFunction, currentLineFather


def updateComplexFunctionWithoutFahters(functionName, place, tempFunction):
    for i in range(place + 1, place + 4):
        if (tempFunction[i - (place + 1)] == ''):
            currentScript.functions.insert(i,
                                           Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                                    (place, functionName), '', currentScript, tree, Lb2, photoViewFrame,
                                                    1))
        else:
            currentScript.functions.insert(i,
                                           Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                                    (place, functionName), '', currentScript, tree, Lb2,
                                                    photoViewFrame))


def updateLineFatherWithoutFathers(functionName, place):
    for i in range(place, place + 4, 1):
        if (i == place):
            currentScript.linesFather[i] = LineFather(place, place + 3, functionName)
        else:
            currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))


def updateComplexFathers(currentFunction, currentLineFather, functionName, place, tempFunction):
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
                tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '', (place, functionName),
                                    '', currentScript, tree, Lb2, photoViewFrame, tempIndention + 1)
            else:
                tempFunc = Function(tempFunction[i - (place + 1)], '', i, rightSectionFrame, '',
                                    (place, functionName), '', currentScript, tree, Lb2, photoViewFrame, tempIndention)
            if tempFatherFunction.father[0] == tempFatherFunction.id:
                currentScript.functions.insert(i, tempFunc)
            tempFatherFunction.extra.functions.insert(i - tempLineFather.fromIndex - 2, tempFunc)
        if tempFatherFunction.father[0] == tempFatherFunction.id:
            break
        tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
        tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]


def updateLineFatherWithFathers(functionName, place):
    for i in range(place, place + 4, 1):
        if i == place:
            currentScript.linesFather[i] =  LineFather(place, place + 3, functionName)
        else:
            currentScript.linesFather.insert(i, LineFather(place, place + 3, functionName))


def UpdateFathers(currentFunction, currentLineFather, place):
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


def checkMarkArea(indexes):
    try:
        firstFunction = currentScript.functions[indexes[0]]
        lastFunction = currentScript.functions[indexes[len(indexes)-1]]

        markFlag = True
        message = ''

        for index in indexes:
            if currentScript.functions[index].indention < firstFunction.indention:
                markFlag = False
                message += "You Marked Wrong Area\n"
                break;

        if(firstFunction.name == '{' or firstFunction.name == '}'):
            message += "cannot start the mark from { or }\n"
            markFlag = False
        if(firstFunction.indention != lastFunction.indention):
            message += "functions are not complete\n"
            markFlag = False
        if (lastFunction.name == '{' ):
            message += "Cannot end the mark with { \n"
            markFlag = False
        if (lastFunction.name == 'Repeat' or lastFunction.name == 'If-Exist' or
                            lastFunction.name == 'If-Not-Exist' or lastFunction.name == 'Else'):
            message += "cannot End the mark with complex function\n"
            markFlag = False
        if(markFlag == False):
            popupmsg(message)
        return markFlag
    except Exception as e:
        exeptionHandler(e)

def findNextFunc(index):
    for i in range(index+1,len(currentScript.functions)):
        if(currentScript.functions[index].indention == currentScript.functions[i].indention and currentScript.functions[i].name != '{' and currentScript.functions[i].name != '}'  ):
            return currentScript.functions[i]

def removeFunctions():
    if (logger != None):
        logger.writeToLog('removeFunctions function')
    try:
        if 'Dis' in remove_flag[0]:
            return
        delta = 0
        indexes = []
        currentIndex = -1
        for x in Lb2.curselection():
            indexes.append(x)
            logger.writeToLog('remove {} function'.format(currentScript.functions[x].name))
        fromIndex = indexes[0]
        toIndex = indexes[len(indexes)-1]
        flag = checkMarkArea(indexes)
        if(flag == True):
            firstIndexIndention = currentScript.functions[indexes[0]].indention
            fatherIndex = currentScript.functions[indexes[0]].father[0]
            functionsSize = len(currentScript.functions)
            childrenSize = 0
            if(firstIndexIndention > 0 and currentScript.functions[fatherIndex].extra != ''):
                childrenSize = len(currentScript.functions[fatherIndex].extra.functions)


            for index in indexes[::-1]:
                if(currentScript.functions[index].indention == currentScript.functions[indexes[0]].indention and currentScript.functions[index].name != '}' and currentScript.functions[index].name != '{'):
                    removeFuncFatherIndex = index
                    haveFather = False

                    if currentScript.functions[index].father != (index,currentScript.functions[index].name):
                        haveFather = True
                        removeFuncFatherIndex = currentScript.linesFather[currentScript.functions[index].father[0]].fromIndex

                    popedFunc = currentScript.functions[index]
                    popedFuncName =popedFunc.name
                    if(popedFuncName == 'Repeat'):
                        Repeat.removeRepeat(removeFuncFatherIndex,index,currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                    elif (popedFuncName == 'If-Exist'):
                        tempFunc = findNextFunc(index)
                        if(tempFunc == None or tempFunc.name != 'Else'):
                            IfExist.removeIfExist(removeFuncFatherIndex,index, currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                        else:
                            popupmsg('Canot Remove If-Exist Without the Else function')
                            return
                    elif (popedFuncName == 'If-Not-Exist'):
                        tempFunc = findNextFunc(index)
                        if (tempFunc == None or tempFunc.name != 'Else'):
                            IfNotExist.removeIfNotExist(removeFuncFatherIndex,index, currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                        else:
                            popupmsg('Canot Remove If-Not-Exist Without the Else function')
                            return
                    elif (popedFuncName == 'Else'):
                        Else.removeElse(removeFuncFatherIndex,index, currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                    else:
                        currentScript.functions.pop(index)
                        currentScript.linesFather.pop(index)

                        if haveFather == True:
                            updateFathersByRemoveFunc(fatherIndex, index)
            if(firstIndexIndention != 0 and haveFather and len(currentScript.functions[fatherIndex].extra.functions) == 0):
                insert_B(fatherIndex+2,False)
            if(len(currentScript.functions) == 0):
                insert_B(0, False)
            updateCurrentScript()
            updateLb2(fromIndex,toIndex,'remove','regular',functionsSize,fatherIndex,childrenSize)
            selectLb2Index(fromIndex)
    except Exception as e:
        exeptionHandler(e)


def updateFathersByRemoveFunc(fatherIndex, index):
    tempLineFather = currentScript.linesFather[fatherIndex]
    tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
    while True:
        tempFatherFunction.extra.functions.pop(index - tempLineFather.fromIndex - 2)
        if tempFatherFunction.father[0] == tempFatherFunction.id:
            break
        tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
        tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]


def window2():
    if (logger != None):
        logger.writeToLog('window2 function')
    try:
        global flag_of_shift
        if 'Dis' in takeS_flag[0] or flag_of_shift == False:
            return

        myScreenshot = pyautogui.screenshot()
        bigScreenshotPath = currentScript.path + 'ScreenTest.png'
        myScreenshot.save(bigScreenshotPath)

        window_of_screen_shot = Tk()
        window_of_screen_shot.title("test!")
        window_of_screen_shot.attributes('-fullscreen', True)

        canvas = Canvas(window_of_screen_shot, width=window_of_screen_shot.winfo_screenwidth(), height=window_of_screen_shot.winfo_screenheight(),
                             highlightthickness=0)
        sh = PhotoImage(master=window_of_screen_shot,file=bigScreenshotPath)
        canvas.takeS = sh
        takeS = canvas.create_image(0, 0, anchor=NW, image=sh)
        canvas.pack()
        window2 = ScreenShotWindow(mainScreen,Lb2,currentScript,tree,photoViewFrame,window_of_screen_shot)
        window2.window.attributes("-topmost", True)
        window2.window.mainloop()
        flag_of_shift = False
    except Exception as e:
        exeptionHandler(e)

def SUBS(path, parent, tree):
    try:
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            # tree.image = fileImg
            if os.path.isdir(abspath):
                parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")
                SUBS(abspath, parent_element, tree)
            else:
                parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")
    except Exception as e:
        exeptionHandler(e)


def disableMoveDown(index,functionsLen,functionName):
    try:
        if (currentScript.functions[index].indention > 0):  # if the function is a child

            fatherLinesFather = currentScript.linesFather[currentScript.functions[index].father[0]]
            fatherFuncLen = len(currentScript.functions[currentScript.functions[index].father[0]].extra.functions)

            if (isComplexFuncByName(functionName)):
                if (currentScript.linesFather[index].toIndex + 1 == currentScript.linesFather[currentScript.functions[index].father[0]].toIndex):
                    # moveDownButton.config(state=DISABLED)
                    move_d_flag[0] = 'moveDownDis'
                    change_on_hover('event', move_d_flag[0], canvasmoveDown, moveDown_b)
                else:
                    # moveDownButton.config(state=NORMAL)
                    move_d_flag[0] = 'moveDown'
                    change_on_hover('event', "moveDownHover", canvasmoveDown, moveDown_b)
            else:
                if (fatherFuncLen == index - fatherLinesFather.fromIndex-1):
                    # moveDownButton.config(state=DISABLED)
                    move_d_flag[0] = 'moveDownDis'
                    change_on_hover('event', move_d_flag[0], canvasmoveDown, moveDown_b)
                else:
                    # moveDownButton.config(state=NORMAL)
                    move_d_flag[0] = 'moveDown'
                    change_on_hover('event', "moveDownHover", canvasmoveDown, moveDown_b)
        else:
            if (currentScript.linesFather[index].toIndex == functionsLen - 1):
                # moveDownButton.config(state=DISABLED)
                move_d_flag[0] = 'moveDownDis'
                change_on_hover('event', move_d_flag[0], canvasmoveDown, moveDown_b)
            else:
                # moveDownButton.config(state=NORMAL)
                move_d_flag[0] = 'moveDown'
                change_on_hover('event', "moveDownHover", canvasmoveDown, moveDown_b)
    except Exception as e:
        exeptionHandler(e)




def disableMoveUp(index,functionsLen,functionName):
    try:
        if (currentScript.functions[index].indention > 0):  # if the function is a child

            fatherLinesFather = currentScript.linesFather[currentScript.functions[index].father[0]]
            fatherFuncLen = len(currentScript.functions[currentScript.functions[index].father[0]].extra.functions)

            if (index - fatherLinesFather.fromIndex - 2 == 0):
                # moveUpButton.config(state=DISABLED)
                move_u_flag[0] = 'moveUpDis'
                change_on_hover('event', move_u_flag[0], canvasmoveUp, moveUp_b)
            else:
                # moveUpButton.config(state=NORMAL)
                move_u_flag[0] = 'moveUp'
                change_on_hover('event', 'moveUpHover', canvasmoveUp, moveUp_b)
        else:
            if (index == 0):
                # moveUpButton.config(state=DISABLED)
                move_u_flag[0] = 'moveUpDis'
                change_on_hover('event', move_u_flag[0], canvasmoveUp, moveUp_b)
            else:
                # moveUpButton.config(state=NORMAL)
                move_u_flag[0] = 'moveUp'
                change_on_hover('event', 'moveUpHover', canvasmoveUp, moveUp_b)
    except Exception as e:
        exeptionHandler(e)


def disableMoveUpAndDown(index):
    try:
        functionsLen = len(currentScript.functions)
        functionName = currentScript.functions[index].name

        if(functionsLen <= 1 or functionName == '{' or functionName == '}' or functionName == ''): #if the number of functions is less then 2
            # moveDownButton.config(state=DISABLED)
            # moveUpButton.config(state=DISABLED)
            move_u_flag[0] = 'moveUpDis'
            move_d_flag[0] = 'moveDownDis'
            change_on_hover('event', move_u_flag[0], canvasmoveUp, moveUp_b)
            change_on_hover('event', move_d_flag[0], canvasmoveDown, moveDown_b)
        else:
            disableMoveDown(index,functionsLen,functionName)
            disableMoveUp(index,functionsLen,functionName)
    except Exception as e:
        exeptionHandler(e)


def disableRemoveFunction(index):
    try:
        functionName = currentScript.functions[index].name
        if(functionName == '{' or functionName == '}' or (functionName == '' and len(currentScript.functions) == 1)):
            # removeFunc.config(state=DISABLED)
            remove_flag[0] = 'removeDis'
            change_on_hover('event', remove_flag[0], canvasRemove, remove_b)
        else:
            # removeFunc.config(state=NORMAL)
            remove_flag[0] = 'remove'
            change_on_hover('event', 'removeHover', canvasRemove, remove_b)
    except Exception as e:
        exeptionHandler(e)

def disableInsertAboveAndBelow(index):
    try:
        functionName = currentScript.functions[index].name
        if(functionName == '{'):
            # insertA.config(state=DISABLED)
            insert_a_flag[0] = 'insertADis'
            change_on_hover('event', insert_a_flag[0], canvasinsertA, insertA)
        else:
            # insertA.config(state=NORMAL)
            insert_a_flag[0] = 'insertA'
            change_on_hover('event', 'insertAHover', canvasinsertA, insertA)
        if(isComplexFuncByName(functionName)):
            # insertB.config(state=DISABLED)
            insert_b_flag[0] = 'insertBDis'
            change_on_hover('event', insert_b_flag[0], canvasinsertB, insertB)
        else:
            insert_b_flag[0] = 'insertB'
            change_on_hover('event', 'insertBHover', canvasinsertB, insertB)
    except Exception as e:
        exeptionHandler(e)


def disableScreeShot(index):
    try:
        functionName = currentScript.functions[index].name
        global takeS_flag
        if (functionName == '{' or functionName == '}' or functionName == ''or functionName == 'Repeat' or functionName == 'Exit' or functionName == 'Sleep' or functionName == 'Else'):
            # takeScreenShot.config(state=DISABLED)

            takeS_flag[0]='takeSDis'
            change_on_hover('event', takeS_flag[0], canvasTakeS, takeS)
            pass
        else:
            # takeScreenShot.config(state=NORMAL)
            takeS_flag[0]='takeS'
            change_on_hover('event', 'takeSHover', canvasTakeS, takeS)
    except Exception as e:
        exeptionHandler(e)

def disableAddFunction(index):
    try:
        functionName = currentScript.functions[index].name

        if(functionName == ''):
            # addFunc.config(state=NORMAL)
            add_func_flag[0]='AddFunc'
            change_on_hover('event',add_func_flag[0],canvasAddFun,addFunc)
        else:
            # addFunc.config(state=DISABLED)
            add_func_flag[0] = 'AddFuncDis'
            change_on_hover('event', add_func_flag[0], canvasAddFun, addFunc)
    except Exception as e:
        exeptionHandler(e)

def disableButtons(index):
    try:
        disableMoveUpAndDown(index)
        disableRemoveFunction(index)
        disableInsertAboveAndBelow(index)
        disableScreeShot(index)
        disableAddFunction(index)
    except Exception as e:
        exeptionHandler(e)

def markCurrentFuncArea(index):
    if (logger != None):
        logger.writeToLog('markCurrentFuncArea function')
    try:
        fromindex = currentScript.linesFather[index].fromIndex
        toIndex = currentScript.linesFather[index].toIndex
        for i in range(len(currentScript.functions)):
            tempFunc = currentScript.functions[i]
            if(fromindex <= i <= toIndex):
                if(tempFunc.name == 'Right-Click'):
                    Lb2.itemconfig(i, bg='#f4b63f')
                elif (tempFunc.name == 'Left-Click'):
                    Lb2.itemconfig(i, bg='#57ceff')
                elif (tempFunc.name == 'Repeat' or ((tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '' ) and tempFunc.father[1] == 'Repeat' )):
                    Lb2.itemconfig(i, bg='#ff5792')
                elif (tempFunc.name == 'If-Exist' or ((tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '' ) and tempFunc.father[1] == 'If-Exist' )):
                    Lb2.itemconfig(i, bg='#c2ff57')
                elif (tempFunc.name == 'If-Not-Exist' or (
                                (tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '') and tempFunc.father[1] == 'If-Not-Exist')):
                    Lb2.itemconfig(i, bg='#ff8657')
                elif (tempFunc.name == 'Else' or (
                                (tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '') and tempFunc.father[1] == 'Else')):
                    Lb2.itemconfig(i, bg='#579aff')
                elif (currentScript.functions[i].name == 'Double-Click'):
                    Lb2.itemconfig(i, bg='#d557ff')
                elif (currentScript.functions[i].name == 'Insert-Input'):
                    Lb2.itemconfig(i, bg='#078f02')
                elif (currentScript.functions[i].name == 'Sleep'):
                    Lb2.itemconfig(i, bg='#57ff7f')
            else:
                Lb2.itemconfig(i, bg='#2b2b2b')
    except Exception as e:
        exeptionHandler(e)

def FocusOnSelectedFunc(event):
    if (logger != None):
        logger.writeToLog('FocusOnSelectedFunc function')
    try:
        # takeScreenShot.config(state='normal')
        takeS_flag[0] = 'takeS'
        change_on_hover('event', "takeSHover", canvasTakeS, takeS)
        Lb1.config(state='normal')
        # addFunc.config(state='normal')
        add_func_flag[0] = 'AddFunc'
        change_on_hover('event', add_func_flag[0], canvasAddFun, addFunc)
        mainScreen.update_idletasks()
        # mainScreen.update()
        try:
            index = Lb2.curselection()[0]
            currentScript.lastClickOnLb2 = index
        except:
            return
        photoName = ''
        x = currentScript.functions[index]
        try:
            if(x.img != ''):
                photoName = x.img.img
        except:
            pass
        updateFrame(photoName, x)
        disableButtons(index)
    except Exception as e:
        exeptionHandler(e)


def updateFrame(photoName, x):
    frame = x.frame
    if frame != '':
        frame.grid(row=1, column=0, sticky='NEWS')

        if photoName != '':
            for childName, childValue in frame.children.items():
                if childName == 'fileNameFrame':
                    for childName1, childValue1 in childValue.children.items():
                        if childName1 == 'fileName':
                            childValue1.config(text='File Name: {}'.format(photoName))
                        elif childName1 == 'fileNameButton':
                            childValue1.config(state=NORMAL)
                if childName == 'canvasFrame':
                    canvas = Canvas(childValue, height=150, bg='#2b2b2b', name='canvas')
                    one = PhotoImage(master=mainScreen, file=currentScript.path + "ScreenShots\\" + photoName)
                    photoViewFrame.one = one  # to prevent the image garbage collected.
                    canvas.create_image((0, 0), image=one, anchor="nw")
                    canvas.grid(sticky='NWE')

        frame.tkraise()
        try:
            frame.refresh()
        except:
            pass


def createTree(frame):
        tree = ttk.Treeview(frame)
        s = ttk.Style()
        #s.theme_use("clam")
        s.configure('Treeview', rowheight=30, font=(None, 8), background = "#2b2b2b", fieldbackground="#2b2b2b")

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
    if (logger != None):
        logger.writeToLog('moveUp function')
    try:
        if "Dis" in move_u_flag[0]:
            return
        index = Lb2.curselection()
        if(len(index)>1):
            popupmsg("Cannot Move more than one function at a time")
        else:
            index = index[0]
            if(currentScript.functions[index].name == 'Else' ):
                popupmsg('Cannot Move Up Else Function, It Must Come After If-Exist Or If-Not-Exist')
                return
            tempFunctions = []
            tempLineFather = []
            fromIndexToMove, toIndexToMove = getMoveUpFunctionsRange(index)
            fromIndexUpperFunc = getUpperFunctionRange(index)
            numberOfFunctionToMove = toIndexToMove - fromIndexToMove +1
            removeMoveFunctions(fromIndexToMove, tempFunctions, tempLineFather, toIndexToMove)
            insertMoveUpFunctions(fromIndexUpperFunc, numberOfFunctionToMove, tempFunctions, tempLineFather)

            updateCurrentScript()
            updateLb2(fromIndexUpperFunc,toIndexToMove,'replace')
            selectLb2Index(fromIndexUpperFunc)
    except Exception as e:
        exeptionHandler(e)


def insertMoveUpFunctions(fromIndexUpperFunc, numberOfFunctionToMove, tempFunctions, tempLineFather):
    tempFuncIndex = 0
    for funcIndex in range(fromIndexUpperFunc, fromIndexUpperFunc + numberOfFunctionToMove):
        currentScript.functions.insert(funcIndex, tempFunctions[tempFuncIndex])
        currentScript.linesFather.insert(funcIndex, tempLineFather[tempFuncIndex])
        tempFuncIndex += 1


def removeMoveFunctions(fromIndexToMove, tempFunctions, tempLineFather, toIndexToMove):
    for funcIndex in range(toIndexToMove, fromIndexToMove - 1,
                           -1):  # save and remove the function that we want to move in tempFunction
        tempFunctions.insert(0, currentScript.functions[funcIndex])
        tempLineFather.insert(0, currentScript.linesFather[funcIndex])
        currentScript.functions.pop(funcIndex)
        currentScript.linesFather.pop(funcIndex)



def getUpperFunctionRange(index):
    if (currentScript.functions[index - 1].name == '}'):
        fromIndexUpperFunc = currentScript.functions[index - 1].father[0]
    else:
        fromIndexUpperFunc = index - 1
    return fromIndexUpperFunc


def getMoveUpFunctionsRange(index):
    if (currentScript.functions[index].name == 'Repeat' or currentScript.functions[index].name == 'If-Exist' or
            currentScript.functions[index].name == 'If-Not-Exist' or currentScript.functions[
                index].name == 'Else'):
        fromIndexToMove = index
        toIndexToMove = index + len(currentScript.functions[index].extra.functions) + 2
    else:
        fromIndexToMove = index
        toIndexToMove = index
    return fromIndexToMove, toIndexToMove


def moveDown():
    if (logger != None):
        logger.writeToLog('moveDown function')
    try:
        if 'Dis' in move_d_flag[0]:
            return
        index = Lb2.curselection()
        if (len(index) > 1):
            popupmsg("Cannot Move more than one function at a time")
        else:
            index = index[0]
            if (currentScript.functions[index].name == 'Else'):
                popupmsg('Cannot Move Down Else Function, It Must Come After If-Exist Or If-Not-Exist')
                return
            tempFunctions = []
            tempLineFather = []

            fromIndexToMove, toIndexToMove = getMoveDownFunctionsRange(index)
            toIndexTopFunc = getBottomFunctionsRange(fromIndexToMove, toIndexToMove)
            numberOfFunctionToMove = toIndexToMove - fromIndexToMove + 1
            removeMoveFunctions(fromIndexToMove, tempFunctions, tempLineFather, toIndexToMove)
            insertMoveDownFunctions(numberOfFunctionToMove, tempFunctions, tempLineFather, toIndexTopFunc)
            updateCurrentScript()
            updateLb2(fromIndexToMove,currentScript.linesFather[toIndexTopFunc].toIndex,'replace')

            selectLb2Index(toIndexTopFunc)
    except Exception as e:
        exeptionHandler(e)


def insertMoveDownFunctions(numberOfFunctionToMove, tempFunctions, tempLineFather, toIndexTopFunc):
    tempFuncIndex = 0
    for funcIndex in range(toIndexTopFunc, toIndexTopFunc + numberOfFunctionToMove):
        currentScript.functions.insert(funcIndex, tempFunctions[tempFuncIndex])
        currentScript.linesFather.insert(funcIndex, tempLineFather[tempFuncIndex])
        tempFuncIndex += 1


def getBottomFunctionsRange(fromIndexToMove, toIndexToMove):
    if (currentScript.functions[toIndexToMove + 1].name == 'Repeat' or currentScript.functions[
        toIndexToMove + 1].name == 'If-Exist' or
            currentScript.functions[toIndexToMove + 1].name == 'If-Not-Exist' or currentScript.functions[
                toIndexToMove + 1].name == 'Else'):
        toIndexTopFunc = fromIndexToMove + (
                    currentScript.linesFather[toIndexToMove + 1].toIndex - (toIndexToMove + 1)) + 1
    else:
        toIndexTopFunc = fromIndexToMove + 1
    return toIndexTopFunc


def getMoveDownFunctionsRange(index):
    if (currentScript.functions[index].name == 'Repeat' or currentScript.functions[index].name == 'If-Exist' or
            currentScript.functions[index].name == 'If-Not-Exist' or currentScript.functions[
                index].name == 'Else'):
        fromIndexToMove = index
        toIndexToMove = index + len(currentScript.functions[index].extra.functions) + 2
    else:
        fromIndexToMove = index
        toIndexToMove = index
    return fromIndexToMove, toIndexToMove


def popupmsg(msg):
    try:
        tkinter.messagebox.showinfo('Notice',msg)
    except Exception as e:
        exeptionHandler(e)


def checkImageInFunc():
    if (logger != None):
        logger.writeToLog('checkImageInFunc function')
    try:
        funcWithoutImage = ""
        index = 1
        for func in currentScript.functions:
            if func.name == 'Repeat':
                if func.extra.time == '?':
                    funcWithoutImage += ("The {} in line {} doesn't have repeat time\n".format(func.name, index))
            elif func.name == 'Sleep':
                if func.extra.time == '?':
                    funcWithoutImage += ("The {} in line {} doesn't have sleep time\n".format(func.name, index))
            elif func.name == 'Insert-Input':
                if func.extra.text == '':
                    funcWithoutImage += ("The {} in line {} doesn't have input text\n".format(func.name, index))
                if func.img == '':
                    funcWithoutImage += ("The {} in line {} doesn't have image\n".format(func.name, index))
            elif func.name == 'If-Exist':
                if func.extra.image == '?':
                    funcWithoutImage += ("The {} in line {} doesn't have image\n".format(func.name, index))
                elif func.extra.text == '' and func.extra.compareState == 'text':
                    funcWithoutImage += ("The {} in line {} doesn't have input text\n".format(func.name, index))
            elif func.name == 'If-Not-Exist':
                if func.extra.image == '?':
                    funcWithoutImage += ("The {} in line {} doesn't have image\n".format(func.name, index))
                elif func.extra.text == '' and func.extra.compareState == 'text':
                    funcWithoutImage += ("The {} in line {} doesn't have input text\n".format(func.name, index))
            elif func.img == '' and func.name != '' and func.name != 'Exit' and func.name != '{' and func.name != '}' and func.name != 'Else':
                funcWithoutImage += ("The {} in line {} doesn't have screenshot\n".format(func.name, index))
            index += 1
        return funcWithoutImage
    except Exception as e:
        exeptionHandler(e)

def on_press(key):
    if (logger != None):
        logger.writeToLog('on_press function')
    try:
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        else:
            pass
    except Exception as e:
        exeptionHandler(e)

def runHendle():
    if (logger != None):
        logger.writeToLog('runHendle function')
    try:
        global stopScript
        stopScript = False
        functionNum = 0
        ifExistFlag = True
        funcWithoutImage = checkImageInFunc()
        if funcWithoutImage != '':
            popupmsg(funcWithoutImage)
        else:
            testLogPath = currentScript.path + 'testLog.txt'
            testLog = open(testLogPath, "w+")
            startTime = datetime.now()
            testLog.write('***Test Start ' + str(startTime) + ' ***\n')
            textView.insert(END, '***Test Start ' + str(startTime) + ' ***\n')
            mainScreen.iconify()
            for func in range(len(currentScript.functions)):
                if(stopScript == False):
                    if currentScript.functions[func].father[0] == currentScript.functions[func].id:
                        if func >= functionNum:
                            if currentScript.functions[func].name == 'Repeat':
                                functionNum += repeat_handle(currentScript.functions[func], currentScript.path,testLog) + 3
                            elif currentScript.functions[func].name == 'Left-Click':
                                left_click_handle(currentScript.functions[func].img, currentScript.path,testLog)
                                functionNum += 1
                            elif currentScript.functions[func].name == 'If-Exist':
                                if currentScript.functions[func].extra.compareState == 'image':
                                    exist,tempFunctionNum = exist_handle(currentScript.functions[func],currentScript.path,testLog)
                                else:
                                    exist, tempFunctionNum = scan_text_compare_handle(currentScript.functions[func], currentScript.path,
                                                             currentScript.functions[func].extra.text, testLog)
                                functionNum += tempFunctionNum
                                ifExistFlag = exist
                            elif currentScript.functions[func].name == 'If-Not-Exist':
                                if currentScript.functions[func].extra.compareState == 'image':
                                    exist,tempFunctionNum = not_exist_handle(currentScript.functions[func],
                                                                               currentScript.path,testLog)
                                else:
                                    exist, tempFunctionNum = not scan_text_compare_handle(currentScript.functions[func], currentScript.path,
                                                             currentScript.functions[func].extra.text, testLog)
                                functionNum += tempFunctionNum
                                ifExistFlag = exist
                            elif currentScript.functions[func].name == 'Else' and not ifExistFlag:
                                else_handle(currentScript.functions[func],currentScript.path,testLog)
                                functionNum += 1
                            elif currentScript.functions[func].name == 'Double-Click':
                                double_click_handle(currentScript.functions[func].img, currentScript.path,testLog)
                                functionNum += 1
                            elif currentScript.functions[func].name == 'Right-Click':
                                right_click_handle(currentScript.functions[func].img, currentScript.path,testLog)
                                functionNum += 1
                            elif currentScript.functions[func].name == 'Sleep':
                                sleep_handle(currentScript.functions[func].extra.time,testLog)
                                functionNum += 1
                            elif currentScript.functions[func].name == 'Insert-Input':
                                insert_input_handle(currentScript.functions[func].img, currentScript.path,currentScript.functions[func].extra.text,testLog)
                                functionNum += 1
                            elif currentScript.functions[func].name == 'Exit':
                                exit_handle(testLog)
                                functionNum += 1
                            elif currentScript.functions[func].name == 'Hover':
                                move_to_handle(currentScript.functions[func].img, currentScript.path,testLog)
                                functionNum += 1
                else:
                    break
            endTime = datetime.now()
            if(testLog != None):
                testLog.write('***Test End ' + str(endTime) + ' ***\n')
                testLog.write('***Total Test Time: ' + str(endTime - startTime) + ' ***\n\n\n')
            textView.insert(END, '***Test End ' + str(endTime) + ' ***\n')
            textView.insert(END, '***Total Test Time: ' + str(endTime-startTime) + ' ***\n\n\n')

        mainScreen.deiconify()
    except Exception as e:
        exeptionHandler(e)


def saveFunctions():
    if (logger != None):
        logger.writeToLog('saveFunctions function')
    try:
        block = []
        for x in currentScript.functions:
            if (x.img != ''):
                imgdict = x.img.getDict()
            else:
                imgdict = ''
            if (x.extra != ''):
                block.append({'name': x.name, 'img': imgdict, 'id': str(x.id),'frameFather':'', 'frame': '', 'fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                              'extra': x.extra.getDict(),'indention':str(x.indention)})
            else:
                block.append({'name': x.name, 'img': imgdict, 'id': str(x.id),'frameFather':'', 'frame': '', 'fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                              'extra': '','indention':str(x.indention)})
        return block
    except Exception as e:
        exeptionHandler(e)


def saveLinesFather():
    if (logger != None):
        logger.writeToLog('saveLinesFather function')
    try:
        block = []
        for x in currentScript.linesFather:
            block.append({'fatherName':x.fatherName,'fromIndex':str(x.fromIndex),'toIndex':str(x.toIndex)})
        return block
    except Exception as e:
        exeptionHandler(e)


def saveCurrentScript():
    if (logger != None):
        logger.writeToLog('saveCurrentScript function')
    try:
        block = []
        block.append({'name': currentScript.name,'created_time':str(currentScript.created_time) , 'path': currentScript.path})
        return block
    except Exception as e:
        exeptionHandler(e)


def saveHundle():
    if (logger != None):
        logger.writeToLog('saveHundle function')
    try:
        clearImages()
        functionPath = currentScript.path + "/functions.json"
        try:
            os.remove(functionPath)
        except:
            pass
        functionsblock = saveFunctions()
        linesFatherblock = saveLinesFather()
        currentScriptblock = saveCurrentScript()
        with open(functionPath, 'w+') as outfile:
            outfile.write(json.dumps(currentScriptblock) + '\n' + json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))
    except Exception as e:
        exeptionHandler(e)

def make_new_project(label):
        functionPath = tkinter.filedialog.askdirectory()
        label.configure(text = functionPath)

def saveAsHundle():
    if (logger != None):
        logger.writeToLog('saveAsHundle function')
    try:
        functionPath = tkinter.filedialog.asksaveasfilename(initialdir=".", title="Select file",
                                                        filetypes=(("Json file", "*.json"), ("all files", "*.*")))
        functionPath+= '.json'
        try:
            os.remove(functionPath)
        except:
            pass
        clearImages()
        functionsblock = saveFunctions()
        linesFatherblock = saveLinesFather()
        currentScriptblock = saveCurrentScript()
        with open(functionPath, 'w+') as outfile:
            outfile.write(json.dumps(currentScriptblock) + '\n' + json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))
    except Exception as e:
        exeptionHandler(e)


def openCurrentScript(currentScriptData):
    if (logger != None):
        logger.writeToLog('openCurrentScript function')
    try:
        created_Time_After_Parse = datetime.strptime(currentScriptData[0]['created_time'], '%Y-%m-%d %H:%M:%S.%f')
        pathFatherDirectory = os.path.dirname(os.path.dirname(currentScriptData[0]['path'])) + '\\'
        return script.Script(currentScriptData[0]['name'],[],created_Time_After_Parse,[],0,pathFatherDirectory)
    except Exception as e:
        exeptionHandler(e)


def openFunctions(data):
    if (logger != None):
        logger.writeToLog('openFunctions function')
    try:
        inputFunctions = []
        tempFunction =[0] * len(data)
        for x in data:
            func = Function('','','', rightSectionFrame,'','','',currentScript,tree,Lb2,photoViewFrame)
            inputFunctions.append(func.getFunction(x,Lb2,currentScript,tempFunction,rightSectionFrame,tree,photoViewFrame))
        currentScript.functions = copy.copy(inputFunctions)
    except Exception as e:
        exeptionHandler(e)


def openLinesFather(data):
    if (logger != None):
        logger.writeToLog('openLinesFather function')
    try:
        inputFunctions = []
        for x in data:
            inputFunctions.append(LineFather(int(x['fromIndex']),int(x['toIndex']),x['fatherName']))
        currentScript.linesFather = copy.copy(inputFunctions)
    except Exception as e:
        exeptionHandler(e)


def openButton():
    if (logger != None):
        logger.writeToLog('openButton')
    try:
        filePath = tkinter.filedialog.askopenfilename(initialdir=".", title="Select file",
                                                      filetypes=(("json files", "*.json"), ("all files", "*.*")))
        with open(filePath) as json_file:
            data = json_file.read()
            currentScriptData = json.loads(data[:data.index('\n')])
            tempData = data[data.index('\n') + 1:]
            functionsData = json.loads(tempData[:tempData.index('\n')])
            linesFatherData = json.loads(tempData[tempData.index('\n') + 1:])

        global currentScript
        currentScript = openCurrentScript(currentScriptData)

        openFunctions(functionsData)
        openLinesFather(linesFatherData)
        updateLb2(0,len(currentScript.functions)-1,'add','deleteBefore')
        selectLb2Index(0)
    except Exception as e:
        exeptionHandler(e)


def updateExtra(tempLineFather,tempFatherFunction,place,currentFunction):
    if (logger != None):
        logger.writeToLog('updateExtra function')
    try:
        while True:
            tempFatherFunction.extra.functions.insert(
                place - tempLineFather.fromIndex - 2, currentFunction)
            if tempFatherFunction.father[0] == tempFatherFunction.id:
                break
            tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
    except Exception as e:
        exeptionHandler(e)


def insert_A():
    if (logger != None):
        logger.writeToLog('insert_A function')
    try:
        if 'Dis' in insert_a_flag[0]:
            return
        try:
            place = Lb2.curselection()[0]
        except:
            place = 0
        if (place != 0 and currentScript.functions[place].name == '}'):
            currentFunction = Function('', '', place, rightSectionFrame, '', '', '',currentScript,tree,Lb2,photoViewFrame,
                                   currentScript.functions[place].indention + 1)
        elif (place != 0 and currentScript.functions[place+1].name == '}'):
            currentFunction = Function('', '', place, rightSectionFrame, '', '', '',currentScript,tree,Lb2,photoViewFrame,
                                   currentScript.functions[place+1].indention + 1)
        elif(place > 0):
            currentFunction = Function('', '', place, rightSectionFrame,'', '', '',currentScript,tree,Lb2,photoViewFrame,currentScript.functions[place+1].indention)
        else:
            currentFunction = Function('', '', place, rightSectionFrame, '', '', '',currentScript,tree,Lb2,photoViewFrame)
        currentScript.functions.insert(place, currentFunction)

        nextFunction = ''
        if place >= 0 and place < len(currentScript.functions)-1:
            nextFunction = currentScript.functions[place + 1]

        if (nextFunction !='' ):
            if(isComplexFuncByName(nextFunction.father[1]) and not isComplexFuncByName(nextFunction.name)):
                currentLineFather = LineFather(currentScript.linesFather[nextFunction.father[0]].fromIndex,
                                                                   currentScript.linesFather[nextFunction.father[0]].toIndex, currentScript.linesFather[nextFunction.father[0]].fatherName)
                currentScript.linesFather.insert(place,currentLineFather)
                fromIndex = currentScript.linesFather[place].fromIndex
                currentScript.functions[place].father = (fromIndex, nextFunction.father[1])
                updateExtra(currentLineFather, currentScript.functions[currentLineFather.fromIndex], place, currentFunction)
            else:
                currentLineFather = LineFather(place, place, '')
                currentScript.linesFather.insert(place, currentLineFather)
                currentScript.functions[place].father = (place, currentScript.functions[place].name)
        # else:
        #     currentScript.linesFather.insert(place, LineFather(place, place, ''))
        #     currentScript.functions[place].father = (place, currentScript.functions[place].name)

        if len(currentScript.functions) > 0:
            updateCurrentScript('A')
        updateLb2(place,place,'add','A')
        selectLb2Index(place)
    except Exception as e:
        exeptionHandler(e)


def insert_B(place = 0,flag = True):

    if (logger != None):
        logger.writeToLog('insert_B function')
    try:
        if(flag == True):
            try:
                place = Lb2.curselection()[0] + 1

            except:
                place = 0
        if(insert_b_flag[0] == 'insertB' or flag == False):
            if(place == 0):
                currentFunction = Function('', '', place, rightSectionFrame, '','','',currentScript,tree,Lb2,photoViewFrame)
            elif(currentScript.functions[place - 1].name == '{'):
                currentFunction = Function('', '', place, rightSectionFrame, '', '', '',currentScript,tree,Lb2,photoViewFrame,
                                           currentScript.functions[place - 1].indention+1)
            else:
                currentFunction = Function('', '', place, rightSectionFrame, '', '', '',currentScript,tree,Lb2,photoViewFrame,
                                           currentScript.functions[place - 1].indention)
            currentScript.functions.insert(place, currentFunction)
            previousFunction = ''
            if place >= 0 and place < len(currentScript.functions):
                previousFunction = currentScript.functions[place -1]
            if (previousFunction != ''):
                fatherLinesFather = currentScript.linesFather[currentScript.functions[previousFunction.father[0]].father[0]]
                if (fatherLinesFather.fromIndex <= place <= fatherLinesFather.toIndex):
                    currentLineFather = LineFather(fatherLinesFather.fromIndex,fatherLinesFather.toIndex,fatherLinesFather.fatherName)
                    currentScript.linesFather.insert(place, currentLineFather)
                    fromIndex = currentScript.linesFather[place].fromIndex
                    currentScript.functions[place].father = (fromIndex, previousFunction.father[1])
                    updateExtra(currentLineFather, currentScript.functions[currentLineFather.fromIndex], place,
                                currentFunction)
                else:
                    currentLineFather = LineFather(place, place, '')
                    currentScript.linesFather.insert(place, currentLineFather)
                    currentScript.functions[place].father = (place, currentScript.functions[place].name)

            if len(currentScript.functions) > 1:
                updateCurrentScript('B')
            if(flag == True):
                updateLb2(place,place,'add','B')
                selectLb2Index(place)
    except Exception as e:
        exeptionHandler(e)

def closeStartWindow(event, startWin):
        try:
            startWin.destroy()
        except:
            pass
        firstTime = False
        startS = Toplevel()
        startS.resizable(False, False)
        #startS.overrideredirect(True)
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

        background = PhotoImage(master=startS,file=r"img\StartUpScreen2.png")
        canvas.bg = background
        canvas.create_image(0, 0, anchor=NW, image=background)

        e1 = Entry(frame)
        e1.pack()
        e1.delete(0, END)
        e1.insert(0, "My_New_Project")

        label = ttk.Label(frame, text="Please select path of new project", background="white")
        label.place(height=40, width=600, x=365, y=310)

        newPButton = PhotoImage(master=startS,file=r"img\buttonStart.png")
        canvas.Button1 = newPButton
        np = canvas.create_image(150, 400, anchor=NW, image=newPButton, tags="Start")
        canvas.tag_bind('Start', '<Button-1>', lambda event: save_new_project_and_run_app(label.cget("text"),e1.get(), startS))
        canvas.tag_bind('Start', '<Enter>', lambda event: hoverOn(event, canvas, np, 1, startS))
        canvas.tag_bind('Start', '<Leave>', lambda event: hoverOff(event, canvas, np, 1, startS))

        e1.place( height=40, width=600 ,x=365,y=215)
        Selec_F_Button = PhotoImage(master=startS,file=r"img\buttonPaN.png")
        canvas.Button2 = Selec_F_Button
        Selec_F = canvas.create_image(135, 285, anchor=NW, image=Selec_F_Button, tags="PaN")
        canvas.tag_bind('PaN', '<Button-1>', lambda event: make_new_project(label))
        canvas.tag_bind('PaN', '<Enter>', lambda event: hoverOn(event, canvas, Selec_F, 5, startS))
        canvas.tag_bind('PaN', '<Leave>', lambda event: hoverOff(event, canvas, Selec_F, 5, startS))

        returnButton = PhotoImage(master=startS,file=r"img\buttonReturn.png")
        canvas.Button3 = returnButton
        returnB = canvas.create_image(750, 400, anchor=NW, image=returnButton, tags="return")
        canvas.tag_bind('return', '<Button-1>', lambda event: startScreen(startS))
        canvas.tag_bind('return', '<Enter>', lambda event: hoverOn(event, canvas, returnB, 6, startS))
        canvas.tag_bind('return', '<Leave>', lambda event: hoverOff(event, canvas, returnB, 6, startS))

        mainScreen.wait_window(startS)


def save_new_project_and_run_app(label,fileName, window):
        if label!='Please select path of new project':
            functionPath =  label+'/'+fileName + "/functions.json"
            global currentScript
            currentScript = script.Script(fileName,[],datetime.now(),path=label + '/')
            global logger
            logger = Logger(currentScript.path + 'Operation Details Log.txt')
            global Emails
            Emails = EmailSender(currentScript.path + 'Operation Details Log.txt')
            try:
                os.mkdir(label+'/'+fileName + '/ScreenShots')
            except:
                print('folder alreay exist!')

            #**************************** Just for testing **********************************
            try:
                os.mkdir(label+'/'+fileName + '/Test Image')
                os.mkdir(label+'/'+fileName + '/Test Image'+ '/Before Crop')
                os.mkdir(label+'/'+fileName + '/Test Image'+ '/After Crop')
            except:
                print('folder alreay exist!')

            root = tree.insert('', 'end', text=fileName, open=True, tag='T')
            SUBS(label+'/'+fileName, root, tree)
            FocusOnSelectedFunc(None)
        insert_A()
        functionsblock = saveFunctions()
        linesFatherblock = saveLinesFather()
        currentScriptblock = saveCurrentScript()
        with open(functionPath, 'w+') as outfile:
            outfile.write(json.dumps(currentScriptblock) + '\n' + json.dumps(functionsblock) + '\n' + json.dumps(
                linesFatherblock))
        selectLb2Index(0)
        window.destroy()
        mainScreen.deiconify()
        mainScreen.state("zoomed")

def isComplexFuncByIndex(index):
    funcName = currentScript.functions[index].name
    if(funcName == 'Repeat' or funcName == 'If-Exist' or funcName == 'If-Not-Exist' or funcName == 'Else'):
        return True
    return False

def isComplexFuncByName(funcName):
    if(funcName == 'Repeat' or funcName == 'If-Exist' or funcName == 'If-Not-Exist' or funcName == 'Else'):
        return True
    return False


def selectLb2Index(index):
    if (logger != None):
        logger.writeToLog('selectLb2Index function')
    try:
        if isComplexFuncByIndex(index) == True:
            index += 2
        Lb2.select_clear(0,len(currentScript.functions)-1)
        Lb2.select_set(index)
        lastClickOnLb2 = index
        FocusOnSelectedFunc(None)
    except Exception as e:
        exeptionHandler(e)

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

        currentScriptData, functionsData, linesFatherData = getDataFromJson(filePath)


        global currentScript
        currentScript = openCurrentScript(currentScriptData)
        global logger
        logger = Logger(currentScript.path + 'Operation Details Log.txt')
        global Emails
        Emails = EmailSender(currentScript.path + 'Operation Details Log.txt')

        openFunctions(functionsData)
        openLinesFather(linesFatherData)
        updateCurrentScript()
        updateLb2(0,len(currentScript.functions)-1,'add')
        selectLb2Index(0)
        # closeStartWindow(None,screenToMini)
        folder_path = os.path.split(filePath)[0]
        file_name = os.path.split(folder_path)[1]
        root = tree.insert('', 'end', text=file_name, open=True, tag='T')
        SUBS(folder_path, root, tree)

        mainScreen.deiconify()
        mainScreen.state("zoomed")
    except Exception as e:
        startScreen()


def getDataFromJson(filePath):
    with open(filePath) as json_file:
        data = json_file.read()
        currentScriptData = json.loads(data[:data.index('\n')])
        tempData = data[data.index('\n') + 1:]
        functionsData = json.loads(tempData[:tempData.index('\n')])
        linesFatherData = json.loads(tempData[tempData.index('\n') + 1:])
    return currentScriptData, functionsData, linesFatherData


def startScreen(startS=None):
    try:
        startS.destroy()
    except:
        pass
    firstTime = False
    startS = Toplevel()
    startS.resizable(False, False)
    #startS.overrideredirect(True)
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

    background = PhotoImage(master=startS,file=r"img\StartUpScreen.png")
    canvas.bg = background
    canvas.create_image(0,0,anchor=NW, image=background)


    newPButton = PhotoImage(master=startS,file=r"img\buttonNP.png")
    canvas.Button1 = newPButton
    np = canvas.create_image(150,400, anchor=NW, image=newPButton,  tags="NewProject")
    canvas.tag_bind('NewProject','<Button-1>', lambda event: closeStartWindow(event, startS))
    canvas.tag_bind('NewProject', '<Enter>', lambda event: hoverOn(event, canvas, np,2, startS))
    canvas.tag_bind('NewProject', '<Leave>', lambda event: hoverOff(event, canvas, np,2, startS))


    loadButton = PhotoImage(master=startS,file=r"img\buttonLoad.png")
    canvas.Button2 = loadButton
    load = canvas.create_image(450, 400, anchor=NW, image=loadButton, tags="Load")
    canvas.tag_bind('Load', '<Button-1>', lambda event: Minimize_and_Open(event, startS))
    canvas.tag_bind('Load', '<Enter>',lambda event: hoverOn(event,canvas, load,3, startS))
    canvas.tag_bind('Load', '<Leave>',lambda event: hoverOff(event, canvas, load,3, startS))

    closeButton = PhotoImage(master=startS,file=r"img\buttonClose.png")
    canvas.Button3 = closeButton
    close=canvas.create_image(750, 400, anchor=NW, image=closeButton, tags="Close")
    canvas.tag_bind('Close', '<Button-1>', lambda event: terminate(startS))
    canvas.tag_bind('Close', '<Enter>',lambda event: hoverOn(event,canvas, close,4, startS))
    canvas.tag_bind('Close', '<Leave>',lambda event: hoverOff(event, canvas, close,4, startS))
    startS.attributes('-topmost', True)

def terminate(screen):
    try:
        for widget in mainScreen.winfo_children():
            if isinstance(widget,Toplevel):
                widget.destroy()
        screen.destroy()
        exit()
    except Exception as e:
        exeptionHandler(e)
        exit()

def hoverOn(event,canvas, item, number, startS):
        if (number == 1):
            Button1 = PhotoImage(master=startS,file=r"img\buttonStartHover.png")
            canvas.a = Button1
            canvas.itemconfig(item, image=Button1)

        if(number==2):
            Button1 = PhotoImage(master=startS,file=r"img\buttonNPHover.png")
            canvas.b = Button1
            canvas.itemconfig(item, image = Button1)
        if(number==3):
            Button1 = PhotoImage(master=startS,file=r"img\buttonLoadHover.png")
            canvas.c = Button1
            canvas.itemconfig(item, image = Button1)

        if(number==4):
            Button1 = PhotoImage(master=startS,file=r"img\buttonCloseHover.png")
            canvas.d = Button1
            canvas.itemconfig(item, image = Button1)

        if (number == 5):

            Button1 = PhotoImage(master=startS,file=r"img\buttonPaNHover.png")
            canvas.e = Button1
            canvas.itemconfig(item, image=Button1)

        if (number == 6):
            Button1 = PhotoImage(master=startS,file=r"img\buttonReturnHover.png")
            canvas.f = Button1
            canvas.itemconfig(item, image=Button1)

def hoverOff(event,canvas, item, number, startS):
        if (number == 1):
            Button1 = PhotoImage(master=startS,file=r"img\buttonStart.png")
            canvas.a = Button1
            canvas.itemconfig(item, image=Button1)

        if (number == 2):
            Button1 = PhotoImage(master=startS,file=r"img\buttonNP.png")
            canvas.b = Button1
            canvas.itemconfig(item, image=Button1)

        if (number == 3):
            Button1 = PhotoImage(master=startS,file=r"img\buttonLoad.png")
            canvas.c = Button1
            canvas.itemconfig(item, image=Button1)

        if(number==4):
            closeButton1 = PhotoImage(master=startS,file=r"img\buttonClose.png")
            canvas.d = closeButton1
            canvas.itemconfig(item, image=closeButton1)
        if (number == 5):
            Button1 = PhotoImage(master=startS,file=r"img\buttonPaN.png")
            canvas.e = Button1
            canvas.itemconfig(item, image=Button1)
        if (number == 6):
            Button1 = PhotoImage(master=startS,file=r"img\buttonReturn.png")
            canvas.f = Button1
            canvas.itemconfig(item, image=Button1)

def clearRe(event):
    if (logger != None):
        logger.writeToLog('clearRe function')
    try:
        textView.delete('1.0',END)
    except Exception as e:
        exeptionHandler(e)

def autosave(arg):
    if (logger != None):
        logger.writeToLog('autosave function')
    try:
        countThread = process[0]

        flag = 0
        if ('No' in arg):
            return
        while (True):
            counter = 60 * 10
            while (counter != 0):
                if (not countThread.is_alive()):
                    flag = 1
                else:
                    flag = 0
                time.sleep(1)
                counter -= 1
                if flag == 1:
                    return
            saveHundle()
    except Exception as e:
        exeptionHandler(e)

def comboBoxSelect(arg,canvas,combo):
    if 'No' in arg:
        filename = "img\\combo.png"
        comboFlag[1]=''
    else:
        filename = filename = "img\\combo2.png"
        comboFlag[1]='2'
    Button1 = PhotoImage(master=mainScreen, file=filename)
    canvas.a = Button1
    canvas.itemconfig(combo, image=Button1)
    if (logger != None):
        logger.writeToLog('comboBoxSelect function')
    try:
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
    except Exception as e:
        exeptionHandler(e)


def on_closing():
    if (logger != None):
        logger.writeToLog('on_closing function')
    try:
        currentFunctions = saveFunctions()
        currentlinesFather = saveLinesFather()

        filePath = currentScript.path + 'functions.json'
        currentScriptData, savedFunctions, savedlinesFather = getDataFromJson(filePath)

        if currentFunctions == savedFunctions and currentlinesFather == savedlinesFather:
            if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
                for x in process:
                    x._is_stopped = True
                mainScreen.destroy()
        else:
            temp = tkinter.messagebox.askyesnocancel("Quit", "Your project is not saved\nDo you want to save your project?")
            if temp == True:
                saveHundle()
                for x in process:
                    x._is_stopped = True
                mainScreen.destroy()
            elif temp == False:
                clearImages()
                for x in process:
                    x._is_stopped = True
                mainScreen.destroy()

    except Exception as e:
        exeptionHandler(e)


def Treeview_right_click(event):
    if (logger != None):
        logger.writeToLog('Treeview_right_click function')
    try:
        tree.selection_set(tree.identify_row(event.y))
        item = tree.identify("item", event.x, event.y)

        item_iid = tree.selection()[0]
        parent_iid = tree.parent(item_iid)
        node = tree.item(parent_iid)['text']
        path = currentScript.path[0:-1] +'/' + node +'/' + tree.item(item)["text"]

        if '.png' in tree.item(item)["text"]:
            menu = Menu(explorerFrame, tearoff=0, bg='#3c3f41', fg='white')
            # menu.add_command(label="Change Name", command = lambda: changeName(item_iid,tree.item(item)["text"], path))
            menu.add_command(label="Preview", command = lambda: image_preview(path))
            # menu.add_command(label="Delete Photo", command = lambda: deletePhoto(path, item_iid))
            menu.post(event.x_root, event.y_root)
    except Exception as e:
        exeptionHandler(e)

def Lb2_right_click(event):
    if (logger != None):
        logger.writeToLog('Lb2_right_click function')
    try:
        menu = Menu(Lb2, tearoff=0, bg='#3c3f41', fg='white')
        menu.add_command(label="Copy", command = lambda: copy_handler())
        menu.add_command(label="Paste", command = lambda: paste_handler())
        menu.add_command(label="Cut", command = lambda: cut_handler())
        menu.add_command(label="Delete", command = lambda: removeFunctions())
        menu.add_command(label="Redo", command = lambda: redo_handler())
        menu.add_command(label="Undo", command = lambda: undo_handler())
        menu.post(event.x_root, event.y_root)
    except Exception as e:
        exeptionHandler(e)

def deletePhoto(path,iid):
    if (logger != None):
        logger.writeToLog('deletePhoto function')
    try:
        if tkinter.messagebox.askokcancel("Delete", "Are you sure you want to delete this file?\nThis will keep the function if exist but without the image"):
            os.remove(path)
            tree.delete(iid)
    except Exception as e:
        exeptionHandler(e)

def changeName(iid, fileName, path):
    if (logger != None):
        logger.writeToLog('changeName function')
    try:
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
    except Exception as e:
        exeptionHandler(e)

def out(entry,fileName, iid, path):
    if (logger != None):
        logger.writeToLog('out function')
    try:
        new_name = entry.get()
        entry.destroy()
        tree.item(iid, text=new_name)
        new_path = path[0:path.rfind('/')]+'/' + new_name
        os.rename(path, new_path)
        for x in currentScript.functions:
            if x.img.img == fileName:
                x.img.img = new_name
    except Exception as e:
        exeptionHandler(e)


def image_preview(filePath):
    if (logger != None):
        logger.writeToLog('image_preview function')
    try:
        r = Toplevel()
        my_image = PhotoImage(master=mainScreen,file=filePath)
        canvas_image = my_image.zoom(2, 2)

        canvas = Canvas(r, height=my_image.width()+100, width=my_image.height()+100)
        canvas.pack()

        canvas.create_image(0, 0, anchor=NW, image=canvas_image)

        r.mainloop()
    except Exception as e:
        exeptionHandler(e)

def copy_handler():
    if (logger != None):
        logger.writeToLog('copy_handler function')
    try:
        indexes = []
        currentIndex = -1
        for x in Lb2.curselection():
            indexes.append(x)
        if(len(indexes)>0):
            copyFunction.clear()
            copyLineFather.clear()
            flag = checkMarkArea(indexes)
            if (flag == True):
                for index in indexes:
                    copyFunction.append(currentScript.functions[index])
                    copyLineFather.append(currentScript.linesFather[index])
    except Exception as e:
        exeptionHandler(e)

def paste_handler():
    try:
        try:
            index = Lb2.curselection()[0]
        except:
            return
        currentFunc = currentScript.functions[index]
        placeAndName = []
        if(currentFunc.name == ''):
            for func in copyFunction:
                if(func.name != '{' and func.name != '}' and func.name != ''):
                    placeAndName.append((index,func.name))
                index += 1
            for func in placeAndName:
                if(currentScript.functions[func[0]].name != ''):
                    insert_B(func[0],False)
                addFunction(func[0],func[1],False)
            updateLb2(placeAndName[0][0],len(copyFunction) + placeAndName[0][0] -1 ,'add')
            selectLb2Index(func[0])
    except Exception as e:
        exeptionHandler(e)

def esc_handler():
    if (logger != None):
        logger.writeToLog('esc_handler function')
    try:
        global stopScript
        stopScript = True
    except Exception as e:
        exeptionHandler(e)

def cut_handler():
    if (logger != None):
        logger.writeToLog('cut_handler function')
    try:
        copy_handler()
        removeFunctions()
    except Exception as e:
        exeptionHandler(e)

def undo_handler():
    if (logger != None):
        logger.writeToLog('undo_handler function')
    try:
        if(len(undoFunctions) > 0):
            openFunctions(undoFunctions[len(undoFunctions) - 1])  # change currentScript.functions
            openLinesFather(undoLinesFather[len(undoLinesFather) - 1])  # change currentScript.linesFather

            undoFunctions.pop(len(undoFunctions) - 1)  # pop the last redo save from redoFunctions
            undoLinesFather.pop(len(undoLinesFather) - 1)  # pop the last redo save from redoLinesFather
            updateLb2(0, len(currentScript.functions) - 1, 'add', 'deleteBefore')
            if (len(currentScript.functions) == 1 and currentScript.functions[0].name == ''):
                Lb2.select_set(0)
                disableButtons(0)
            updateRedoFunctions()
    except Exception as e:
        exeptionHandler(e)

def redo_handler():
    if (logger != None):
        logger.writeToLog('redo_handler function')
    try:
        if(len(redoFunctions) > 1):
            openFunctions(redoFunctions[len(redoFunctions)-2]) # change currentScript.functions
            openLinesFather(redoLinesFather[len(redoLinesFather)-2])# change currentScript.linesFather

            updateUndoFunctions(len(redoFunctions)-1)

            redoFunctions.pop(len(redoFunctions)-1) #pop the last redo save from redoFunctions
            redoLinesFather.pop(len(redoLinesFather)-1)#pop the last redo save from redoLinesFather
            updateLb2(0, len(currentScript.functions) - 1, 'add', 'deleteBefore')
            if(len(currentScript.functions) == 1 and currentScript.functions[0].name == ''):
                Lb2.select_set(0)
                disableButtons(0)
    except Exception as e:
        exeptionHandler(e)

def delete_handler():
    if (logger != None):
        logger.writeToLog('delete_handler function')
    try:
        indexes = []
        for x in Lb2.curselection():
            indexes.append(x)
        flag = checkMarkArea(indexes)
        if (flag == True):
            removeFunctions()
    except Exception as e:
        exeptionHandler(e)

def repeat_handle(fatherFunction,path,testLog):
    if (logger != None):
        logger.writeToLog('repeat_handle function')
    try:
        repeatTime = fatherFunction.extra.time
        childrenFunction = fatherFunction.extra.functions
        functionNum = 0
        for i in range(repeatTime):
            if(stopScript == False):
                for func in childrenFunction:
                    functionNum = ComplexRunHandle(func, functionNum, path, testLog)
            else:
                break
        return functionNum/repeatTime
    except Exception as e:
        exeptionHandler(e)


def ComplexRunHandle(func, functionNum, path, testLog):
    if (func.name == 'Repeat'):
        functionNum += repeat_handle(func, path, testLog) + 3
    elif (func.name == 'Left-Click'):
        left_click_handle(func.img, path, testLog)
        functionNum += 1
    elif (func.name == 'If-Exist'):
        exist, tempFunctionNum = exist_handle(func, path, testLog)
        functionNum += tempFunctionNum
        ifExistFlag = exist
    elif (func.name == 'If-Not-Exist'):
        exist, tempFunctionNum = not_exist_handle(func, path, testLog)
        functionNum += tempFunctionNum
        ifExistFlag = exist
    elif (func.name == 'Double-Click'):
        double_click_handle(func.img, path, testLog)
        functionNum += 1
    elif (func.name == 'Else' and not ifExistFlag):
        functionNum += else_handle(func, path, testLog)
    elif (func.name == 'Right-Click'):
        right_click_handle(func.img, path, testLog)
        functionNum += 1
    elif (func.name == 'Sleep'):
        sleep_handle(func.extra.time, testLog)
        functionNum += 1
    elif (func.name == 'Insert-Input'):
        insert_input_handle(func.img, path, func.extra.text, testLog)
        functionNum += 1
    elif (func.name == 'Exit'):
        exit_handle(testLog)
        functionNum += 1
    elif (func.name == 'Hover'):
        move_to_handle(func.img, path, testLog)
        functionNum += 1
    return functionNum


def sleep_handle(timeDelay,testLog):
    if (logger != None):
        logger.writeToLog('sleep_handle function')
    try:
        testLog.write('wait for {} second as expected (Sleep)\n'.format(timeDelay))
        textView.insert(END,'wait for {} second (Sleep)\n'.format(timeDelay))
        time.sleep(timeDelay)
    except Exception as e:
        exeptionHandler(e)

def left_click_handle(template,path,testLog):
    if (logger != None):
        logger.writeToLog('left_click_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        beforeCropScreenShot,screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop\\' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop\\' + template.img)
        exist,howManyRectangles = ImgRecog.photoRec(path,screenShot,template)
        x = (template.x1Cord + template.x0Cord) / 2
        y = (template.y1Cord + template.y0Cord) / 2
        if(exist == True):
            testLog.write('image {} is exist as expected (Left-Click)\n'.format(template.img))
            textView.insert(END,'image {} is exist as expected (Left-Click)\n'.format(template.img))
            pyautogui.click(x,y,duration=speed)
        else:
            testLog.write('image {} is not exist as not expected (Left-Click)\n'.format(template.img))
            textView.insert(END, 'image {} is not exist as not expected (Left-Click)\n'.format(template.img))
    except Exception as e:
        exeptionHandler(e)

def insert_input_handle(template,path,text,testLog):
    if (logger != None):
        logger.writeToLog('insert_input_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        beforeCropScreenShot, screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop' + template.img)
        exist,howManyRec = ImgRecog.photoRec(path,screenShot,template)
        x = (template.x1Cord + template.x0Cord) / 2
        y = (template.y1Cord + template.y0Cord) / 2
        if(exist == True):
            testLog.write('image {} is exist as expected (Insert-Input)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as expected (Insert-Input)\n'.format(template.img))
            pyautogui.click(x, y, duration=speed)
            pyautogui.typewrite(text, interval=0.1)
        else:
            testLog.write('image {} is not exist as not expected (Insert-Input)\n'.format(template.img))
            textView.insert(END, 'image {} is not exist as not expected (Insert-Input)\n'.format(template.img))
    except Exception as e:
        exeptionHandler(e)
def exit_handle(testLog):
    if (logger != None):
        logger.writeToLog('exit_handle function')
    try:
        esc_handler()
    except Exception as e:
        exeptionHandler(e)

def move_to_handle(template,path,testLog):
    if (logger != None):
        logger.writeToLog('move_to_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        beforeCropScreenShot, screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop' + template.img)
        exist, howManyRectangles = ImgRecog.photoRec(path, screenShot, template)
        x = (template.x1Cord + template.x0Cord) / 2
        y = (template.y1Cord + template.y0Cord) / 2
        if (exist == True):
            testLog.write('image {} is exist as expected (Move-To)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as expected (Move-To)\n'.format(template.img))
            pyautogui.moveTo(x, y, duration=speed)
        else:
            testLog.write('image {} is not exist as not expected (Move-To)\n'.format(template.img))
            textView.insert(END, 'image {} is not exist as not expected (Move-To)\n'.format(template.img))
    except Exception as e:
        exeptionHandler(e)

def scan_text_compare_handle(fatherFunction,path,text,testLog):
    if (logger != None):
        logger.writeToLog('scan_text_compare_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        childrenFunctions = fatherFunction.extra.functions
        beforeCropScreenShot, screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop' + template.img)
        exist = ScanText.scan_text_and_compare(screenShot,text)
        functionNum = 0
        if (exist == True):
            testLog.write('image {} is exist as expected (scan_text_compare)\n'.format(fatherFunction.img.img))
            textView.insert(END, 'image {} is exist as expected (scan_text_compare)\n'.format(fatherFunction.img.img))

            for func in childrenFunctions:
                if (stopScript == False):
                    if (func.father[0] == fatherFunction.id):
                        functionNum = ComplexRunHandle(func, functionNum, path, testLog)
                else:
                    break
        else:
            testLog.write('image {} is not exist as not expected (scan_text_compare)\n'.format(fatherFunction.img.img))
            textView.insert(END, 'image {} is not exist as not expected (scan_text_compare)\n'.format(fatherFunction.img.img))
        return exist,functionNum
    except Exception as e:
        exeptionHandler(e)

def double_click_handle(template,path,testLog):
    if (logger != None):
        logger.writeToLog('double_click_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        beforeCropScreenShot, screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop' + template.img)
        exist,howManyRec = ImgRecog.photoRec(path,screenShot,template)
        x = (template.x1Cord + template.x0Cord) / 2
        y = (template.y1Cord + template.y0Cord) / 2
        if(exist == True):
            testLog.write('image {} is exist as expected (Double-Click)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as expected (Double-Click)\n'.format(template.img))
            pyautogui.doubleClick(x,y,duration=speed)
        else:
            testLog.write('image {} is exist as not expected (Double-Click)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as not expected (Double-Click)\n'.format(template.img))
    except Exception as e:
        exeptionHandler(e)

def right_click_handle(template,path,testLog):
    if (logger != None):
        logger.writeToLog('right_click_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        beforeCropScreenShot, screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop' + template.img)
        exist,howManyRec = ImgRecog.photoRec(path,screenShot,template)
        x = (template.x1Cord + template.x0Cord) / 2
        y = (template.y1Cord + template.y0Cord) / 2
        if(exist == True):
            testLog.write('image {} is exist as expected (Right-Click)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as expected (Right-Click)\n'.format(template.img))

            pyautogui.rightClick(x,y,duration=speed)
        else:
            testLog.write('image {} is exist as not expected (Right-Click)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as not expected (Right-Click)\n'.format(template.img))
    except Exception as e:
        exeptionHandler(e)

def exist_handle(fatherFunction,path,testLog):
    if (logger != None):
        logger.writeToLog('exist_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        childrenFunctions = fatherFunction.extra.functions
        template = fatherFunction.img
        ifExistFlag = True
        beforeCropScreenShot, screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop' + template.img)
        exist,howManyRec = ImgRecog.photoRec(path, screenShot, template)
        functionNum = 0
        if(exist == True):
            testLog.write('image {} is exist as expected (If-Exist)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as expected (If-Exist)\n'.format(template.img))

            for func in childrenFunctions:
                if(stopScript==False):
                    if(func.father[0] == fatherFunction.id):
                        functionNum = ComplexRunHandle(func, functionNum, path, testLog)
                else:
                    break
        else:
            testLog.write('image {} is not exist as not expected (If-Exist)\n'.format(template.img))
            textView.insert(END,'image {} is not exist as not expected (If-Exist)\n'.format(template.img))

        return exist,functionNum
    except Exception as e:
        exeptionHandler(e)

def not_exist_handle(fatherFunction,path,testLog):
    if (logger != None):
        logger.writeToLog('not_exist_handle function')
    try:
        time.sleep(waitBeforeImageProcess)
        childrenFunctions = fatherFunction.extra.functions
        template = fatherFunction.img
        ifExistFlag = True
        beforeCropScreenShot, screenShot = ImgRecog.tempScreenShot(template,currentScript)
        beforeCropScreenShot.save(currentScript.path + 'Test Image\\before Crop' + template.img)
        screenShot.save(currentScript.path + 'Test Image\\after Crop' + template.img)
        exist,howManyRec = ImgRecog.photoRec(path, screenShot, template)
        functionNum = 0
        if (exist == False):
            testLog.write('image {} is not exist as expected (If-Not-Exist)\n'.format(template.img))
            textView.insert(END,'image {} is not exist as expected (If-Not-Exist)\n'.format(template.img))


            for func in childrenFunctions:
                if(stopScript == False):
                    functionNum = ComplexRunHandle(func, functionNum, path, testLog)
                else:
                    break
        else:
            testLog.write('image {} is exist as not expected(If-Not-Exist)\n'.format(template.img))
            textView.insert(END, 'image {} is exist as not expected(If-Not-Exist)\n'.format(template.img))

        return exist, functionNum
    except Exception as e:
        exeptionHandler(e)

def else_handle(fatherFunction,path,testLog):
    if (logger != None):
        logger.writeToLog('else_handle function')
    try:
        childrenFunctions = fatherFunction.extra.functions
        ifExistFlag = True
        functionNum = 0
        for func in childrenFunctions:
            if(stopScript==False):
                functionNum = ComplexRunHandle(func, functionNum, path, testLog)
            else:
                break
        return functionNum
    except Exception as e:
        exeptionHandler(e)



def drag_and_drop(event,pointers,selection_index, canvasGoust, flag):
    if (logger != None):
        logger.writeToLog('drag_and_drop function')
    try:
        selection = Lb1.get(selection_index)
        for child in canvasGoust.winfo_children():
            child.destroy()

        if flag[0]=='empty':
            flag[0] = selection
            flag[1] = selection_index
            name_of_fun = Label(canvasGoust, text=selection, fg='white', bg='#3c3f41')
            Lb1.select_set(selection_index)
            Lb1.activate(selection_index)
        else:
            name_of_fun = Label(canvasGoust, text=flag[0], fg='white', bg='#3c3f41' )
            Lb1.select_set(flag[1])
            Lb1.activate(flag[1])


        name_of_fun.pack()

        canvasGoust.place(x=pointers[0]-30, y=pointers[1]-50)
    except Exception as e:
        exeptionHandler(e)

def drop(event, canvasGoust, flag ):
    if (logger != None):
        logger.writeToLog('drop function')
    try:
        for child in canvasGoust.winfo_children():
            child.destroy()
        background = PhotoImage(master=mainScreen,file=r"img\transparent.png")
        canvasGoust.bg = background
        canvasGoust.create_image(0, 0, image=background)
        # canvasGoust.pack()
        canvasGoust.place(x=10000000, y=1000000000)
        flag[0]='empty'

        pointerX, pointerY = event.x_root,event.y_root
        if(pointerX>= Lb2.winfo_rootx() and pointerX<= Lb2.winfo_rootx()+ Lb2.winfo_width() and pointerY>=Lb2.winfo_rooty() and pointerY<= Lb2.winfo_rooty()+ Lb2.winfo_height()) :
            addFunction()
    except Exception as e:
        exeptionHandler(e)

def change_on_hover(event, name, canvas, item):
        try:
            if 'Dis' in name:
                filename = "img\\" + name + ".png"

                Button1 = PhotoImage(master=mainScreen,file=filename)
                canvas.a = Button1
                canvas.itemconfig(item, image=Button1)
                return
        except:
            pass
        if 'Hover' in name:
            filename = "img\\" +  name[0:name.rfind('Hover')] + ".png"
        else:
            filename = "img\\" + name + "Hover.png"


        Button1 = PhotoImage(master=mainScreen,file=filename)
        canvas.a = Button1
        canvas.itemconfig(item, image=Button1)

def combobox_save(comboFlag,x,y, canvas, combo):
    if (logger != None):
        logger.writeToLog('combobox_save function')
    try:
        if comboFlag[0] =='0':
            menu = Menu(explorerFrame, tearoff=0, bg='#3c3f41', fg='white')
            menu.add_command(label="No Auto Save", command = lambda: comboBoxSelect('No_Auto',canvas,combo))
            menu.add_command(label="Auto Save", command = lambda: comboBoxSelect('Auto', canvas,combo))
            menu.post(x+20, y+35)
            comboFlag[0]='1'
        else:
            comboFlag[0]='0'
            pass
    except Exception as e:
        exeptionHandler(e)

def editToolBar_click(event, x, y, flag):
    if (logger != None):
        logger.writeToLog('editToolBar_click function')
    try:
        if flag[0] == '0':
            menu = Menu(mainScreen, tearoff=0, bg='#3c3f41', fg='white')
            menu.add_command(label="Copy", command = lambda: copy_handler())
            menu.add_command(label="Paste", command = lambda: paste_handler())
            menu.add_command(label="Cut", command = lambda: cut_handler())
            menu.add_command(label="Delete", command = lambda: removeFunctions())
            menu.add_command(label="Redo", command = lambda: redo_handler())
            menu.add_command(label="Undo", command = lambda: undo_handler())
            menu.post(x+10, y+35)
            flag[0]='1'
        else:
            flag[0]='0'
    except Exception as e:
        exeptionHandler(e)

def option_click_handler(selection, flag):
    if (logger != None):
        logger.writeToLog('option_click_handler function')
    try:
        global speed
        flag[1] = selection
        if selection == 'Slow':
            speed = 3
        elif selection == 'Regular':
            speed = 1
        elif selection == 'Fast':
            speed = 0.6
        elif selection == 'Very Fast':
            speed = 0.2
    except Exception as e:
        exeptionHandler(e)

def optionToolBar_click(event, x, y, flag):
    if (logger != None):
        logger.writeToLog('optionToolBar_click function')
    try:
        if flag[0] == '0':
            menu = Menu(mainScreen, tearoff=0, bg='#3c3f41', fg='white')
            if flag[1]=='Slow':
                menu.add_command(label="⦿ Slow", command=lambda: option_click_handler('Slow', flag))
            else:
                menu.add_command(label="      Slow", command=lambda: option_click_handler('Slow', flag))
            if flag[1]=='Regular':
                menu.add_command(label="⦿ Regular", command=lambda: option_click_handler('Regular', flag))
            else:
                menu.add_command(label="      Regular", command=lambda: option_click_handler('Regular', flag))
            if flag[1]=='Fast':
                menu.add_command(label="⦿ Fast", command=lambda: option_click_handler('Fast', flag))
            else:
                menu.add_command(label="      Fast", command=lambda: option_click_handler('Fast', flag))
            if flag[1] == 'Very Fast':
                menu.add_command(label="⦿ Very Fast", command=lambda: option_click_handler('Very Fast', flag))
            else:
                menu.add_command(label="      Very Fast", command=lambda: option_click_handler('Very Fast', flag))

            menu.post(x + 10, y + 35)
            flag[0] = '1'
        else:
            flag[0] = '0'
    except Exception as e:
        exeptionHandler(e)

def OnVsb(*args):
    if (logger != None):
        logger.writeToLog('OnVsb function')
    try:
        lb2Indexes.yview(*args)
        Lb2.yview(*args)
    except Exception as e:
        exeptionHandler(e)

def OnHsb(*args):
    if (logger != None):
        logger.writeToLog('OnHsb function')
    try:
        lb2Indexes.xview(*args)
        Lb2.xview(*args)
    except Exception as e:
        exeptionHandler(e)

def OnMouseWheel(event):
    if (logger != None):
        logger.writeToLog('OnMouseWheel function')
    try:
        lb2Indexes.yview("scroll", event.delta*-1, "units")
        Lb2.yview("scroll", event.delta*-1, "units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"
    except Exception as e:
        exeptionHandler(e)

def Lb2Indexes_left_click(event):
    if (logger != None):
        logger.writeToLog('Lb2Indexes_left_click function')
    try:
        try:
            index = lb2Indexes.curselection()[0]
        except:
            return
        lb2Indexes.select_clear(index)
    except Exception as e:
        exeptionHandler(e)

def screen_shot_handle():
    if (logger != None):
        logger.writeToLog('screen_shot_handle function')
    try:
        if 'Dis' in takeS_flag[0]:
            return
        global flag_of_shift
        flag_of_shift = True
        mainScreen.iconify()

    except Exception as e:
        exeptionHandler(e)

def clearImages():
    usedImages = []
    for func in currentScript.functions:
        if(func.img != ''):
            usedImages.append(func.img.img)
    previousPath = os.getcwd()
    list_of_pics = os.listdir(currentScript.path + 'ScreenShots\\')
    os.chdir(currentScript.path + 'ScreenShots\\')

    for pic in list_of_pics:
        if not pic in usedImages:
            os.remove(pic)
    os.chdir(previousPath)




def exeptionHandler(exeption):
    logger.writeExeption(traceback.format_exc())
    global Emails
    Emails.send(traceback.format_exc())

def Lb1_double_click(event):
    if (logger != None):
        logger.writeToLog('Lb1_double_click function')
    try:
        addFunction()
    except Exception as e:
        exeptionHandler(e)

if __name__ == '__main__':
    functionFather = []


    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.configure(background='#3c3f41')

    mainScreen.columnconfigure(0,weight = 1)
    mainScreen.columnconfigure(1,weight = 2)
    mainScreen.columnconfigure(2,weight = 1)
    mainScreen.rowconfigure(0,weight = 1)
    mainScreen.rowconfigure(1,weight = 1)
    mainScreen.rowconfigure(2,weight = 1)
    mainScreen.rowconfigure(3,weight = 30)

    if firstTime:
        startScreen()

    toolbarFrame = Frame(mainScreen, bg='#3c3f41')
    toolbarFrame.grid(row=0,column=0,sticky = 'WEN')

    openToolButton = PhotoImage(master=mainScreen, file=r"img\OpenTool.png")
    canvasOpen = Canvas(toolbarFrame,height = openToolButton.height(),width = openToolButton.width(),  bg='#3c3f41', highlightbackground='#3c3f41')
    canvasOpen.grid(row=0,column=0, sticky="WE")

    canvasOpen.open = openToolButton
    openTool = canvasOpen.create_image(openToolButton.width()/2, openToolButton.height()/2, anchor=CENTER, image=openToolButton, tags="openTool")

    canvasOpen.tag_bind('openTool', '<Button-1>', lambda event:openButton())
    canvasOpen.tag_bind('openTool', '<Enter>', lambda event: change_on_hover(event,"openTool",canvasOpen,openTool))
    canvasOpen.tag_bind('openTool', '<Leave>', lambda event: change_on_hover(event,"openToolHover",canvasOpen,openTool))

    saveToolButton = PhotoImage(master=mainScreen, file=r"img\SaveTool.png")
    canvasSave = Canvas(toolbarFrame, height=saveToolButton.height(), width=saveToolButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasSave.grid(row=0, column=1, sticky="NWE")

    canvasSave.save = saveToolButton
    saveTool = canvasSave.create_image(saveToolButton.width()/2, saveToolButton.height()/2, anchor=CENTER, image=saveToolButton, tags="SaveTool")

    canvasSave.tag_bind('SaveTool', '<Button-1>', lambda event: saveHundle())
    canvasSave.tag_bind('SaveTool', '<Enter>', lambda event: change_on_hover(event, "SaveTool", canvasSave, saveTool))
    canvasSave.tag_bind('SaveTool', '<Leave>',lambda event: change_on_hover(event, "SaveToolHover", canvasSave, saveTool))

    saveAsToolButton = PhotoImage(master=mainScreen,file=r"img\SaveAsTool.png")
    canvasSaveAs = Canvas(toolbarFrame, height=saveAsToolButton.height(), width=saveAsToolButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasSaveAs.grid(row=0, column=2, sticky="EWN")

    canvasSaveAs.save = saveToolButton
    saveAsTool = canvasSaveAs.create_image(saveAsToolButton.width()/2, saveAsToolButton.height()/2, anchor=CENTER, image=saveAsToolButton, tags="SaveAsTool")

    canvasSaveAs.tag_bind('SaveAsTool', '<Button-1>', lambda event: saveAsHundle())
    canvasSaveAs.tag_bind('SaveAsTool', '<Enter>', lambda event: change_on_hover(event, "SaveAsTool", canvasSaveAs, saveAsTool))
    canvasSaveAs.tag_bind('SaveAsTool', '<Leave>', lambda event: change_on_hover(event, "SaveAsToolHover", canvasSaveAs, saveAsTool))

    optionsAndRunFrame = Frame(mainScreen, bd=3, bg='#3c3f41')
    optionsAndRunFrame.grid(row=0, column=1, sticky='N')

    editToolButton = PhotoImage(master=mainScreen,file=r"img\editTool.png")
    canvasEdit = Canvas(optionsAndRunFrame, height=editToolButton.height(), width=editToolButton.width(), bg='#3c3f41',highlightbackground='#3c3f41')
    canvasEdit.grid(row=0, column=0, sticky="NWE")

    canvasEdit.edit = editToolButton
    editTool = canvasEdit.create_image(editToolButton.width()/2, editToolButton.height()/2, anchor=CENTER, image=editToolButton, tags="edit")
    canvasEdit_flag=['0']
    canvasEdit.tag_bind('edit', '<Button-1>', lambda event: editToolBar_click(event, canvasEdit.winfo_rootx(),canvasEdit.winfo_rooty(), canvasEdit_flag))
    canvasEdit.tag_bind('edit', '<Enter>',lambda event: change_on_hover(event, "editTool", canvasEdit, editTool))
    canvasEdit.tag_bind('edit', '<Leave>',lambda event: change_on_hover(event, "editToolHover", canvasEdit, editTool))

    optionToolButton = PhotoImage(master=mainScreen, file=r"img\optionsTool.png")
    canvasOption = Canvas(optionsAndRunFrame, height=optionToolButton.height(), width=optionToolButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasOption.grid(row=0, column=1, sticky="NWE")

    canvasOption.options = optionToolButton
    optionTool = canvasOption.create_image(optionToolButton.width()/2, optionToolButton.height()/2, anchor=CENTER, image=optionToolButton, tags="options")
    canvasOptions_flag = ['0', 'Regular']
    canvasOption.tag_bind('options', '<Button-1>', lambda event: optionToolBar_click(event, canvasOption.winfo_rootx(), canvasOption.winfo_rooty(), canvasOptions_flag))
    canvasOption.tag_bind('options', '<Enter>', lambda event: change_on_hover(event, "optionsTool", canvasOption, optionTool))
    canvasOption.tag_bind('options', '<Leave>', lambda event: change_on_hover(event, "optionsToolHover", canvasOption, optionTool))

    playToolButton = PhotoImage(master=mainScreen,file=r"img\PlayTool.png")
    canvasPlay = Canvas(optionsAndRunFrame, height=playToolButton.height(), width=playToolButton.width(), bg='#3c3f41',highlightbackground='#3c3f41')
    canvasPlay.grid(row=0, column=2, sticky="N")

    canvasPlay.play = playToolButton
    playTool = canvasPlay.create_image(playToolButton.width()/2, playToolButton.height()/2, anchor=CENTER, image=playToolButton, tags="PlayTool")
    reportList=[]
    canvasPlay.tag_bind('PlayTool', '<Button-1>', lambda event: runHendle())
    canvasPlay.tag_bind('PlayTool', '<Enter>', lambda event: change_on_hover(event, "PlayTool", canvasPlay, playTool))
    canvasPlay.tag_bind('PlayTool', '<Leave>', lambda event: change_on_hover(event, "PlayToolHover", canvasPlay, playTool))

    comboToolButton = PhotoImage(master=mainScreen,file=r"img\Combo.png")
    canvasCombo = Canvas(mainScreen, height=comboToolButton.height(), width=comboToolButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasCombo.grid(row=0, column=2, sticky="N")

    canvasCombo.combo = comboToolButton
    combo = canvasCombo.create_image(comboToolButton.width()/2, comboToolButton.height()/2, anchor=CENTER, image=comboToolButton, tags="Combo")
    comboFlag=['0','']
    canvasCombo.tag_bind('Combo', '<Button-1>', lambda event: combobox_save(comboFlag,canvasCombo.winfo_rootx(),canvasCombo.winfo_rooty(), canvasCombo,combo))
    canvasCombo.tag_bind('Combo', '<Enter>', lambda event: change_on_hover(event, "Combo"+comboFlag[1],canvasCombo , combo))
    canvasCombo.tag_bind('Combo', '<Leave>', lambda event: change_on_hover(event, "Combo" + comboFlag[1] +"Hover", canvasCombo, combo))

    line_style = ttk.Style()
    line_style.configure("Line.TSeparator", background="black")
    seperatorFrame = Frame(mainScreen,bg='white',height = 6)
    seperatorFrame.grid(column=0, row=1,sticky="WENS")

    seperatorFrame2 = Frame(mainScreen, bg='white', height=6)
    seperatorFrame2.grid(column=1, row=1, sticky="WENS")

    seperatorFrame3 = Frame(mainScreen, bg='white', height=6)
    seperatorFrame3.grid(column=2, row=1, sticky="WENS")

    addFunclButton = PhotoImage(master=mainScreen,file=r"img\AddFuncDis.png")
    canvasAddFun = Canvas(mainScreen, height=addFunclButton.height(), width=addFunclButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasAddFun.grid(row=2, column=2, sticky="N", pady=4)

    canvasAddFun.addFun = addFunclButton
    addFunc = canvasAddFun.create_image(addFunclButton.width()/2, addFunclButton.height()/2, image=addFunclButton, tags="AddFunc")
    add_func_flag=['AddFuncDis']
    canvasAddFun.tag_bind('AddFunc', '<Button-1>',lambda event: addFunction(add_func_flag))
    canvasAddFun.tag_bind('AddFunc', '<Enter>', lambda event: change_on_hover(event, add_func_flag[0], canvasAddFun, addFunc))
    canvasAddFun.tag_bind('AddFunc', '<Leave>', lambda event: change_on_hover(event, add_func_flag[0]+'Hover', canvasAddFun, addFunc))

    leftSectionFrame = Frame(mainScreen,bg='#3c3f41')
    leftSectionFrame.columnconfigure(0, weight=1)
    leftSectionFrame.rowconfigure(0, weight=1)
    leftSectionFrame.rowconfigure(1, weight=1)
    leftSectionFrame.grid(row=3, column=0, sticky='NWES', padx=10, pady=(0, 10))

    explorerFrame = Frame(leftSectionFrame, bd=3, relief=SUNKEN)
    explorerFrame.columnconfigure(0, weight=1)
    explorerFrame.rowconfigure(0, weight=1)
    explorerFrame.grid(row=0, column=0, sticky='NWE', pady= (0,25))

    reportFrame = Frame(leftSectionFrame, bd=3, relief=SUNKEN)
    reportFrame.columnconfigure(0, weight=1)
    reportFrame.rowconfigure(0, weight=1)
    reportFrame.grid(row=1, column=0, sticky='NWES', pady= (25,0))

    leftSectionFrame.update_idletasks()
    textView = Text(reportFrame,wrap=NONE, width=int(leftSectionFrame.winfo_width()/15),bg='#2b2b2b',fg='white',font=tkFont.Font(family="Ariel", size=10))
    textView.grid(row=0, column=0,sticky='WNES')

    yScroll1 = Scrollbar(reportFrame, orient=VERTICAL, command=textView.yview)
    yScroll1.grid(row=0, column=1, sticky='NS')

    xScroll1 = Scrollbar(reportFrame, orient=HORIZONTAL, command=textView.xview)
    xScroll1.grid(row=1, column=0, sticky='EW')

    textView['yscrollcommand'] = yScroll1.set
    textView['xscrollcommand'] = xScroll1.set

    centerSectionFrame = Frame(mainScreen,bg='#3c3f41')
    centerSectionFrame.columnconfigure(0, weight=1)
    centerSectionFrame.rowconfigure(0, weight=1)
    centerSectionFrame.rowconfigure(1, weight=30)
    centerSectionFrame.grid(row=3, column=1, sticky='NWES', padx=(5,5))

    mainFrame1 = Frame(centerSectionFrame,bd = 3, relief=SUNKEN, bg='#3c3f41')
    mainFrame1.columnconfigure(0, weight=1)
    mainFrame1.columnconfigure(1, weight=1)
    mainFrame1.columnconfigure(2, weight=1)
    mainFrame1.columnconfigure(3, weight=1)
    mainFrame1.columnconfigure(4, weight=1)
    mainFrame1.columnconfigure(5, weight=1)
    mainFrame1.grid(row=0, column=0,sticky='N')

    Lb2Frame = Frame(centerSectionFrame,bd=0)
    Lb2Frame.columnconfigure(0, weight=1)
    Lb2Frame.columnconfigure(1, weight=1000)
    Lb2Frame.rowconfigure(0, weight=1)
    Lb2Frame.grid(row=1, column=0, sticky='NSWE', pady=(0, 10))

    yScroll = Scrollbar(Lb2Frame, orient=VERTICAL,command = OnVsb)
    yScroll.grid(row=0, column=2, sticky='NS')

    xScroll = Scrollbar(Lb2Frame, orient=HORIZONTAL,command = OnHsb)
    xScroll.grid(row=1, column=1, sticky='EW')

    lb2Indexes = Listbox(Lb2Frame, background="#2b2b2b",xscrollcommand=xScroll.set,yscrollcommand=yScroll.set,selectmode=BROWSE,width=4,bd=0)
    lb2Indexes.config(highlightbackground="#2b2b2b")
    lb2Indexes.grid(row=0, column=0, sticky='WNSE')

    Lb2Frame.update()
    Lb2FrameHeight = Lb2Frame.winfo_reqheight()

    lb2Indexes.configure(state=DISABLED)
    lb2Indexes.bind("<MouseWheel>", OnMouseWheel)
    lb2Indexes.bind("<Button-1>", lambda event: addFunction())

    Lb2 = Listbox(Lb2Frame, background="#2b2b2b",xscrollcommand=xScroll.set,yscrollcommand=yScroll.set,selectmode=EXTENDED,bd=0)

    Lb2.grid(row=0, column=1, sticky='NSWE')
    Lb2.bind("<Button-3>", Lb2_right_click)
    Lb2.bind("<MouseWheel>", OnMouseWheel)
    Lb2.bind('<Return>', lambda event: insert_B())

    rightSectionFrame = Frame(mainScreen, relief=SUNKEN, background="#3c3f41")
    rightSectionFrame.columnconfigure(0,weight=1)
    rightSectionFrame.rowconfigure(0,weight=1)
    rightSectionFrame.rowconfigure(1,weight=4)
    rightSectionFrame.grid(row=3,column=2,sticky='NWES',padx =(0,10),pady=(0,10))

    Lb1 = Listbox(rightSectionFrame, exportselection=0,height = len(functionList), selectmode = SINGLE, bd=3,  background="#2b2b2b", fg='white')
    Lb1.bind("<Double-Button-1>", Lb1_double_click)
    Lb1.grid(row=0, column=0, sticky='NEW')

    for x in range(0, len(functionList)):
        Lb1.insert(x, functionList[x])
        Lb1.itemconfig(x, foreground=Lb1Colors[x])
    Lb1.config(state=DISABLED)
    flag_for_drag_and_drop = ["empty", 0]

    canvasGoust = Canvas(mainScreen, bg='#3c3f41')
    Lb1.bind('<B1-Motion>',
             lambda event: drag_and_drop(event, mainScreen.winfo_pointerxy(), Lb1.curselection()[0], canvasGoust,
                                         flag_for_drag_and_drop))
    Lb1.bind('<ButtonRelease-1>', lambda event: drop(event, canvasGoust, flag_for_drag_and_drop))

    photoViewFrame = Frame(rightSectionFrame, bd=3, relief=SUNKEN, background="#3c3f41", name='photoViewFrame')
    photoViewFrame.grid(row=1, column=0,sticky='NEWS')

    moveDownButton = PhotoImage(master=mainScreen,file=r"img\moveDownDis.png")
    canvasmoveDown = Canvas(mainFrame1, height=moveDownButton.height(), width=moveDownButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')

    canvasmoveDown.grid(row=0, column=0, sticky="N")

    canvasmoveDown.moveDown = moveDownButton
    moveDown_b = canvasmoveDown.create_image(moveDownButton.width()/2, moveDownButton.height()/2,anchor=CENTER, image=moveDownButton, tags="moveDown")
    move_d_flag=['moveDownDis']
    canvasmoveDown.tag_bind('moveDown', '<Button-1>', lambda event: moveDown())
    canvasmoveDown.tag_bind('moveDown', '<Enter>', lambda event: change_on_hover(event, move_d_flag[0], canvasmoveDown, moveDown_b))
    canvasmoveDown.tag_bind('moveDown', '<Leave>', lambda event: change_on_hover(event, move_d_flag[0]+'Hover', canvasmoveDown, moveDown_b))

    moveUpButton = PhotoImage(master=mainScreen,file=r"img\moveUpDis.png")
    canvasmoveUp = Canvas(mainFrame1, height=moveUpButton.height(), width=moveUpButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasmoveUp.grid(row=0, column=1, sticky="N")

    canvasmoveUp.moveUp = moveUpButton
    moveUp_b = canvasmoveUp.create_image(moveUpButton.width()/2, moveUpButton.height()/2,anchor=CENTER, image=moveUpButton, tags="moveUp")
    move_u_flag=['moveUpDis']

    canvasmoveUp.tag_bind('moveUp', '<Button-1>',lambda event: moveUp())
    canvasmoveUp.tag_bind('moveUp', '<Enter>', lambda event: change_on_hover(event, move_u_flag[0], canvasmoveUp, moveUp_b))
    canvasmoveUp.tag_bind('moveUp', '<Leave>', lambda event: change_on_hover(event, move_u_flag[0]+'Hover', canvasmoveUp, moveUp_b))

    removeButton = PhotoImage(master=mainScreen,file=r"img\remove.png")
    canvasRemove = Canvas(mainFrame1, height=removeButton.height(), width=removeButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasRemove.grid(row=0, column=2, sticky="N")

    canvasRemove.remove = removeButton
    remove_b = canvasRemove.create_image(removeButton.width()/2, removeButton.height()/2,anchor=CENTER, image=removeButton, tags="remove")
    remove_flag=['removeDis']
    canvasRemove.tag_bind('remove', '<Button-1>', lambda event: removeFunctions())
    canvasRemove.tag_bind('remove', '<Enter>', lambda event: change_on_hover(event, remove_flag[0], canvasRemove, remove_b))
    canvasRemove.tag_bind('remove', '<Leave>', lambda event: change_on_hover(event, remove_flag[0]+'Hover', canvasRemove, remove_b))

    insertBButton = PhotoImage(master=mainScreen,file=r"img\insertBDis.png")
    canvasinsertB = Canvas(mainFrame1, height=insertBButton.height(), width=insertBButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasinsertB.grid(row=0, column=3, sticky="N")

    canvasinsertB.insertb = insertBButton
    insertB= canvasinsertB.create_image(insertBButton.width()/2, insertBButton.height()/2,anchor=CENTER, image=insertBButton, tags="insertB")
    insert_b_flag = ['insertBDis']
    canvasinsertB.tag_bind('insertB', '<Button-1>', lambda event: insert_B())
    canvasinsertB.tag_bind('insertB', '<Enter>', lambda event: change_on_hover(event, insert_b_flag[0], canvasinsertB, insertB))
    canvasinsertB.tag_bind('insertB', '<Leave>',lambda event: change_on_hover(event, insert_b_flag[0]+'Hover', canvasinsertB, insertB))

    insertAButton = PhotoImage(master=mainScreen,file=r"img\insertADis.png")
    canvasinsertA = Canvas(mainFrame1, height=insertAButton.height(), width=insertAButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasinsertA.grid(row=0, column=4, sticky="N")
    canvasinsertA.inserta = insertAButton
    insert_a_flag = ['insertA']

    insertA = canvasinsertA.create_image(insertAButton.width()/2, insertAButton.height()/2,anchor=CENTER, image=insertAButton, tags="insertA")
    canvasinsertA.tag_bind('insertA', '<Button-1>', lambda event: insert_A())
    canvasinsertA.tag_bind('insertA', '<Enter>', lambda event: change_on_hover(event, insert_a_flag[0], canvasinsertA, insertA))
    canvasinsertA.tag_bind('insertA', '<Leave>', lambda event: change_on_hover(event, insert_a_flag[0]+'Hover', canvasinsertA, insertA))

    takeSButton = PhotoImage(master=mainScreen,file=r"img\TakeSDis.png")
    canvasTakeS = Canvas(mainFrame1, height=takeSButton.height(), width=takeSButton.width(), bg='#3c3f41', highlightbackground='#3c3f41')
    canvasTakeS.grid(row=0, column=5, sticky="N", padx = (0,3))
    canvasTakeS.takeS = takeSButton
    takeS_flag = ['takeSDis']
    takeS = canvasTakeS.create_image((takeSButton.width()-4)/2, takeSButton.height()/2,anchor=CENTER, image=takeSButton, tags="takeS")
    # canvasTakeS.tag_bind('takeS', '<Button-1>', lambda event: window2())
    canvasTakeS.tag_bind('takeS', '<Button-1>', lambda event: screen_shot_handle())
    canvasTakeS.tag_bind('takeS', '<Enter>', lambda event: change_on_hover(event, takeS_flag[0] , canvasTakeS, takeS))
    canvasTakeS.tag_bind('takeS', '<Leave>', lambda event: change_on_hover(event,  takeS_flag[0]+'Hover', canvasTakeS ,takeS))

    Lb2.bind("<<ListboxSelect>>", func=FocusOnSelectedFunc)

    tree = createTree(explorerFrame)

    tree.bind("<Button-3>", Treeview_right_click)

    mainScreen.protocol("WM_DELETE_WINDOW", on_closing)

    hotKeys = keyboard.GlobalHotKeys({
        '<ctrl>+c': copy_handler,
        '<ctrl>+v': paste_handler,
        '<ctrl>+x': cut_handler,
        '<ctrl>+z': redo_handler,
        '<ctrl>+y': undo_handler,
        '<delete>': delete_handler,
        '<shift>': window2,
        '<esc>': esc_handler})
    hotKeys.start()

mainScreen.mainloop()

