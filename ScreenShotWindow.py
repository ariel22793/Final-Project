import os
from tkinter import *
from PIL import Image
import pyautogui
import Photo
from Photo import Photo


class ScreenShotWindow():
    def __init__(self,mainScreen,Lb2,currentScript,tree,photoViewFrame):
        mainScreen.iconify()
        window2 = Tk()
        window2.title("window2")
        window2.attributes('-fullscreen', True)
        window2.attributes('-alpha', 0.3)

        #tkinter.messagebox.showinfo("Notic!", "Press ENTER To Take ScreenShot\nPress ESC To Quit")
        self.width = window2.winfo_screenwidth()
        self.heigth = window2.winfo_screenheight()

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
                img = img.crop((self.x0, self.y0, self.x1, self.y1))

                index = Lb2.curselection()[0]
                currentFunction = currentScript.functions[index]

                numberOfImages = len([name for name in os.listdir(currentScript.path + 'ScreenShots\\')])
                imgName = "Screen" + str(numberOfImages) + ".png"
                if not os.path.exists(currentScript.path + 'ScreenShots\\'):
                    os.mkdir(currentScript.path + 'ScreenShots\\')

                if currentFunction.img == '':
                    img.save(currentScript.path + 'ScreenShots\\' + imgName)
                else:
                    img.save(currentScript.path + 'ScreenShots\\' + currentFunction.img.img)

                img = Photo(self.x0, self.y0, self.x1, self.y1, imgName)

                mainScreen.state('zoomed')
                self.window.destroy()

                for func in range(len(currentScript.functions)):
                    if currentScript.functions[func].id == index:
                        currentScript.functions[func].img = img
                        if currentScript.functions[func].name == 'If-Exist' or \
                                currentScript.functions[func].name == 'If-Not-Exist':
                            currentScript.functions[func].extra.image = img.img
                        if (currentScript.functions[func].father[1] == 'Repeat' or currentScript.functions[func].father[1] == 'If-Exist' or currentScript.functions[func].father[1] == 'If-Not-Exist' or currentScript.functions[func].father[1] == 'Else') and currentScript.functions[func].id !=currentScript.functions[func].father[0]   :
                            currentScript.functions[currentScript.functions[func].father[0]].extra.functions[
                                func - currentScript.functions[func].father[0] - 2].img = img
                Lb2.select_clear(0, END)
                self.updateLb2(Lb2,currentScript)
                self.FocusOnSelectedFunc(mainScreen,Lb2,currentScript,index,photoViewFrame)

                for i in tree.get_children(): #clear treeView
                    tree.delete(i)

                root = tree.insert('', 'end', text=currentScript.name, open=True, tag='T')
                self.SUBS(currentScript.path,root,tree)


        if str(event.keysym) == 'Escape':
            print("Quit window")
            mainScreen.state('zoomed')
            self.window.destroy()

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
            Lb2.select_set(index)
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


    def updateLb2(self,Lb2,currentScript):
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

