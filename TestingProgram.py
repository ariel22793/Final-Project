from tkinter import *

mainScreen = Tk()
mainScreen.state("zoomed")
mainScreen.title("Testing App")





counterUp = Button(mainScreen, text= '+1', width=20, height=5, bg='blue', fg='white', font=("Helvetica", 15))
counterUp.place(x=600, y=500)

counterDown = Button(mainScreen, text= '-1',  width=20, height=5, bg='red', fg='white', font=("Helvetica", 15))
counterDown.place(x=1200, y=500)

counterDown = Button(mainScreen, text= 'Clear',  width=20, height=5,  font=("Helvetica", 15))
counterDown.place(x=900, y=700)




mainScreen.mainloop()