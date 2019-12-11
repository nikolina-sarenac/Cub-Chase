from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton, QLineEdit, QInputDialog)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QPixmap, QIcon, QCursor)
from PyQt5 import QtCore
import sys
from PyQt5.uic.properties import QtCore
from pygame.locals import *
import pygame


class Maze:
    def __init__(self):
        self.M = 22
        self.N = 16
        self.maze = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
                     1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
                     1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
                     1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
                     1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1,
                     1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,
                     1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,
                     1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1,
                     1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1,
                     1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
                     1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1,
                     1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
                     1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1,
                     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def draw(self, display_surf, image_surf):
        bx = 0
        by = 0
        for i in range(0, self.M * self.N):
            if self.maze[bx + (by * self.M)] == 1:
                display_surf.blit(image_surf, (bx * 29, by * 30))

            bx = bx + 1
            if bx > self.M - 1:
                bx = 0
                by = by + 1


class CubChase(QWidget):
    windowWidth = 640
    windowHeight = 480

    def __init__(self):
        super().__init__()
        self.maze = Maze()
        self._block_surf = None
        self._display_surf = None
        self._background = None

        self.initUI()

    def initUI(self):
        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap("pocetna.jpg")
        self.setMaximumSize(640, 480)
        self.setMinimumSize(640, 480)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)

        self.hbox.addWidget(self.lbl)
        self.setLayout(self.hbox)

        self.move(150, 100)
        self.setWindowTitle('Cub Chase')

        self.txtbox1 = QLineEdit(self)
        self.txtbox1.move(228, 315)
        self.txtbox1.resize(93, 23)
        self.txtbox1.setStyleSheet('background-color: #f5deb3; border: 2px solid teal; font: Bold')
        self.txtbox1.setAlignment(Qt.AlignCenter)
        self.txtbox1.setVisible(False)

        self.txtbox2 = QLineEdit(self)
        self.txtbox2.move(344, 315)
        self.txtbox2.resize(93, 23)
        self.txtbox2.setStyleSheet('background-color: #f5deb3; border: 2px solid teal; font: Bold')
        self.txtbox2.setAlignment(Qt.AlignCenter)
        self.txtbox2.setVisible(False)

        self.btn = QPushButton('', self)
        self.btn.clicked.connect(self.showDialog)
        self.btn.setStyleSheet('background-color: rgba(255, 255, 255, 0)')
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setIconSize(QSize(89, 46))
        self.btn.resize(100, 50)
        self.btn.move(120, 323)

        self.btn1 = QPushButton('', self)
        self.btn1.setVisible(False)

        self.show()

    def showDialog(self):
        self.pixmap = QPixmap("pozadina2.png")
        self.lbl.setPixmap(self.pixmap)

        self.txtbox1.setVisible(True)
        self.txtbox2.setVisible(True)

        self.btn1.setVisible(True)
        self.btn1.setText('')
        self.btn1.resize(150, 50)
        self.btn1.move(100, 400)
        self.btn1.setIcon(QIcon("startdugme.jpg"))
        self.btn1.setIconSize(QSize(89, 46))
        self.btn1.resize(93, 50)
        self.btn1.move(285, 355)
        self.btn1.clicked.connect(self.showMaze)
        self.btn1.clicked.connect(self.hide)

        self.show()

    def showMaze(self):
        pygame.init()
        pygame.display.set_caption('Cub Chase')
        self.move(150, 100)
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._block_surf = pygame.image.load("block3.jpg").convert()
        self._background = pygame.image.load("playWin.png").convert()
        self.on_render()
        self.show()

    def on_render(self):
        screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        screen.blit(self._background, [0, 0])
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubChase = CubChase()
    sys.exit(app.exec_())