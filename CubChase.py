from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QLineEdit, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class CubChase(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.hbox = QHBoxLayout(self)

        self.pixmap = QPixmap("rsz_lion.jpg")

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)


        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

        self.move(150, 100)
        self.setWindowTitle('Start window')
        

        self.btn = QPushButton('Start', self)
        self.btn.resize(90, 50)
        self.btn.move(150, 340)


        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubChase = CubChase()
    sys.exit(app.exec_())