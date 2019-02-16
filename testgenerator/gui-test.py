# Introduction to PyQt5

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Test GUI"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initFileMenu(self):
        fileMenu = self.menuBar().addMenu('File')
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

    def initMenuBar(self):
        mainMenu = self.menuBar()
        self.initFileMenu()
        mainMenu.addMenu('Edit')
        mainMenu.addMenu('View')
        mainMenu.addMenu('Search')
        mainMenu.addMenu('Tools')
        mainMenu.addMenu('Help')

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.initMenuBar()
        self.show()



def main():
    app=QApplication(sys.argv)
    ex=App()
    app.exec_()



if __name__=='__main__': main()
