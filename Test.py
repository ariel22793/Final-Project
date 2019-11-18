from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
from PyQt5.QtCore import QDir, Qt




import easygui
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('ui.ui', self)
        self.addfu.clicked.connect(self.func)
        self.stop_3.clicked.connect(self.func2)
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



def load_project_structure(startpath, tree):
    """
    Load Project structure tree
    :param startpath:
    :param tree:
    :return:
    """
    import os
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QIcon
    print(startpath)
    for element in os.listdir(startpath):
        path_info = startpath + "/" + element
        parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
        if os.path.isdir(path_info):
            load_project_structure(path_info, parent_itm)
            parent_itm.setIcon(0, QIcon('img/open.png'))
        else:
            parent_itm.setIcon(0, QIcon('img/file.png'))


if __name__=='__main__':
    import sys
    app =QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())