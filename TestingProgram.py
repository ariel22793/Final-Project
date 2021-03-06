from tkinter import *
from PIL import Image, ImageTk
counter = [0]


def add(counter):
    counter[0] += 1
    update()

def down(counter):
    counter[0] -= 1
    update()


def clear(counter):
    counter[0]=0
    update()


def doubleClick(couter):
    counter[0]+=3
    update()


def update():
    counterShow.config(text="Counter: " +str(counter[0]))


def colorChange():
    if daniDinButton.cget('bg') == 'black':
        daniDinButton.config(bg='white', fg='black')
    elif daniDinButton.cget('bg') == 'white':
        daniDinButton.config(bg='black', fg='white')


if __name__ == '__main__':

    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("Testing App")


    title = Label(mainScreen, text='Testing App', font=("Helvetica", 40))
    title.place(x=500,y=50)

    counterShow = Label(mainScreen, text='Counter: ' +str(counter[0]), font=("Helvetica", 30))
    counterShow.place(x=550,y=150)

    counterUp = Button(mainScreen, text= '+1', width=20, height=5, bg='blue', fg='white', font=("Helvetica", 15))
    counterUp.place(x=300, y=200)
    counterUp.bind('<Button-1>', lambda event : add(counter))

    counterDoubleClick = Button(mainScreen, text='+3 (DoubleClick)', width=15, height=3, bg='Green', fg='white', font=("Helvetica", 10))
    counterDoubleClick.place(x=580, y=200)
    counterDoubleClick.bind('<Double-Button-1>', lambda event: doubleClick(counter))

    counterDown = Button(mainScreen, text= '-1',  width=20, height=5, bg='red', fg='white', font=("Helvetica", 15))
    counterDown.place(x=800, y=200)
    counterDown.bind('<Button-1>', lambda event: down(counter))

    counterClear = Button(mainScreen, text= 'Clear (RightClick)',  width=20, height=5,  font=("Helvetica", 15))
    counterClear.place(x=550, y=360)
    counterClear.bind('<Button-3>', lambda event: clear(counter))

    daniDinButton = Button(mainScreen, text='Click To Change Color!', width=50, height=3,bg='black', fg='white', font=("Helvetica", 10))
    daniDinButton.place(x=460, y=520)
    daniDinButton.bind('<Button-1>', lambda event: colorChange())

    mainScreen.mainloop()


