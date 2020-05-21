import os
from tkinter import *
from PIL import Image, ImageTk
import pyautogui
import Photo
import matplotlib.pyplot as plt
from Photo import Photo
import ImgRecog


class ScreenShotWindow():
    Lb1Colors = ['#f4b63f', '#57ceff', '#ff5792', '#c2ff57', '#ff8657', '#579aff', '#d557ff', '#078f02', '#57ff7f','white', 'white']

    def __init__(self,mainScreen,Lb2,currentScript,tree,photoViewFrame,window_of_screen_shot):
        # mainScreen.iconify()


        window2 = Tk()
        window2.title("window2")
        window2.attributes('-fullscreen', True)
        window2.attributes('-alpha', 0.3)


        #tkinter.messagebox.showinfo("Notic!", "Press ENTER To Take ScreenShot\nPress ESC To Quit")
        self.width = window2.winfo_screenwidth()
        self.heigth = window2.winfo_screenheight()
        self.window_of_screen_shot = window_of_screen_shot

        self.x0, self.y0, self.x1, self.y1 = -1, -1, -1, -1
        self.canvas = Canvas(window2, width=window2.winfo_screenwidth(), height=window2.winfo_screenheight(),
                             highlightthickness=0)
        self.canvas.pack()


        self.click = 0
        self.window = window2
        window2.bind('<Button-1>', self.getMaousePosition)
        window2.bind('<Key>', lambda event :self.keyPress(event,mainScreen,Lb2,currentScript,tree,photoViewFrame))
        window2.bind('<Motion>', self.paint)
        window2.bind('<ButtonRelease-1>', self.getMaousePosition)



    def keyPress(self, event,mainScreen,Lb2,currentScript,tree,photoViewFrame):
        if str(event.keysym) == 'Return':
            if self.x0 != self.x1 and self.y0 != self.y1:
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save('Screen.png')
                img = Image.open("Screen.png")
                img1 = Image.open(currentScript.path + 'ScreenTest.png')
                img = img.crop((self.x0, self.y0, self.x1, self.y1))

                index = Lb2.curselection()[0]
                currentFunction = currentScript.functions[index]

                numberOfImages = len([name for name in os.listdir(currentScript.path + 'ScreenShots\\')])
                imgName = "Screen" + str(numberOfImages) + ".png"

                if not os.path.exists(currentScript.path + 'ScreenShots\\'):
                    os.mkdir(currentScript.path + 'ScreenShots\\')

                while os.path.exists(currentScript.path + 'ScreenShots\\' + imgName):
                    numberOfImages += 1
                    imgName = "Screen" + str(numberOfImages) + ".png"

                img.save(currentScript.path + 'ScreenShots\\' + imgName)

                img = Photo(self.x0, self.y0, self.x1, self.y1, imgName)
                # flag = ImgRecog.photoRec(currentScript.path,img1,img)
                mainScreen.state('zoomed')
                self.window.destroy()
                self.window_of_screen_shot.destroy()

                # for func in range(len(currentScript.functions)):
                #     if currentScript.functions[func].id == index:
                currentScript.functions[index].img = img
                if currentScript.functions[index].name == 'If-Exist' or \
                        currentScript.functions[index].name == 'If-Not-Exist':
                    currentScript.functions[index].extra.image = img.img
                if currentScript.functions[index].father[0] != index:
                    tempLineFather = currentScript.linesFather[currentScript.functions[index].father[0]]
                    tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]

                    while True:
                        tempFatherFunction.extra.functions[index - tempLineFather.fromIndex - 2].img = img
                        if tempFatherFunction.father[0] == tempFatherFunction.id:
                            break
                        tempLineFather = currentScript.linesFather[tempFatherFunction.father[0]]
                        tempFatherFunction = currentScript.functions[tempLineFather.fromIndex]




                        # if (currentScript.functions[func].father[1] == 'Repeat' or currentScript.functions[func].father[1] == 'If-Exist' or currentScript.functions[func].father[1] == 'If-Not-Exist' or currentScript.functions[func].father[1] == 'Else') and currentScript.functions[func].id !=currentScript.functions[func].father[0]   :
                        #     currentScript.functions[currentScript.functions[func].father[0]].extra.functions[
                        #         func - currentScript.functions[func].father[0] - 2].img = img
                Lb2.select_clear(0, END)
                self.updateLb2(index,index,'add',currentScript,Lb2)
                self.FocusOnSelectedFunc(mainScreen,Lb2,currentScript,index,photoViewFrame)

                for i in tree.get_children(): #clear treeView
                    tree.delete(i)

                root = tree.insert('', 'end', text=currentScript.name, open=True, tag='T')
                self.SUBS(currentScript.path,root,tree)


        if str(event.keysym) == 'Escape':
            print("Quit window")
            mainScreen.state('zoomed')
            self.window.destroy()
            self.window_of_screen_shot.destroy()

        else:
            pass


    def paint(self, event):
        if self.click == 1:
            self.x1, self.y1 = event.x, event.y
            self.canvas.delete('all')
            self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline='black')  # inner

            self.canvas.create_rectangle(0, 0, self.x0, self.heigth, fill='red', outline='red')  # outter
            self.canvas.create_rectangle(self.x0, 0, self.x1, self.y0, fill='red', outline='red')  # outter
            self.canvas.create_rectangle(self.x0, self.y1, self.width, self.heigth, fill='red', outline='red')  # outter
            self.canvas.create_rectangle(self.x1, 0, self.width, self.heigth, fill='red', outline='red')  # outter



    def getMaousePosition(self, event):
        if (str(event.type) == 'ButtonPress'):
            self.click = 1
            self.x0, self.y0 = event.x, event.y
        else:
            self.click = 2
            self.x1, self.y1 = event.x, event.y

    def FocusOnSelectedFunc(self,mainScreen,Lb2,currentScript,index,photoViewFrame):

        mainScreen.update_idletasks()

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
            # self.markCurrentFuncArea(index,currentScript,Lb2)
        # reportFrame()

    def SUBS(self,path, parent, tree):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            # tree.image = fileImg

            if os.path.isdir(abspath):
                parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")
                self.SUBS(abspath, parent_element, tree)
            else:
                parent_element = tree.insert(parent, 'end', text=p, open=True, tag="T")

    def getFunctionColor(self,funcName):
        if (funcName == 'Right-Click'):
            return '#f4b63f'
        elif (funcName == 'Left-Click'):
            return  '#57ceff'
        elif (funcName == 'Repeat'):
            return '#ff5792'
        elif (funcName == 'If-Exist'):
            return'#c2ff57'
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
        elif (funcName == 'Exit'):
            return 'white'
        elif (funcName == 'Move-To'):
            return 'white'
        else:
            return 'white'

    def updateLb2(self,fromIndex, toIndex, operation,currentScript,Lb2, options='regular'):
        vw = Lb2.yview()
        if (options == 'deleteBefore'):
            Lb2.delete(0, 'end')
        highestNumDigit = len(str(len(currentScript.functions)))

        if (operation == 'add' or operation == 'replace'):
            for x in range(fromIndex, toIndex + 1):
                textColor = self.getFunctionColor(currentScript.functions[x].name)
                currentNumDigit = len(str(x))
                if (operation == 'add'):
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
                            Lb2.insert(x, shift + name + '({},{})'.format(currentScript.functions[x].extra.image,currentScript.functions[x].extra.text))
                        else:
                            Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.image))
                        Lb2.itemconfig(x, foreground=textColor)
                    elif name == 'Insert-Input' or name == 'Scan Text & Compare':
                        Lb2.insert(x, shift + name + '("{}")'.format(
                            currentScript.functions[x].extra.text))
                        Lb2.itemconfig(x, foreground=textColor)
                    else:
                        Lb2.insert(x, shift + name)
                        Lb2.itemconfig(x, foreground=textColor)

                elif (operation == 'replace'):
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
                            Lb2.insert(x, shift + name + '({},{})'.format(currentScript.functions[x].extra.image,currentScript.functions[x].extra.text))
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
            Lb2.update()
        elif (operation == 'remove'):
            for x in range(toIndex, fromIndex - 1, -1):
                # textColor = getFunctionColor(currentScript.functions[x].name)
                Lb2.delete(x)
                if (x == fromIndex and x <= len(currentScript.functions) - 1 and (
                        currentScript.functions[x].indention > 0 or (
                        len(currentScript.functions) == 1 and currentScript.functions[0].name == ''))):
                    shift = ' ' * currentScript.functions[x].indention * 5
                    Lb2.insert(x, shift + '')
                    Lb2.itemconfig(x, foreground='white')

            Lb2.update()
        Lb2.yview_moveto(vw[0])

    def markCurrentFuncArea(self,index,currentScript,Lb2):
        fromindex = currentScript.linesFather[index].fromIndex
        toIndex = currentScript.linesFather[index].toIndex
        for i in range(len(currentScript.functions)):
            tempFunc = currentScript.functions[i]
            if (fromindex <= i <= toIndex):
                if (tempFunc.name == 'Right-Click'):
                    Lb2.itemconfig(i, bg='#f4b63f')
                elif (tempFunc.name == 'Left-Click'):
                    Lb2.itemconfig(i, bg='#57ceff')
                elif (tempFunc.name == 'Repeat' or (
                        (tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '') and tempFunc.father[
                    1] == 'Repeat')):
                    Lb2.itemconfig(i, bg='#ff5792')
                elif (tempFunc.name == 'If-Exist' or (
                        (tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '') and tempFunc.father[
                    1] == 'If-Exist')):
                    Lb2.itemconfig(i, bg='#c2ff57')
                elif (tempFunc.name == 'If-Not-Exist' or (
                        (tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '') and tempFunc.father[
                    1] == 'If-Not-Exist')):
                    Lb2.itemconfig(i, bg='#ff8657')
                elif (tempFunc.name == 'Else' or (
                        (tempFunc.name == '{' or tempFunc.name == '}' or tempFunc.name == '') and tempFunc.father[
                    1] == 'Else')):
                    Lb2.itemconfig(i, bg='#579aff')
                elif (currentScript.functions[i].name == 'Double-Click'):
                    Lb2.itemconfig(i, bg='#d557ff')
                elif (currentScript.functions[i].name == 'Insert-Input'):
                    Lb2.itemconfig(i, bg='#078f02')
                elif (currentScript.functions[i].name == 'Sleep'):
                    Lb2.itemconfig(i, bg='#57ff7f')
            else:
                Lb2.itemconfig(i, bg='#2b2b2b')

