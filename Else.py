import os

import Function
# from Function import Function
import LineFather
from LineFather import LineFather

class Else():
    def __init__(self, functions):
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
                    block.append({'name':x.name, 'img':imgdict, 'id':str(x.id),'frame':'','fatherIndex': str(x.father[0]),'fatherName':x.father[1], 'extra':x.extra.getDict(),'indention':x.indention})
                else:
                    block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '','fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                                  'extra':'','indention':x.indention})
        return {'functions':block}

    @classmethod
    def getExtra(cls, extra,Lb2,currentScript,tempFunction):
        functions = []
        if(len(extra['functions'])>0):
            for x in extra['functions']:
                func = Function.Function('','','','','','','')
                func = Function.Function.getFunction(func,x,Lb2,currentScript,tempFunction)
                functions.append(func)
        return Else(functions)

    @classmethod
    def removeElse(cls,removeFuncFatherIndex, index,currentScript,haveFather):
        fromIndex = currentScript.linesFather[index].fromIndex
        toIndex = currentScript.linesFather[index].toIndex
        place = toIndex-1
        for i in range(toIndex-1,fromIndex+1,-1):
            if(i <= place):
                if(currentScript.functions[i].name == '}'):
                    if currentScript.functions[i].father[1] == 'Repeat':
                        place = currentScript.functions[currentScript.functions[i].father[0]].extra.removeRepeat(removeFuncFatherIndex,
                            currentScript.functions[i].father[0], currentScript,haveFather)
                    elif currentScript.functions[i].father[1] == 'If-Exist':
                        place = currentScript.functions[currentScript.functions[i].father[0]].extra.removeIfExist(removeFuncFatherIndex,currentScript.functions[i].father[0], currentScript,haveFather)
                    elif currentScript.functions[i].father[1] == 'If-Not-Exist':
                        place = currentScript.functions[currentScript.functions[i].father[0]].extra.removeIfNotExist(removeFuncFatherIndex,
                            currentScript.functions[i].father[0], currentScript,haveFather)
                    elif currentScript.functions[i].father[1] == 'Else':
                        place = cls.removeElse(removeFuncFatherIndex,currentScript.functions[i].father[0], currentScript,haveFather)
                elif(currentScript.functions[i].father != (i,currentScript.functions[i].name)):
                    currentScript.functions.pop(i)
                    if haveFather == True:
                        currentScript.functions[removeFuncFatherIndex].extra.functions.pop(i - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
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
            currentScript.functions[removeFuncFatherIndex].extra.functions.pop(
                (fromIndex + 2) - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
            currentScript.functions[removeFuncFatherIndex].extra.functions.pop(
                (fromIndex + 1) - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
            currentScript.functions[removeFuncFatherIndex].extra.functions.pop(
                fromIndex - (currentScript.linesFather[removeFuncFatherIndex].fromIndex + 2))
            currentScript.linesFather[removeFuncFatherIndex].toIndex -= 3
            if len(currentScript.functions[removeFuncFatherIndex].extra.functions) == 0:
                currentScript.functions.insert(removeFuncFatherIndex + 2,
                                               Function.Function('', '', removeFuncFatherIndex + 2,'', '',
                                                                 currentScript.functions[removeFuncFatherIndex].father,
                                                                 '', currentScript.functions[
                                                                     removeFuncFatherIndex].indention))
                currentScript.functions[removeFuncFatherIndex].extra.functions.append(
                    Function.Function('', '', removeFuncFatherIndex + 2,'', '',
                                      currentScript.functions[removeFuncFatherIndex].father, '',
                                      currentScript.functions[removeFuncFatherIndex].indention))
                currentScript.linesFather.insert(removeFuncFatherIndex + 2,
                                                 LineFather(currentScript.linesFather[removeFuncFatherIndex].fromIndex,
                                                            currentScript.linesFather[removeFuncFatherIndex].toIndex,
                                                            currentScript.linesFather[
                                                                removeFuncFatherIndex].fatherName))
                currentScript.linesFather[removeFuncFatherIndex].toIndex += 1

        return fromIndex-1

    def changeElse(sv,Lb2,currentScript):
        index = Lb2.curselection()[0]
        currentScript.functions[index].extra.time = int(sv.get())
        currentScript.functions[index].name = "Repeat"
        Lb2.delete(index)
        shift = ' ' * currentScript.functions[index].indention * 5
        Lb2.insert(index,
                   shift + currentScript.functions[index].name + '({})'.format(currentScript.functions[index].extra.time))
        Lb2.selection_set(index)
        return True