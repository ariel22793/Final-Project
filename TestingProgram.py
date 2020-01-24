from tkinter import *







def counterUp():


if __name__ == '__main__':
    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("Testing App")

    counter=0

    title = Label(mainScreen, text='Testing App', font=("Helvetica", 40))
    title.place(x=850,y=100)

    counterShow = Label(mainScreen, text='Counter: ' +str(counter), font=("Helvetica", 30))
    counterShow.place(x=910,y=300)

    counterUp = Button(mainScreen, text= '+1', width=20, height=5, bg='blue', fg='white', font=("Helvetica", 15), command = counterUp)
    counterUp.place(x=600, y=500)

    counterDown = Button(mainScreen, text= '-1',  width=20, height=5, bg='red', fg='white', font=("Helvetica", 15))
    counterDown.place(x=1200, y=500)

    counterDown = Button(mainScreen, text= 'Clear',  width=20, height=5,  font=("Helvetica", 15))
    counterDown.place(x=900, y=700)


    mainScreen.mainloop()


