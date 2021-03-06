import os
from tkinter import *
from PIL import Image
import pyautogui
import Photo
from Photo import Photo


class ScreenShotWindow():
    def __init__(self,mainScreen,Lb2,currentScript,explorerFrame):
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
        window2.bind('<Key>', lambda event :self.keyPress(event,mainScreen,Lb2,currentScript,explorerFrame))
        window2.bind('<Motion>', self.paint)
        window2.bind('<ButtonRelease-1>', self.getMaousePosition)



    def keyPress(self, event,mainScreen,Lb2,currentScript,explorerFrame):
        if str(event.keysym) == 'Return':
            if self.x0 != self.x1 and self.y0 != self.y1:
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save('Screen.png')
                img = Image.open("Screen.png")
                img = img.crop((self.x0, self.y0, self.x1, self.y1))

                currentFunction = currentScript.functions[Lb2.curselection()[0]]

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
                    if currentScript.functions[func].id == Lb2.curselection()[0]:
                        currentScript.functions[func].img = img
                        if currentScript.functions[func].name == 'If-Exist' or \
                                currentScript.functions[func].name == 'If-Not-Exist':
                            currentScript.functions[func].extra.image = img.img
                        if (currentScript.functions[func].father[1] == 'Repeat' or currentScript.functions[func].father[1] == 'If-Exist' or currentScript.functions[func].father[1] == 'If-Not-Exist' or currentScript.functions[func].father[1] == 'Else') and currentScript.functions[func].id !=currentScript.functions[func].father[0]   :
                            currentScript.functions[currentScript.functions[func].father[0]].extra.functions[
                                func - currentScript.functions[func].father[0] - 2].img = img
                Lb2.select_clear(0, END)
                self.updateLb2(Lb2,currentScript)


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

    def updateLb2(self,Lb2,currentScript):
        Lb2.delete(0, 'end')
        for x in range(0, len(currentScript.functions)):
            name = currentScript.functions[x].name
            shift = ' ' * currentScript.functions[x].indention * 5
            if name == 'Sleep' or name == 'Repeat':
                Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.time))
                # Lb2.place(x=0, y=40)
                Lb2.pack(side="left", fill="y")

            elif name == 'If-Exist' or name == 'If-Not-Exist':
                Lb2.insert(x, shift + name + '({})'.format(currentScript.functions[x].extra.image))
                # Lb2.place(x=0, y=40)
                Lb2.pack(side="left", fill="y")

            else:
                Lb2.insert(x, shift + name)
                # Lb2.place(x=0, y=40)
                Lb2.pack(side="left", fill="y")
