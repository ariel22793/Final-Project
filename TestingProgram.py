from tkinter import *

counter = [0]


def add(counter):
    counter[0] += 1
    update()

def down(counter):
    counter[0] -= 1
    update()

def update():
    counterShow.config(text="Counter: " +str(counter[0]))

if __name__ == '__main__':
    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("Testing App")


    title = Label(mainScreen, text='Testing App', font=("Helvetica", 40))
    title.place(x=850,y=100)

    counterShow = Label(mainScreen, text='Counter: ' +str(counter[0]), font=("Helvetica", 30))
    counterShow.place(x=910,y=300)

    counterUp = Button(mainScreen, text= '+1', width=20, height=5, bg='blue', fg='white', font=("Helvetica", 15))
    counterUp.place(x=600, y=500)
    counterUp.bind('<Button-1>', lambda event : add(counter))

    counterDown = Button(mainScreen, text= '-1',  width=20, height=5, bg='red', fg='white', font=("Helvetica", 15))
    counterDown.place(x=1200, y=500)
    counterDown.bind('<Button-1>', lambda event: down(counter))
    counterDown = Button(mainScreen, text= 'Clear',  width=20, height=5,  font=("Helvetica", 15))
    counterDown.place(x=900, y=700)


    mainScreen.mainloop()


