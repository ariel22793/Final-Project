from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from PyQt5.QtCore import QDir, Qt
import pyautogui
import time
import sys
import win32gui, win32con
import photoSelect






class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WindowScreenShot")

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.c2 = event.GetPosition()
            self.Refresh()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('ui.ui', self)
        self.addfu.clicked.connect(self.func)
        self.stop_3.clicked.connect(self.func2)
        self.stop_5.clicked.connect(self.screenShot)
        self.pushButton.setIcon(QtGui.QIcon('img/start2.png'))
        self.pushButton_2.setIcon(QtGui.QIcon('img/stop.png'))
        self.pushButton_3.setIcon(QtGui.QIcon('img/open.png'))
        self.pushButton_4.setIcon(QtGui.QIcon('img/save.png'))

        allFuncList =['Click', 'Exist', 'NoExist']
        self.listWidget.addItems(allFuncList)
        self.selectedFuncList = []
        self.addfu.setStyleSheet("background-color: \
                               rgba(255,255,255,255); \
                               color: rgba(0,0,10,255); \
                               border-style: solid; \
                               border-radius: 8px;")


        self.stop_3.setStyleSheet("background-color: \
                               rgba(255,255,255,255); \
                               color: rgba(0,0,10,255); \
                               border-style: solid; \
                               border-radius: 8px;")

        self.stop_5.setStyleSheet("background-color: \
                                       rgba(255,255,255,255); \
                                       color: rgba(0,0,10,255); \
                                       border-style: solid; \
                                       border-radius: 8px;")


        file = QAction('File', self)
        edit = QAction('Edit', self)
        view = QAction('View', self)

        self.statusBar()
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(file)
        toolbar.addAction(edit)
        toolbar.addAction(view)

        load_project_structure(os.path.dirname(os.path.abspath(__file__)), self.treeWidget)

    def func(self):
        try:
            self.selectedFuncList.append(self.listWidget.currentItem().text())
            self.script.clear()
            self.script.addItems(self.selectedFuncList)
            print(self.selectedFuncList)
        except Exception as e:
            print(e)

    def func2(self):
        try:
            self.selectedFuncList.remove((self.script.currentItem().text()))
            self.script.takeItem(self.script.row(self.script.currentItem()))

        except Exception as e:
            print(e)

    def screenShot(self, event):
        print('pressed screen')
        time.sleep(2)
        Minimize = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
        self.window2()



    def window2(self):  # <===             ##screen shot 2 button show
        self.w = Window2()
        painter = QPainter(self.w)
        painter.setOpacity(0.3)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())

        self.w.setWindowFlags(Qt.FramelessWindowHint)
        self.w.setAttribute(Qt.WA_NoSystemBackground, True)
        # self.w.setAttribute(Qt.WA_TranslucentBackground, True)



        # Create the button
        pushButton = QPushButton(self.w)
        pushButton.setGeometry(QRect(1000, 900, 200, 50))
        pushButton.setText("close Window")
        pushButton.clicked.connect(self.w.close)

        pushButton2 = QPushButton(self.w)
        pushButton2.setGeometry(QRect(730, 900, 200, 50))
        pushButton2.setText("Take ScreenShot")
        pushButton2.clicked.connect(self.takePhoto)



        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        for i in top_windows:
            if "WindowScreenShot" in i[1].lower():
                print(i)
                win32gui.ShowWindow(i[0], 5)
                win32gui.SetForegroundWindow(i[0])
                break

        self.w.showMaximized()
        Minimize = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)



    def takePhoto(self):
        self.w.close()
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('Screen.png')
        top_windows = []
        self.window3()


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))




def load_project_structure(startpath, tree):

    # import os
    # from PyQt5.QtWidgets import QTreeWidgetItem
    # from PyQt5.QtGui import QIcon
    for element in os.listdir(startpath):
        path_info = startpath + "/" + element
        parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
        if os.path.isdir(path_info):
            load_project_structure(path_info, parent_itm)
            parent_itm.setIcon(0, QIcon('img/open.png'))
        else:
            parent_itm.setIcon(0, QIcon('img/file.png'))


if __name__=='__main__':
    app =QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())