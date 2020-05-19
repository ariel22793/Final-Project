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
import Scan_Text_Compare
from Scan_Text_Compare import Scan_Text_Compare
from tkinter import *
from win32api import GetSystemMetrics
import tkinter.ttk as ttk
import os
import json


class Function():
    def __init__(self, name, img, id,frameFather, frame, father,extra,currentScript,tree,Lb2,photoViewFrame,indention=0):
        self.name = name
        self.img = img
        self.id = id
        self.frameFather = frameFather
        self.father = father
        self.extra = extra
        self.indention = indention
        self.frame = self.getFrame(name, frame, frameFather, currentScript, tree, Lb2, photoViewFrame)


    def getFunction(self,func,Lb2,currentScript,tempFunction,rightSectionFrame,tree,photoViewFrame):
        extra = ''
        img = ''
        frame = ''

        self.name = func['name']
        self.id = int(func['id'])
        self.father = (int(func['fatherIndex']), func['fatherName'])
        self.indention = int(func['indention'])


        if(func['img'] != ''):
            img = Photo.getImg(func['img'])
            self.img = img
        if (func['extra'] != ''):
            if(func['name'] == 'Repeat'):
                extra = Repeat.Repeat.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame,photoViewFrame,tree)
                self.extra=extra
            elif (func['name'] == 'Sleep'):
                extra = Sleep.getExtra(func['extra'])
                self.extra = extraself.extra=extra
            elif (func['name'] == 'If-Exist'):
                extra = IfExist.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame,photoViewFrame,tree)
                self.extra = extra
            elif (func['name'] == 'If-Not-Exist'):
                extra = IfNotExist.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame,photoViewFrame,tree)
                self.extra = extra
            elif (func['name'] == 'Else'):
                extra = Else.getExtra(func['extra'],Lb2,currentScript,tempFunction,rightSectionFrame,photoViewFrame,tree)
                self.extra = extra
            elif (func['name'] == 'Insert-Input'):
                extra = InsertInput.getExtra(func['extra'])
                self.extra = extra
            elif (func['name'] == 'Scan Text & Compare'):
                extra = Scan_Text_Compare.getExtra(func['extra'])
                self.extra = extra
        if (func['name'] != '{' and func['name'] != '}'):
            frame = self.getFrame(func['name'],'',rightSectionFrame,currentScript,tree,Lb2,photoViewFrame)
            if (func['name'] == 'Repeat'):
                self.getInputBox(func['name'],extra, frame.children.get('labelAndInput'),
                            Repeat.Repeat.changeRepeatTime,Lb2,currentScript)
            elif(func['name'] == 'Sleep'):
                self.getInputBox(func['name'],extra, frame.children.get('labelAndInput'),
                            Sleep.changeSleepTime,Lb2,currentScript)
            elif (func['name'] == 'Insert-Input'):
                self.getInputBox(func['name'], extra, frame.children.get('labelAndInput'),
                                 InsertInput.changeInsertInputText, Lb2, currentScript)
            elif (func['name'] == 'If-Exist'):
                self.getInputBox(func['name'], extra, frame.children.get('labelAndInput'),
                                 InsertInput.changeInsertInputText, Lb2, currentScript)
            elif (func['name'] == 'If-Not-Exist'):
                self.getInputBox(func['name'], extra, frame.children.get('labelAndInput'),
                                 InsertInput.changeInsertInputText, Lb2, currentScript)
            elif (func['name'] == 'Scan Text & Compare'):
                self.getInputBox(func['name'], extra, frame.children.get('labelAndInput'),
                                 Scan_Text_Compare.changeScan_Text_Compare, Lb2, currentScript)
        if(tempFunction[int(func['id'])] == 0):
            function = Function(func['name'], img, int(func['id']),rightSectionFrame, frame,
                                (int(func['fatherIndex']), func['fatherName']), extra,currentScript,tree,Lb2,photoViewFrame,int(func['indention']))
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
    def changeImageName(self,currentScript,tree,Lb2,photoViewFrame):
        changeImageNameWindow = Toplevel()
        changeImageNameWindow.geometry('250x35')
        changeImageNameWindow.title("Rename")
        changeImageNameWindow.configure(background='#3c3f41')
        x, y = self.getCenterOfScreen(changeImageNameWindow)
        changeImageNameWindow.geometry("250x35+" + str(x) + '+' + str(y))

        frame = Frame(changeImageNameWindow, bd=3, bg='#3c3f41')
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        frame.grid(row=0, column=0, sticky='WEN')

        label = Label(frame, text="Rename:", fg="white",bg='#3c3f41' )
        label.grid(row=0, column=0, sticky='WEN',pady=5)

        inputName = StringVar()
        input = Entry(frame,textvariable=inputName)
        input.grid(row=0, column=1, sticky='WEN',padx=5,pady=5)

        button = Button(frame,text='Rename',command= lambda: self.changeHandler(inputName,currentScript,tree,Lb2,photoViewFrame,changeImageNameWindow))
        button.grid(row=0, column=2, sticky='WE')

    def changeHandler(self,inputName,currentScript,tree,Lb2,photoViewFrame,changeImageNameWindow):
        if(inputName.get() != ''):
            if not os.path.exists(currentScript.path +'ScreenShots\\' + inputName.get() + '.png'):
                self.changeInDirectory(inputName, currentScript)
                self.changeInCurrentScript(inputName,currentScript)
                self.FocusOnSelectedFunc(Lb2,currentScript,self.id,photoViewFrame)

                for i in tree.get_children(): #clear treeView
                    tree.delete(i)

                root = tree.insert('', 'end', text=currentScript.name, open=True, tag='T')
                self.SUBS(currentScript.path,root,tree)
                self.saveHundle(currentScript)
                changeImageNameWindow.destroy()
            else:
                print('there image with the same name')

    def changeInDirectory(self,inputName,currentScript):
        os.rename(currentScript.path +'ScreenShots\\' + currentScript.functions[self.id].img.img,currentScript.path +'ScreenShots\\' + inputName.get() + '.png')
    def changeInCurrentScript(self,inputName,currentScript):
        index = self.id
        currentScript.functions[index].img.img = inputName.get() + '.png'
        if(currentScript.functions[index].father[0] != index):
            fatherIndex = currentScript.functions[index].father[0]
            tempLineFather = currentScript.linesFather[fatherIndex]
            tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

            while True:
                tempFatherFunction.extra.functions[index - tempLineFather.fromIndex - 2].img.img = inputName.get() + '.png'
                if tempFatherFunction.father[0] == tempFatherFunction.id:
                    break
                tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

    def saveHundle(self,currentScript):
        functionPath = currentScript.path + "/functions.json"
        try:
            os.remove(functionPath)
        except:
            pass
        functionsblock = self.saveFunctions(currentScript)
        linesFatherblock = self.saveLinesFather(currentScript)
        with open(functionPath, 'w+') as outfile:
            outfile.write(json.dumps(functionsblock) + '\n' + json.dumps(linesFatherblock))

    def saveFunctions(self,currentScript):
        block = []
        for x in currentScript.functions:
            if (x.img != ''):
                imgdict = x.img.getDict()
            else:
                imgdict = ''
            if (x.extra != ''):
                block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frameFather': '', 'frame': '',
                                'fatherIndex': str(x.father[0]), 'fatherName': x.father[1],
                                'extra': x.extra.getDict(), 'indention': x.indention})
            else:
                block.append({'name': x.name, 'img': imgdict, 'id': str(x.id), 'frameFather': '', 'frame': '',
                                'fatherIndex': str(x.father[0]), 'fatherName': x.father[1],
                                'extra': '', 'indention': x.indention})
        return block

    def saveLinesFather(self,currentScript):
        block = []
        for x in currentScript.linesFather:
            block.append({'fatherName': x.fatherName, 'fromIndex': x.fromIndex, 'toIndex': x.toIndex})
        return block

    def getCenterOfScreen(self,screen):
        screen.update()
        h = screen.winfo_height()
        w = screen.winfo_width()
        wScreen = GetSystemMetrics(0)
        hScreen = GetSystemMetrics(1)
        xPoint = (wScreen / 2) - (w / 2)
        yPoint = hScreen / 2 - h / 2
        return (int(xPoint), int(yPoint))

    def getFrame(self,functionName,frame,fatherFrame,currentScript,tree,Lb2,photoViewFrame):
        if(frame != ''):
            return frame
        # if(functionName == ''):
        #     return ''
        frame1 = Frame(fatherFrame, bg='#2b2b2b')
        frame1.columnconfigure(0,weight = 1)
        frame1.grid(row=1, column=0, sticky='NEWS')
        functionNameLabel = Label(frame1, text='Function Name : {}'.format(functionName),bg='#2b2b2b',fg = 'white' )
        if functionName == 'Sleep' or functionName == 'Repeat':
            functionNameLabel.grid(row = 0 , column = 0,sticky = 'WN',padx = (50,0) , pady = 15)
            tempFrame = Frame(frame1, height=30, bg='#2b2b2b', name='labelAndInput')
            tempFrame.grid(row=2, column=0, sticky='WNE', padx=50, pady=15)
            tempFrame1 = Frame(tempFrame, width=200, height=30, name='label',bg='#2b2b2b')
            tempFrame1.grid(row = 1 , column = 0,sticky = 'NE',padx = 1, pady = 15)
            tempFrame2 = Frame(tempFrame, width=10, height=30, name='input')
            tempFrame2.grid(row=2, column=0, sticky='NW' ,padx = 1, pady = 15)
        elif(functionName == 'Insert-Input' or functionName == 'Scan Text & Compare'):
            littlePhoto = Frame(frame1, bd=2, relief=SUNKEN,height=150, bg='#2b2b2b', name='canvasFrame')
            littlePhoto.columnconfigure(0, weight=1)
            littlePhoto.grid(row = 0 , column = 0,sticky = 'EWN', pady = (0,15))
            canvas = Canvas(littlePhoto, height=150, bg='#2b2b2b', name='canvas')
            canvas.grid(sticky='NWE')
            functionNameLabel.grid(row = 1 , column = 0,sticky = 'WN',padx = 50 , pady = 15)
            tempFrame = Frame(frame1, height=30, bg='#2b2b2b', name='labelAndInput')
            tempFrame.grid(row=2, column=0, sticky='WNE',padx = 50 , pady = 15)
            tempFrame1 = Frame(tempFrame, width=200, height=30, bg='#2b2b2b', name='label')
            tempFrame1.grid(row=0, column=0, sticky='N' ,padx = 1, pady = 15)
            tempFrame2 = Frame(tempFrame, width=200, height=30, name='input')
            tempFrame2.grid(row=0, column=1, sticky='N',padx = 1, pady = 15)
            fileNameFrame = Frame(frame1, bg='#2b2b2b', name='fileNameFrame')
            fileNameFrame.columnconfigure(0, weight=1)
            fileNameFrame.columnconfigure(1, weight=1)
            fileNameFrame.grid(row=3, column=0, sticky='WEN', pady=15)
            fileNameLabel = Label(fileNameFrame, text='File Name : ', name='fileName',bg='#2b2b2b',fg = 'white')
            fileNameLabel.grid(row=0, column=0, sticky='WN', padx=(50, 25))
            fileNameButton = Button(fileNameFrame, width=20, text='Change Image Name',state = DISABLED,name = 'fileNameButton',command = lambda: self.changeImageName(currentScript,tree,Lb2,photoViewFrame),bg='#2b2b2b',fg = 'white')
            fileNameButton.grid(row=0, column=1, sticky='EN', padx=(25, 50))

        elif (functionName == 'If-Exist' or functionName == 'If-Not-Exist' ):
            littlePhoto = Frame(frame1, bd=2, relief=SUNKEN, height=150, bg='#2b2b2b', name='canvasFrame')
            littlePhoto.columnconfigure(0, weight=1)
            littlePhoto.grid(row=0, column=0, sticky='EWN', pady=(0, 15))
            canvas = Canvas(littlePhoto, height=150, bg='#2b2b2b', name='canvas')
            canvas.grid(sticky='NWE')
            functionNameLabel.grid(row=1, column=0, sticky='WN', padx=50, pady=15)
            tempFrame = Frame(frame1, height=30, bg='#2b2b2b', name='labelAndInput')
            tempFrame.grid(row=4, column=0, sticky='WNE', padx=50, pady=15)
            tempFrame1 = Frame(tempFrame, width=200, height=30, name='label', bg='#2b2b2b')
            tempFrame1.grid(row=1, column=0, sticky='NE', padx=1, pady=15)
            tempFrame2 = Frame(tempFrame, width=10, height=30, name='input')
            tempFrame2.grid(row=2, column=0, sticky='NW', padx=1, pady=15)
            radioFrame = Frame(frame1, bg='#2b2b2b')
            radioFrame.columnconfigure(0, weight=1)
            radioFrame.columnconfigure(1, weight=1)
            radioFrame.grid(row=2, column=0, sticky='WNE', padx=50, pady=15)
            if self.extra.compareState == 'image':
                buttonImage = Button(radioFrame,text='Image' ,command = lambda : self.radio_button_handle('image',tempFrame,buttonImage,buttonText,Lb2),bg='white',fg='#2b2b2b')
                buttonImage.grid(row=0, column=0, sticky='WN', padx=(50, 25))
                buttonText = Button(radioFrame,text='Text',command = lambda : self.radio_button_handle('text',tempFrame,buttonImage,buttonText,Lb2),bg='#2b2b2b',fg='white')
                buttonText.grid(row=0, column=1, sticky='WN', padx=(50, 25))
            else:
                buttonImage = Button(radioFrame, text='Image',
                                     command=lambda: self.radio_button_handle('image', tempFrame, buttonImage,
                                                                              buttonText,Lb2), bg='#2b2b2b', fg='white')
                buttonImage.grid(row=0, column=0, sticky='WN', padx=(50, 25))
                buttonText = Button(radioFrame, text='Text',
                                    command=lambda: self.radio_button_handle('text', tempFrame, buttonImage,
                                                                             buttonText,Lb2), bg='white', fg='#2b2b2b')
                buttonText.grid(row=0, column=1, sticky='WN', padx=(50, 25))
            # var = StringVar(radioFrame)
            # radioFrame.grid(row=2, column=0, sticky='WNE', padx=50, pady=15)
            # R1 = Radiobutton(radioFrame, text="Image", variable=var, value='A',  bg='#2b2b2b', indicatoron=0, command = lambda : self.radio_button_handle('image',tempFrame))
            # R1.grid(row=0, column=0, sticky='WN', padx=(50, 25))
            # R2 = Radiobutton(radioFrame, text="Text", variable=var, value='B', bg='#2b2b2b',  indicatoron=0, command = lambda : self.radio_button_handle('text',tempFrame))
            # R2.grid(row=0, column=1, sticky='WN', padx=(50, 25))
            # R1.select()
            fileNameFrame = Frame(frame1, bg='#2b2b2b', name='fileNameFrame')
            fileNameFrame.columnconfigure(0, weight=1)
            fileNameFrame.columnconfigure(1, weight=1)
            fileNameFrame.grid(row=3, column=0, sticky='WEN', pady=15)
            fileNameLabel = Label(fileNameFrame, text='File Name : ', name='fileName', bg='#2b2b2b', fg='white')
            fileNameLabel.grid(row=0, column=0, sticky='WN', padx=(50, 25))
            fileNameButton = Button(fileNameFrame, width=20, text='Change Image Name', state=DISABLED,name='fileNameButton',command=lambda: self.changeImageName(currentScript, tree, Lb2, photoViewFrame),bg='#2b2b2b', fg='white')
            fileNameButton.grid(row=0, column=1, sticky='EN', padx=(25, 50))


        elif (functionName == 'Else' ):
            functionNameLabel.grid(row=0, column=0, sticky='WN', padx=50, pady=15)
        else:
            littlePhoto = Frame(frame1, bd=2, relief=SUNKEN, height=150, bg='#2b2b2b', name='canvasFrame')
            littlePhoto.columnconfigure(0,weight=1)
            littlePhoto.grid(row = 0 , column = 0,sticky = 'EWN', pady = (0,15))
            canvas = Canvas(littlePhoto, height=150, bg='#2b2b2b', name='canvas')
            canvas.grid(sticky='NWE')
            functionNameLabel.grid(row=1, column=0, sticky='WN', padx=50, pady=15)
            fileNameFrame = Frame(frame1,bg = '#2b2b2b', name='fileNameFrame')
            fileNameFrame.columnconfigure(0,weight=1)
            fileNameFrame.columnconfigure(1,weight=1)
            fileNameFrame.grid(row = 2 , column = 0,sticky = 'WEN', pady = 15)
            fileNameLabel = Label(fileNameFrame, text='File Name : ', name='fileName',bg='#2b2b2b',fg = 'white')
            fileNameLabel.grid(row = 0 , column = 0,sticky = 'WN',padx = (50,25))
            fileNameButton = Button(fileNameFrame,width =20,text = 'Change Image Name',state = DISABLED,name = 'fileNameButton',command = lambda: self.changeImageName(currentScript,tree,Lb2,photoViewFrame),bg='#2b2b2b',fg = 'white')
            fileNameButton.grid(row=0, column=1, sticky='EN', padx=(25,50))

        return frame1


    def getInputBox(self,functionName,function, frameLabelAndInput, eventFunction,Lb2,currentScript):
        count = 0
        for attr in dir(function):
            if not callable(getattr(function, attr)) and not attr.startswith("__") and attr != 'functions':
                count += 1
                frameLabel = frameLabelAndInput.children.get('label')
                frameInput = frameLabelAndInput.children.get('input')

                if(functionName == 'Insert-Input' or functionName == 'Scan Text & Compare'):
                    frameLabel.grid(row=0, column=0, sticky='NE')
                    label = Label(frameLabel, text='Text:',bg='#2b2b2b',fg='white')
                    label.grid(row=0, column=0, sticky='N')

                    frameInput.grid(row=0, column=1, sticky='NW')
                    sv = StringVar(value=function.text)
                    entry = Entry(frameInput, textvariable=sv,bg='#2b2b2b',fg='white',name = 'entry',disabledbackground = '#2b2b2b')
                    entry.bind('<Return>', (lambda _: eventFunction(entry,Lb2,currentScript)))
                    entry.grid(row=0, column=0, sticky='N')
                elif (functionName == 'If-Exist' or functionName == 'If-Not_Exist'):
                    frameLabel.grid(row=0, column=0, sticky='NE')
                    label = Label(frameLabel, text='Text:', bg='#2b2b2b', fg='white')
                    label.grid(row=0, column=0, sticky='N')
                    frameInput.grid(row=0, column=1, sticky='NW')
                    sv = StringVar(value=function.text)
                    if(self.extra.compareState == 'image'):
                        entry = Entry(frameInput, textvariable=sv, bg='#2b2b2b',state='disabled', fg='white',name = 'entry',disabledbackground = '#2b2b2b')
                    elif (self.extra.compareState == 'text'):
                        entry = Entry(frameInput, textvariable=sv, bg='#2b2b2b', fg='white',
                                          name='entry', disabledbackground='#2b2b2b')
                    entry.bind('<Return>', (lambda _: eventFunction(entry, Lb2, currentScript)))
                    entry.grid(row=0, column=0, sticky='N')
                else:
                    frameLabel.grid(row = 0 , column = 0,sticky = 'NE')
                    label = Label(frameLabel, text='Time:',bg='#2b2b2b',fg='white')
                    label.grid(row =0 , column = 0,sticky = 'N')

                    frameInput.grid(row = 0 , column = 1,sticky = 'NW')
                    sv = StringVar(value=function.time)
                    entry = Entry(frameInput, textvariable=sv,bg='#2b2b2b',fg='white',name = 'entry',disabledbackground = '#2b2b2b')
                    entry.bind('<Return>', (lambda _: eventFunction(entry, Lb2, currentScript)))
                    entry.grid(row=0, column=0, sticky='N')


    def radio_button_handle(self, value, textBox,buttonImage,buttonText,Lb2):
        name = self.name
        shift = ' ' * self.indention * 5
        Lb2.delete(self.id)
        if(value =='image' ):
            for childName, childValue in textBox.children.items():
                if(childName == 'input'):
                    for childName, childValue in childValue.children.items():
                        if(childName == 'entry'):
                            childValue.config(state='disabled')
            self.extra.compareState = 'image'
            buttonImage.config(bg='white',fg='#2b2b2b')
            buttonText.config(bg='#2b2b2b',fg='white')
            Lb2.insert(self.id, shift + name + '({})'.format(self.extra.image))


        elif (value =='text' ):
            for childName, childValue in textBox.children.items():
                if(childName == 'input'):
                    for childName, childValue in childValue.children.items():
                        if (childName == 'entry'):
                            childValue.config(state='normal')
            self.extra.compareState = 'text'
            buttonText.config(bg='white',fg='#2b2b2b')
            buttonImage.config(bg='#2b2b2b',fg='white')
            Lb2.insert(self.id, shift + name + '({},{})'.format(self.extra.image,self.extra.text))
        Lb2.itemconfig(self.id, foreground=self.getFunctionColor(name))


    def FocusOnSelectedFunc(self,Lb2,currentScript,index,photoViewFrame):
        frame = ''
        id = index
        photoName = ''
        functionName = ''  # repoFrame_and_Button[0].destroy()

        x = currentScript.functions[index]
        try:
            if (x.img != ''):
                photoName = x.img.img
            functionName = x.name
        except:
            pass
        frame = x.frame
        print(frame)
        if frame != '':
            frame.columnconfigure(0,weight = 1)
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
                        canvas = Canvas(childValue, height=150, name='canvas',bg = '#2b2b2b')
                        one = PhotoImage(file=currentScript.path + "ScreenShots\\" + photoName)
                        photoViewFrame.one = one  # to prevent the image garbage collected.
                        canvas.create_image((0, 0), image=one, anchor="nw")
                        canvas.grid(sticky = 'NWE')

            frame.tkraise()
            try:
                frame.refresh()
            except:
                pass
            Lb2.select_set(index)

    def SUBS(self,path, parent, tree):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            # tree.image = fileImg

            if os.path.isdir(abspath):
                parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")
                self.SUBS(abspath, parent_element, tree)
            else:
                parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")

    def getFunctionColor(self, funcName):
        ['#f4b63f', '#57ceff', '#ff5792', '#c2ff57', '#ff8657', '#579aff', '#d557ff', '#078f02', '#57ff7f']
        if (funcName == 'Right-Click'):
            return '#f4b63f'
        elif (funcName == 'Left-Click'):
            return '#57ceff'
        elif (funcName == 'Repeat'):
            return '#ff5792'
        elif (funcName == 'If-Exist'):
            return '#c2ff57'
        elif (funcName == 'If-Not-Exist'):
            return '#ff8657'
        elif (funcName == 'Else'):
            return '#579aff'
        elif (funcName == 'Double-Click'):
            return '#d557ff'
        elif (funcName == 'Insert-Input'):
            return '#078f02'
        elif (funcName == 'Sleep'):
            return '#57ff7f'
        elif (funcName == 'Scan_Text'):
            return 'white'
        elif (funcName == 'Scan Text_&_Compare'):
            return 'white'
        else:
            return 'white'

