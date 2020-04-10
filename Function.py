import Photo
from Photo import Photo
import Repeat
import Sleep
from Sleep import Sleep
import IfExist
from IfExist import IfExist
import IfNotExist
from IfNotExist import IfNotExist
import Else
from Else import Else
from tkinter import *


class Function():
    def __init__(self, name, img, id,frameFather, frame, father,extra,indention=0):
        self.name = name
        self.img = img
        self.id = id
        self.frameFather = frameFather
        self.frame = self.getFrame(name,frame,frameFather)
        self.father = father
        self.extra = extra
        self.indention = indention


    def getFunction(self,func,Lb2,currentScript,tempFunction,rightSectionFrame):
        extra = ''
        img = ''
        frame = ''

        if(func['img'] != ''):
            img = Photo.getImg(func['img'])
        if (func['extra'] != ''):
            if(func['name'] == 'Repeat'):
                extra = Repeat.Repeat.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame)
            elif (func['name'] == 'Sleep'):
                extra = Sleep.getExtra(func['extra'])
            elif (func['name'] == 'If-Exist'):
                extra = IfExist.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame)
            elif (func['name'] == 'If-Not-Exist'):
                extra = IfNotExist.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame)
            elif (func['name'] == 'Else'):
                extra = Else.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame)
        if (func['name'] != '{' and func['name'] != '}'):
            frame = self.getFrame(func['name'],'',rightSectionFrame)
            if (func['name'] == 'Repeat'):
                self.getInputBox(extra, frame.children.get('label'), frame.children.get('input'),
                            Repeat.Repeat.changeRepeatTime,Lb2,currentScript)
            elif(func['name'] == 'Sleep'):
                self.getInputBox(extra, frame.children.get('label'), frame.children.get('input'),
                            Sleep.changeSleepTime,Lb2,currentScript)
        if(tempFunction[int(func['id'])] == 0):
            function = Function(func['name'], img, int(func['id']),rightSectionFrame, frame,
                                (int(func['fatherIndex']), func['fatherName']), extra,int(func['indention']))
            tempFunction[int(func['id'])] = function
            return function
        else:
            return tempFunction[int(func['id'])]


    def printFunction(self):
        temp = 'name:' + str(self.name) + ', id:' + str(self.id) + ', img:' + str(self.img) + ', father:' + str(self.father)
        return(temp)

    def hasFather(self):           ## check if the function has father
        if self.father != (self.id, self.name):
            return True
        else:
            return False

    def getFrame(self,functionName,frame,fatherFrame):
        if(frame != ''):
            return frame
        if(functionName == ''):
            return ''
        frame1 = Frame(fatherFrame, bd=3, relief=SUNKEN, bg='white')
        frame1.grid(row=1, column=0, sticky='NEWS')
        functionNameLabel = Label(frame1, text='Function Name : {}'.format(functionName))
        if functionName == 'Sleep' or functionName == 'Repeat':
            functionNameLabel.place(x=50, y=50)
            Frame(frame1, width=200, height=30, bg='white', name='label')
            Frame(frame1, width=200, height=30, bg='white', name='input')
        else:
            fileNameLabel = Label(frame1, text='File Name : ', name='fileName')
            functionNameLabel.place(x=50, y=200)
            fileNameLabel.place(x=50, y=250)
            littlePhoto = Frame(frame1, bd=2, relief=SUNKEN, width=437, height=150, bg='white', name='canvasFrame')
            littlePhoto.place(x=0, y=0)
        return frame1

    def getInputBox(self,function, frameLabel, frameInput, eventFunction,Lb2,currentScript):
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
                entry.bind('<Return>', (lambda _: eventFunction(entry,Lb2,currentScript)))
                entry.pack()
                entry.place(x=0, y=0)