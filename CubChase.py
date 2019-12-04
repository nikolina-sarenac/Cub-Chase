from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QLineEdit, QInputDialog)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QPixmap, QIcon)
import sys


class CubChase(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("rsz_lion.jpg")
        self.setMaximumSize(640, 480)
        self.setMinimumSize(640, 480)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

        self.move(150, 100)
        self.setWindowTitle('Start window')

        self.btn = QPushButton('', self)
        self.btn.clicked.connect(self.showDialog)
        self.btn.setIcon(QIcon("startdugme.jpg"))
        self.btn.setStyleSheet('background-color: #fdc086; border: 5px solid beige; font: Bold')
        self.btn.setIconSize(QSize(89, 46))
        self.btn.resize(93, 50)
        self.btn.move(150, 340)


        self.show()

    def showDialog(self):
        self.pixmap = QPixmap("pozadina2.png")
        self.lbl.setPixmap(self.pixmap)

        self.btn.setText('')
        self.btn.resize(150, 50)
        self.btn.move(100, 400)
        self.btn.setIcon(QIcon("startdugme.jpg"))
        self.btn.setIconSize(QSize(89, 46))
        self.btn.resize(93, 50)
        self.btn.move(285, 355)
        


        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubChase = CubChase()
    sys.exit(app.exec_())