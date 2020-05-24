import os
import numpy as np
import Function
# from Function import Function
import LineFather
from LineFather import LineFather



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
                    block.append({'name':x.name, 'img':imgdict, 'id':str(x.id),'frameFather':'','frame':'','fatherIndex': str(x.father[0]),'fatherName':x.father[1], 'extra':x.extra.getDict(),'indention':x.indention})
                else:
                    block.append({'name': x.name, 'img': imgdict, 'id': str(x.id),'frameFather':'', 'frame': '','fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                                  'extra':'','indention':x.indention})
        return {'time':str(self.time),'functions':block}

    @classmethod
    def getExtra(cls, extra,Lb2,currentScript,tempFunction,rightSectionFrame,tree):
        functions = []
        if(len(extra['functions'])>0):
            for x in extra['functions']:
                func = Function.Function('','','', rightSectionFrame,'','','',currentScript,tree,Lb2,photoViewFrame)
                func = Function.Function.getFunction(func,x,Lb2,currentScript,tempFunction,rightSectionFrame,tree,photoViewFrame)
                functions.append(func)
        if(extra['time'] == '?'):
            return Repeat(extra['time'],functions)
        else:
            return Repeat(int(extra['time']),functions)

    @classmethod
    def removeRepeat(cls,removeFuncFatherIndex, index,currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame):
        fromIndex = currentScript.linesFather[index].fromIndex
        toIndex = currentScript.linesFather[index].toIndex

        place = toIndex-1
        for i in range(toIndex-1,fromIndex+1,-1):
            if(i <= place):
                if(currentScript.functions[i].name == '}'):
                    if currentScript.functions[i].father[1] == 'Repeat':
                        place = cls.removeRepeat(removeFuncFatherIndex,currentScript.functions[i].father[0], currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                    elif currentScript.functions[i].father[1] == 'If-Exist':
                        place = currentScript.functions[currentScript.functions[i].father[0]].extra.removeIfExist(removeFuncFatherIndex,currentScript.functions[i].father[0], currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                    elif currentScript.functions[i].father[1] == 'If-Not-Exist':
                        place = currentScript.functions[currentScript.functions[i].father[0]].extra.removeIfNotExist(removeFuncFatherIndex,currentScript.functions[i].father[0], currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                    elif currentScript.functions[i].father[1] == 'Else':
                        place = currentScript.functions[currentScript.functions[i].father[0]].extra.removeElse(removeFuncFatherIndex,currentScript.functions[i].father[0], currentScript,haveFather,rightSectionFrame,tree,Lb2,photoViewFrame)
                elif(currentScript.functions[i].father != (i,currentScript.functions[i].name)):
                    currentScript.functions.pop(i)
                    if haveFather == True:
                        tempLineFather = currentScript.linesFather[removeFuncFatherIndex]
                        tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

                        while True:
                            tempFatherFunction.extra.functions.pop(i - tempLineFather.fromIndex - 2)
                            if tempFatherFunction.father[0] == tempFatherFunction.id:
                                break
                            tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

                        # currentScript.functions[removeFuncFatherIndex].extra.functions.pop(i - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
                        currentScript.linesFather[removeFuncFatherIndex].toIndex -= 1
                    currentScript.functions[fromIndex].extra.functions.pop(i-fromIndex-2)
                    currentScript.linesFather.pop(i)

        currentScript.functions.pop(fromIndex+2)
        currentScript.linesFather.pop(fromIndex+2)
        currentScript.functions.pop(fromIndex+1)
        currentScript.linesFather.pop(fromIndex+1)
        currentScript.functions.pop(fromIndex)
        currentScript.linesFather.pop(fromIndex)
        if haveFather == True:

            tempLineFather = currentScript.linesFather[removeFuncFatherIndex]
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

            while True:
                tempFatherFunction.extra.functions.pop((fromIndex+2) - tempLineFather.fromIndex - 2)
                tempFatherFunction.extra.functions.pop((fromIndex+1) - tempLineFather.fromIndex - 2)
                tempFatherFunction.extra.functions.pop(fromIndex - tempLineFather.fromIndex - 2)
                if tempFatherFunction.father[0] == tempFatherFunction.id:
                    break
                tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
            # currentScript.functions[removeFuncFatherIndex].extra.functions.pop((fromIndex+2) - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
            # currentScript.functions[removeFuncFatherIndex].extra.functions.pop((fromIndex+1) - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
            # currentScript.functions[removeFuncFatherIndex].extra.functions.pop(fromIndex - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
            currentScript.linesFather[removeFuncFatherIndex].toIndex -= 3


            if len(currentScript.functions[removeFuncFatherIndex].extra.functions) == 0:
                currentFunction = Function.Function('', '', removeFuncFatherIndex + 2,rightSectionFrame, '',(removeFuncFatherIndex,currentScript.functions[removeFuncFatherIndex].name),'',currentScript,tree,Lb2,photoViewFrame, currentScript.functions[
                                                                     removeFuncFatherIndex].indention+1,)
                currentScript.functions.insert(removeFuncFatherIndex + 2,currentFunction)

                tempLineFather = currentScript.linesFather[removeFuncFatherIndex]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]
                i = currentScript.linesFather[removeFuncFatherIndex].toIndex
                while True:
                    tempFatherFunction.extra.functions.insert(
                            i - tempLineFather.fromIndex - 2, currentFunction)
                    if tempFatherFunction.father[0] == tempFatherFunction.id:
                        break
                    tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                    tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

                currentScript.linesFather.insert(removeFuncFatherIndex + 2,
                                                 LineFather(currentScript.linesFather[removeFuncFatherIndex].fromIndex,
                                                            currentScript.linesFather[removeFuncFatherIndex].toIndex,
                                                            currentScript.linesFather[
                                                                removeFuncFatherIndex].fatherName))
                currentScript.linesFather[removeFuncFatherIndex].toIndex += 1
        return fromIndex-1

    def changeRepeatTime(sv,Lb2,currentScript):
        try:
            index = currentScript.lastClickOnLb2
        except:
            print('need to mark the function that you want to change')
        if (currentScript.functions[index].name == 'Repeat'):
            if(sv.get() == ''):
                currentScript.functions[index].extra.time = '?'
            else:
                currentScript.functions[index].extra.time = int(sv.get())

            Lb2.delete(index)
            shift = ' ' * currentScript.functions[index].indention * 5

            Lb2.insert(index,
                       shift + currentScript.functions[index].name + '({})'.format(currentScript.functions[index].extra.time))
            Lb2.itemconfig(index, foreground='#ff5792')
            Lb2.selection_set(index)

    def updateFunction(self,currentScript, fatherIndex):
        fatherLinesFather = currentScript.linesFather[fatherIndex]
        currentIndex = -1
        for func in range(fatherLinesFather.fromIndex + 1, fatherLinesFather.toIndex + 1):
            tempIndex = func
            if (func > currentIndex):
                currentScript.functions[func].id = func
                currentScript.functions[func].father = (fatherIndex, currentScript.functions[func].father[1])
                if (currentScript.functions[func].name == 'Repeat' or currentScript.functions[
                    func].name == 'If-Exist' or
                        currentScript.functions[func].name == 'If-Not-Exist' or currentScript.functions[
                            func].name == 'Else'):
                    currentScript.linesFather[func].fromIndex = func
                    currentScript.linesFather[func].toIndex = func + len(
                        currentScript.functions[func].extra.functions) + 2
                else:
                    currentScript.linesFather[func].fromIndex = fatherIndex
                    currentScript.linesFather[func].toIndex = fatherIndex + len(
                        currentScript.functions[fatherIndex].extra.functions) + 2

                if (currentScript.functions[func].name != '{' and currentScript.functions[
                    func].name != '}'):  # if is one of the father function not '{' or '}'
                    currentScript.functions[fatherIndex].extra.functions[func - fatherIndex - 2].id = func
                    currentScript.functions[fatherIndex].extra.functions[func - fatherIndex - 2].father = (
                    fatherIndex, currentScript.functions[func].father[1])

                if (currentScript.functions[func].name == 'Repeat' or currentScript.functions[
                    func].name == 'If-Exist' or
                        currentScript.functions[func].name == 'If-Not-Exist' or currentScript.functions[
                            func].name == 'Else'):
                    currentIndex = currentScript.functions[func].extra.updateFunction(currentScript, func)
        return func