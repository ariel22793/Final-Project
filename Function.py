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
import InsertInput
from InsertInput import InsertInput
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
            elif (func['name'] == 'Insert-Input'):
                extra = InsertInput.getExtra(func['extra'])
        if (func['name'] != '{' and func['name'] != '}'):
            frame = self.getFrame(func['name'],'',rightSectionFrame)
            if (func['name'] == 'Repeat'):
                self.getInputBox(func['name'],extra, frame.children.get('labelAndInput'),
                            Repeat.Repeat.changeRepeatTime,Lb2,currentScript)
            elif(func['name'] == 'Sleep'):
                self.getInputBox(func['name'],extra, frame.children.get('labelAndInput'),
                            Sleep.changeSleepTime,Lb2,currentScript)
            elif (func['name'] == 'Insert-Input'):
                self.getInputBox(func['name'], extra, frame.children.get('labelAndInput'),
                                 InsertInput.changeInsertInputText, Lb2, currentScript)
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
        # if(functionName == ''):
        #     return ''
        frame1 = Frame(fatherFrame, bg='#2b2b2b')
        frame1.columnconfigure(0,weight = 1)
        frame1.grid(row=1, column=0, sticky='NEWS')
        functionNameLabel = Label(frame1, text='Function Name : {}'.format(functionName))
        if functionName == 'Sleep' or functionName == 'Repeat':
            functionNameLabel.grid(row = 0 , column = 0,sticky = 'WN',padx = 50 , pady = 15)
            tempFrame = Frame(frame1, height=30, bg='#2b2b2b', name='labelAndInput')
            tempFrame.grid(row=2, column=0, sticky='WNE', padx=50, pady=15)
            tempFrame1 = Frame(tempFrame, width=200, height=30, name='label')
            tempFrame1.grid(row = 1 , column = 0,sticky = 'NE',padx = 1, pady = 15)
            tempFrame2 = Frame(tempFrame, width=200, height=30, name='input')
            tempFrame2.grid(row=2, column=0, sticky='NW' ,padx = 1, pady = 15)
        elif(functionName == 'Insert-Input'):
            littlePhoto = Frame(frame1, bd=2, relief=SUNKEN,height=150, bg='#2b2b2b', name='canvasFrame')
            littlePhoto.columnconfigure(0, weight=1)
            littlePhoto.grid(row = 0 , column = 0,sticky = 'EWN', pady = (0,15))
            canvas = Canvas(littlePhoto, height=150, bg='#2b2b2b', name='canvas')
            canvas.grid(sticky='NWE')
            functionNameLabel.grid(row = 1 , column = 0,sticky = 'WN',padx = 50 , pady = 15)
            tempFrame = Frame(frame1, height=30, bg='#2b2b2b', name='labelAndInput')
            tempFrame.grid(row=2, column=0, sticky='WNE',padx = 50 , pady = 15)
            tempFrame1 = Frame(tempFrame, width=200, height=30, bg='white', name='label')
            tempFrame1.grid(row=0, column=0, sticky='N' ,padx = 1, pady = 15)
            tempFrame2 = Frame(tempFrame, width=200, height=30, name='input')
            tempFrame2.grid(row=0, column=1, sticky='N',padx = 1, pady = 15)
        elif (functionName == 'Else'):
            fileNameLabel = Label(frame1, text='File Name : ', name='fileName')
            functionNameLabel.grid(row=0, column=0, sticky='WN', padx=50, pady=15)
            fileNameLabel.grid(row=1, column=0, sticky='WN', padx=50, pady=15)
        else:
            littlePhoto = Frame(frame1, bd=2, relief=SUNKEN, height=150, bg='#2b2b2b', name='canvasFrame')
            littlePhoto.columnconfigure(0,weight=1)
            littlePhoto.grid(row = 0 , column = 0,sticky = 'EWN', pady = (0,15))
            canvas = Canvas(littlePhoto, height=150, bg='#2b2b2b', name='canvas')
            canvas.grid(sticky='NWE')
            fileNameLabel = Label(frame1, text='File Name : ', name='fileName')
            functionNameLabel.grid(row = 1 , column = 0,sticky = 'WN',padx = 50 , pady = 15)
            fileNameLabel.grid(row = 2 , column = 0,sticky = 'WN',padx = 50 , pady = 15)

        return frame1

    def getInputBox(self,functionName,function, frameLabelAndInput, eventFunction,Lb2,currentScript):
        count = 0
        for attr in dir(function):
            if not callable(getattr(function, attr)) and not attr.startswith("__") and attr != 'functions':
                count += 1
                frameLabel = frameLabelAndInput.children.get('label')
                frameInput = frameLabelAndInput.children.get('input')

                if(functionName == 'Insert-Input'):
                    frameLabel.grid(row=0, column=0, sticky='NE')
                    label = Label(frameLabel, text=attr.capitalize() + ' :',bg='white')
                    label.grid(row=0, column=0, sticky='N')

                    frameInput.grid(row=0, column=1, sticky='NW')
                    sv = StringVar(value=function.text)
                    entry = Entry(frameInput, textvariable=sv)
                    entry.bind('<Return>', (lambda _: eventFunction(entry,Lb2,currentScript)))
                    entry.grid(row=0, column=0, sticky='N')
                else:
                    frameLabel.grid(row = 0 , column = 0,sticky = 'NE')
                    label = Label(frameLabel, text=attr.capitalize() + ' :',bg='white')
                    label.grid(row =0 , column = 0,sticky = 'N')

                    frameInput.grid(row = 0 , column = 1,sticky = 'NW')
                    sv = StringVar(value=function.time)
                    entry = Entry(frameInput, textvariable=sv)
                    entry.bind('<Return>', (lambda _: eventFunction(entry, Lb2, currentScript)))
                    entry.grid(row=0, column=0, sticky='N')

