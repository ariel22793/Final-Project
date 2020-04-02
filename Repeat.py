import os

import Function
# from Function import Function

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
                    block.append({'name':x.name, 'img':imgdict, 'id':str(x.id),'frame':'','fatherIndex': str(x.father[0]),'fatherName':x.father[1], 'extra':x.extra.getDict()})
                else:
                    block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frame': '','fatherIndex': str(x.father[0]),'fatherName':x.father[1],
                                  'extra':''})
        return {'time':str(self.time),'functions':block}

    @classmethod
    def getExtra(cls, extra,Lb2,currentScript,tempFunction):
        functions = []
        if(len(extra['functions'])>0):
            for x in extra['functions']:
                func = Function.Function('','','','','','')
                func = Function.Function.getFunction(func,x,Lb2,currentScript,tempFunction)
                functions.append(func)
        if(extra['time'] == '?'):
            return Repeat(extra['time'],functions)
        else:
            return Repeat(int(extra['time']),functions)

    @classmethod
    def removeRepeat(cls, index,currentScript):
        fromIndex = currentScript.linesFather[index].fromIndex
        toIndex = currentScript.linesFather[index].toIndex
        place = toIndex-1
        for i in range(toIndex-1,fromIndex+1,-1):
            if(i <= place):
                if(currentScript.functions[i].name == '}'):
                    place = cls.removeRepeat(currentScript.functions[i].father[0], currentScript)
                elif(currentScript.functions[i].father != (i,currentScript.functions[i].name)):
                    currentScript.functions.pop(i)
                    currentScript.functions[fromIndex].extra.functions.pop(i-fromIndex-2)
                    currentScript.linesFather.pop(i)
        currentScript.functions.pop(fromIndex+2)
        currentScript.linesFather.pop(fromIndex+2)
        currentScript.functions.pop(fromIndex+1)
        currentScript.linesFather.pop(fromIndex+1)
        currentScript.functions.pop(fromIndex)
        currentScript.linesFather.pop(fromIndex)
        return fromIndex-1

    def changeRepeatTime(sv,Lb2,currentScript):
        index = Lb2.curselection()[0]
        currentScript.functions[index].extra.time = int(sv.get())
        currentScript.functions[index].name = "Repeat"
        Lb2.delete(index)
        Lb2.insert(index,
                   currentScript.functions[index].name + '({})'.format(currentScript.functions[index].extra.time))
        Lb2.selection_set(index)
        return True