from tkinter import *
from PIL import Image, ImageTk
counter=1
success = 0

def fun(number_of_button):
    global counter
    global success
    counter+=1

    if number_of_button == 51:
        print('done')
        print("Success: " + str(success)+"/50")
        print("Percentages: " + str((success/50)*100)+"%")
        exit()
    if counter == number_of_button:
        print('ok! counter is ' + str(counter) + ' and buttin number is ' + str(number_of_button) )
        success+=1
    else:
        print('faild! counter is ' + str(counter) + ' and buttin number is ' + str(number_of_button))


if __name__ == '__main__':
    mainScreen = Tk()
    mainScreen.state("zoomed")
    mainScreen.title("Testing App")



    frame = Frame(mainScreen, width=1000, height=1000)
    frame.pack(fill=BOTH)
    canvas = Canvas(frame, width=1000, height=1000)
    canvas.pack(fill=BOTH)


    newPButton = PhotoImage(file=r"img\PNG\virb.png")
    canvas.Button1 = newPButton
    np = canvas.create_image(10, 10, anchor=NW, image=newPButton, tags="one")
    canvas.tag_bind('one', '<Button>',  lambda event: fun(1))


    newPButton2 = PhotoImage(file=r"img\PNG\facebook.png")
    canvas.Button2 = newPButton2
    np2 = canvas.create_image(30, 10, anchor=NW, image=newPButton2, tags="two")
    canvas.tag_bind('two', '<Button>', lambda event: fun(2))

    newPButton3 = PhotoImage(file=r"img\PNG\wordpress.png")
    canvas.Button3 = newPButton3
    np3 = canvas.create_image(70, 10, anchor=NW, image=newPButton3, tags="three")
    canvas.tag_bind('three', '<Button>', lambda event: fun(3))

    newPButton4 = PhotoImage(file=r"img\PNG\qik.png")
    canvas.Button4 = newPButton4
    np4 = canvas.create_image(90, 10, anchor=NW, image=newPButton4, tags="four")
    canvas.tag_bind('four', '<Button>', lambda event: fun(4))

    newPButton5 = PhotoImage(file=r"img\PNG\ebay.png")
    canvas.Button5 = newPButton5
    np5 = canvas.create_image(120, 10, anchor=NW, image=newPButton5, tags="five")
    canvas.tag_bind('five', '<Button>', lambda event: fun(5))

    newPButton6 = PhotoImage(file=r"img\PNG\paypal.png")
    canvas.Button6 = newPButton6
    np6 = canvas.create_image(155, 10, anchor=NW, image=newPButton6, tags="six")
    canvas.tag_bind('six', '<Button>', lambda event: fun(6))

    newPButton7 = PhotoImage(file=r"img\PNG\git.png")
    canvas.Button7 = newPButton7
    np7 = canvas.create_image(175, 10, anchor=NW, image=newPButton7, tags="seven")
    canvas.tag_bind('seven', '<Button>', lambda event: fun(7))

    newPButton8 = PhotoImage(file=r"img\PNG\amazon.png")
    canvas.Button8 = newPButton8
    np8 = canvas.create_image(195, 10, anchor=NW, image=newPButton8, tags="eghit")
    canvas.tag_bind('eghit', '<Button>', lambda event: fun(8))

    newPButton9 = PhotoImage(file=r"img\PNG\wifi.png")
    canvas.Button9 = newPButton9
    np9 = canvas.create_image(217, 10, anchor=NW, image=newPButton9, tags="nine")
    canvas.tag_bind('nine', '<Button>', lambda event: fun(9))

    newPButton10 = PhotoImage(file=r"img\PNG\windows.png")
    canvas.Button10 = newPButton10
    np10 = canvas.create_image(290, 10, anchor=NW, image=newPButton10, tags="ten")
    canvas.tag_bind('ten', '<Button>', lambda event: fun(10))


    newPButton11 = PhotoImage(file=r"img\PNG\google.png")
    canvas.Button11 = newPButton11
    np11 = canvas.create_image(430, 10, anchor=NW, image=newPButton11, tags="eleven")
    canvas.tag_bind('eleven', '<Button>', lambda event: fun(11))

    newPButton12 = PhotoImage(file=r"img\PNG\heart.png")
    canvas.Button12 = newPButton12
    np12 = canvas.create_image(10, 200, anchor=NW, image=newPButton12, tags="12")
    canvas.tag_bind('12', '<Button>', lambda event: fun(12))

    newPButton13 = PhotoImage(file=r"img\PNG\lab.png")
    canvas.Button13 = newPButton13
    np13 = canvas.create_image(30, 200, anchor=NW, image=newPButton13, tags="13")
    canvas.tag_bind('13', '<Button>', lambda event: fun(13))

    newPButton14 = PhotoImage(file=r"img\PNG\inbox.png")
    canvas.Button14 = newPButton14
    np14 = canvas.create_image(50, 200, anchor=NW, image=newPButton14, tags="14")
    canvas.tag_bind('14', '<Button>', lambda event: fun(14))

    newPButton15 = PhotoImage(file=r"img\PNG\folder.png")
    canvas.Button15 = newPButton15
    np15 = canvas.create_image(80, 200, anchor=NW, image=newPButton15, tags="15")
    canvas.tag_bind('15', '<Button>', lambda event: fun(15))

    newPButton16 = PhotoImage(file=r"img\PNG\mackdonalds.png")
    canvas.Button16 = newPButton16
    np16 = canvas.create_image(120, 200, anchor=NW, image=newPButton16, tags="16")
    canvas.tag_bind('16', '<Button>', lambda event: fun(16))

    newPButton17 = PhotoImage(file=r"img\PNG\chrome.png")
    canvas.Button17 = newPButton17
    np17 = canvas.create_image(190, 200, anchor=NW, image=newPButton17, tags="17")
    canvas.tag_bind('17', '<Button>', lambda event: fun(17))

    newPButton18 = PhotoImage(file=r"img\PNG\airbnb.png")
    canvas.Button18 = newPButton18
    np18 = canvas.create_image(220, 200, anchor=NW, image=newPButton18, tags="18")
    canvas.tag_bind('18', '<Button>', lambda event: fun(18))

    newPButton19 = PhotoImage(file=r"img\PNG\nike.png")
    canvas.Button19 = newPButton19
    np19 = canvas.create_image(255, 200, anchor=NW, image=newPButton19, tags="19")
    canvas.tag_bind('19', '<Button>', lambda event: fun(19))

    newPButton20 = PhotoImage(file=r"img\PNG\timber.png")
    canvas.Button20 = newPButton20
    np20 = canvas.create_image(285, 200, anchor=NW, image=newPButton20, tags="20")
    canvas.tag_bind('20', '<Button>', lambda event: fun(20))



    newPButton21 = PhotoImage(file=r"img\PNG\viber.png")
    canvas.Button21 = newPButton21
    np21 = canvas.create_image(10, 300, anchor=NW, image=newPButton21, tags="21")
    canvas.tag_bind('21', '<Button>', lambda event: fun(21))

    newPButton22 = PhotoImage(file=r"img\PNG\whatsapp.png")
    canvas.Button22 = newPButton22
    np22 = canvas.create_image(50, 300, anchor=NW, image=newPButton22, tags="22")
    canvas.tag_bind('22', '<Button>', lambda event: fun(22))

    newPButton23 = PhotoImage(file=r"img\PNG\dropbox.png")
    canvas.Button23 = newPButton23
    np23 = canvas.create_image(150, 300, anchor=NW, image=newPButton23, tags="23")
    canvas.tag_bind('23', '<Button>', lambda event: fun(23))

    newPButton24 = PhotoImage(file=r"img\PNG\linkdin.png")
    canvas.Button24 = newPButton24
    np24 = canvas.create_image(239, 300, anchor=NW, image=newPButton24, tags="24")
    canvas.tag_bind('24', '<Button>', lambda event: fun(24))

    newPButton25 = PhotoImage(file=r"img\PNG\snapshot.png")
    canvas.Button25 = newPButton25
    np25 = canvas.create_image(380, 300, anchor=NW, image=newPButton25, tags="25")
    canvas.tag_bind('25', '<Button>', lambda event: fun(25))

    newPButton26 = PhotoImage(file=r"img\PNG\ball.png")
    canvas.Button26 = newPButton26
    np26 = canvas.create_image(460, 300, anchor=NW, image=newPButton26, tags="26")
    canvas.tag_bind('26', '<Button>', lambda event: fun(26))

    newPButton27 = PhotoImage(file=r"img\PNG\facebookmsg.png")
    canvas.Button27 = newPButton27
    np27 = canvas.create_image(490, 300, anchor=NW, image=newPButton27, tags="27")
    canvas.tag_bind('27', '<Button>', lambda event: fun(27))

    newPButton28 = PhotoImage(file=r"img\PNG\be.png")
    canvas.Button28 = newPButton28
    np28 = canvas.create_image(550, 300, anchor=NW, image=newPButton28, tags="28")
    canvas.tag_bind('28', '<Button>', lambda event: fun(28))

    newPButton29 = PhotoImage(file=r"img\PNG\mexico.png")
    canvas.Button29 = newPButton29
    np29 = canvas.create_image(10, 360, anchor=NW, image=newPButton29, tags="29")
    canvas.tag_bind('29', '<Button>', lambda event: fun(29))

    newPButton30 = PhotoImage(file=r"img\PNG\sydney.png")
    canvas.Button30 = newPButton30
    np30 = canvas.create_image(10, 400, anchor=NW, image=newPButton30, tags="30")
    canvas.tag_bind('30', '<Button>', lambda event: fun(30))

    newPButton31 = PhotoImage(file=r"img\PNG\egipt.png")
    canvas.Button31 = newPButton31
    np31 = canvas.create_image(10, 440, anchor=NW, image=newPButton31, tags="31")
    canvas.tag_bind('31', '<Button>', lambda event: fun(31))

    newPButton32 = PhotoImage(file=r"img\PNG\rio.png")
    canvas.Button32 = newPButton32
    np32 = canvas.create_image(10, 480, anchor=NW, image=newPButton32, tags="32")
    canvas.tag_bind('32', '<Button>', lambda event: fun(32))

    newPButton33 = PhotoImage(file=r"img\PNG\rome.png")
    canvas.Button33 = newPButton33
    np33 = canvas.create_image(10, 520, anchor=NW, image=newPButton33, tags="33")
    canvas.tag_bind('33', '<Button>', lambda event: fun(33))

    newPButton34 = PhotoImage(file=r"img\PNG\newyork.png")
    canvas.Button34 = newPButton34
    np34 = canvas.create_image(10, 560, anchor=NW, image=newPButton34, tags="34")
    canvas.tag_bind('34', '<Button>', lambda event: fun(34))

    newPButton35 = PhotoImage(file=r"img\PNG\india.png")
    canvas.Button35 = newPButton35
    np35 = canvas.create_image(10, 600, anchor=NW, image=newPButton35, tags="35")
    canvas.tag_bind('35', '<Button>', lambda event: fun(35))

    newPButton36 = PhotoImage(file=r"img\PNG\hoolywood.png")
    canvas.Button36 = newPButton36
    np36 = canvas.create_image(50, 600, anchor=NW, image=newPButton36, tags="36")
    canvas.tag_bind('36', '<Button>', lambda event: fun(36))

    newPButton37 = PhotoImage(file=r"img\PNG\x.png")
    canvas.Button37 = newPButton37
    np37 = canvas.create_image(90, 600, anchor=NW, image=newPButton37, tags="37")
    canvas.tag_bind('37', '<Button>', lambda event: fun(37))

    newPButton38 = PhotoImage(file=r"img\PNG\vi.png")
    canvas.Button38 = newPButton38
    np38 = canvas.create_image(140, 600, anchor=NW, image=newPButton38, tags="38")
    canvas.tag_bind('38', '<Button>', lambda event: fun(38))

    newPButton39 = PhotoImage(file=r"img\PNG\left.png")
    canvas.Button39 = newPButton39
    np39 = canvas.create_image(190, 600, anchor=NW, image=newPButton39, tags="39")
    canvas.tag_bind('39', '<Button>', lambda event: fun(39))

    newPButton40 = PhotoImage(file=r"img\PNG\right.png")
    canvas.Button40 = newPButton40
    np40 = canvas.create_image(240, 600, anchor=NW, image=newPButton40, tags="40")
    canvas.tag_bind('40', '<Button>', lambda event: fun(40))

    newPButton41 = PhotoImage(file=r"img\PNG\Ai.png")
    canvas.Button41 = newPButton41
    np41 = canvas.create_image(290, 600, anchor=NW, image=newPButton41, tags="41")
    canvas.tag_bind('41', '<Button>', lambda event: fun(41))

    newPButton42 = PhotoImage(file=r"img\PNG\triangle.png")
    canvas.Button42 = newPButton42
    np42 = canvas.create_image(340, 600, anchor=NW, image=newPButton42, tags="42")
    canvas.tag_bind('42', '<Button>', lambda event: fun(42))

    newPButton43 = PhotoImage(file=r"img\PNG\sad.png")
    canvas.Button43 = newPButton43
    np43 = canvas.create_image(900, 10, anchor=NW, image=newPButton43, tags="43")
    canvas.tag_bind('43', '<Button>', lambda event: fun(43))

    newPButton44 = PhotoImage(file=r"img\PNG\xoxo.png")
    canvas.Button44 = newPButton44
    np44 = canvas.create_image(900, 150, anchor=NW, image=newPButton44, tags="44")
    canvas.tag_bind('44', '<Button>', lambda event: fun(44))

    newPButton45 = PhotoImage(file=r"img\PNG\sunglasses.png")
    canvas.Button45 = newPButton45
    np45 = canvas.create_image(900, 290, anchor=NW, image=newPButton45, tags="45")
    canvas.tag_bind('45', '<Button>', lambda event: fun(45))

    newPButton46 = PhotoImage(file=r"img\PNG\cry.png")
    canvas.Button46 = newPButton46
    np46 = canvas.create_image(900, 440, anchor=NW, image=newPButton46, tags="46")
    canvas.tag_bind('46', '<Button>', lambda event: fun(46))


    newPButton47 = PhotoImage(file=r"img\PNG\woman.png")
    canvas.Button47 = newPButton47
    np47 = canvas.create_image(1200, 10, anchor=NW, image=newPButton47, tags="47")
    canvas.tag_bind('47', '<Button>', lambda event: fun(47))

    newPButton48 = PhotoImage(file=r"img\PNG\woman2.png")
    canvas.Button48 = newPButton48
    np48 = canvas.create_image(1200,70, anchor=NW, image=newPButton48, tags="48")
    canvas.tag_bind('48', '<Button>', lambda event: fun(48))

    newPButton49 = PhotoImage(file=r"img\PNG\view.png")
    canvas.Button49 = newPButton49
    np49 = canvas.create_image(1200, 170, anchor=NW, image=newPButton49, tags="49")
    canvas.tag_bind('49', '<Button>', lambda event: fun(49))

    newPButton50 = PhotoImage(file=r"img\PNG\view2.png")
    canvas.Button50 = newPButton50
    np50 = canvas.create_image(1200, 230, anchor=NW, image=newPButton50, tags="50")
    canvas.tag_bind('50', '<Button>', lambda event: fun(50))

    newPButton51 = PhotoImage(file=r"img\PNG\done.png")
    canvas.Button51 = newPButton51
    np51 = canvas.create_image(1150, 400, anchor=NW, image=newPButton51, tags="51")
    canvas.tag_bind('51', '<Button>', lambda event: fun(51))


    mainScreen.mainloop()


